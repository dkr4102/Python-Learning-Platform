"""
Automated unit & integration tests for Pip Learn 2.0 Auth, Navigation, and Progress.
Tests Argon2id hashing, registration validation, duplicate prevention, sessions,
rate limiting, deterministic resume resolution, and cross-account progress isolation.
"""
import pytest
from datetime import datetime, timezone
from app.database.connection import get_db
from app.database.models import User, Learner, UserSession, LessonActivity, LessonCompletion, ModuleProgress
from app.auth.service import (
    hash_password,
    verify_password,
    register_user,
    authenticate_user,
    create_session,
    invalidate_session,
    validate_registration_input,
    is_rate_limited,
    record_failed_attempt,
    reset_failed_attempts,
)
from app.navigation.nav import resolve_resume_target
from app.database.crud import reset_learner_course_progress, get_learner_summary


def test_argon2id_hashing():
    """Verify password hashing produces Argon2id hashes and validates correctly."""
    raw = "SecureStudentPass2026!"
    hashed = hash_password(raw)
    assert hashed.startswith("$argon2id$")
    assert verify_password(hashed, raw) is True
    assert verify_password(hashed, "WrongPass123") is False


def test_registration_validation():
    """Verify input validation for learner registration."""
    # Short name
    assert validate_registration_input("A", "validuser", "user@test.com", "secret123", "secret123") is not None
    # Short username
    assert validate_registration_input("Valid Name", "ab", "user@test.com", "secret123", "secret123") is not None
    # Invalid characters in username
    assert validate_registration_input("Valid Name", "user@name!", "user@test.com", "secret123", "secret123") is not None
    # Invalid email
    assert validate_registration_input("Valid Name", "validuser", "not-an-email", "secret123", "secret123") is not None
    # Short password
    assert validate_registration_input("Valid Name", "validuser", "user@test.com", "123", "123") is not None
    # Mismatched passwords
    assert validate_registration_input("Valid Name", "validuser", "user@test.com", "secret123", "secret456") is not None
    # All valid
    assert validate_registration_input("Valid Name", "validuser", "user@test.com", "secret123", "secret123") is None


def test_user_registration_and_duplicate_prevention():
    """Verify clean registration and duplicate account prevention."""
    with get_db() as db:
        unique_suffix = int(datetime.now(timezone.utc).timestamp())
        uname = f"testuser_{unique_suffix}"
        email = f"testuser_{unique_suffix}@student.mu.edu.in"

        user, learner = register_user(
            db=db,
            name="Test Learner",
            username=uname,
            email=email,
            password="StrongPassword123!"
        )

        assert user.id is not None
        assert user.username == uname
        assert learner.user_id == user.id
        assert learner.onboarding_completed is False

        # Attempt duplicate username
        with pytest.raises(ValueError) as exc1:
            register_user(
                db=db,
                name="Another",
                username=uname,
                email=f"diff_{email}",
                password="AnotherPassword123!"
            )
        assert "already taken" in str(exc1.value)

        # Attempt duplicate email
        with pytest.raises(ValueError) as exc2:
            register_user(
                db=db,
                name="Another",
                username=f"diff_{uname}",
                email=email,
                password="AnotherPassword123!"
            )
        assert "already exists" in str(exc2.value)


def test_authentication_and_session_lifecycle():
    """Verify authentication, session token creation and database revocation."""
    with get_db() as db:
        unique_suffix = int(datetime.now(timezone.utc).timestamp())
        uname = f"authuser_{unique_suffix}"
        email = f"authuser_{unique_suffix}@student.mu.edu.in"
        pwd = "MySecretPassword2026!"

        user, learner = register_user(db, "Auth User", uname, email, pwd)

        # Successful auth
        authed_user = authenticate_user(db, uname, pwd)
        assert authed_user is not None
        assert authed_user.id == user.id

        # Auth by email
        authed_by_email = authenticate_user(db, email, pwd)
        assert authed_by_email is not None
        assert authed_by_email.id == user.id

        # Incorrect password
        failed_auth = authenticate_user(db, uname, "WrongPassword!")
        assert failed_auth is None

        # Session creation
        token = create_session(db, user.id, duration_days=7)
        assert len(token) > 30

        session_rec = db.query(UserSession).filter(UserSession.session_token == token).first()
        assert session_rec is not None
        assert session_rec.user_id == user.id

        # Revocation on logout
        revoked = invalidate_session(db, token)
        assert revoked is True
        assert db.query(UserSession).filter(UserSession.session_token == token).first() is None


def test_login_rate_limiting():
    """Verify rate limiting triggers after multiple failed attempts."""
    test_id = f"ratelimit_test_{datetime.now(timezone.utc).timestamp()}"
    reset_failed_attempts(test_id)

    assert is_rate_limited(test_id) is False
    for _ in range(4):
        record_failed_attempt(test_id)
    assert is_rate_limited(test_id) is False

    # 5th attempt triggers lockout
    record_failed_attempt(test_id)
    assert is_rate_limited(test_id) is True

    reset_failed_attempts(test_id)
    assert is_rate_limited(test_id) is False


def test_deterministic_resume_resolution():
    """Verify resume policy under different learner progression states."""
    with get_db() as db:
        unique_suffix = int(datetime.now(timezone.utc).timestamp())
        user, learner = register_user(
            db, "Resume Learner", f"resume_{unique_suffix}", f"resume_{unique_suffix}@mu.edu", "Pass123456!"
        )

        # 1. Fresh learner -> Module 1, Lesson 1, Read
        m_id, l_id, stage = resolve_resume_target(db, learner.id)
        assert m_id == 1
        assert l_id == "py-v2-u1-l01"
        assert stage == "read"

        # 2. Learner paused mid-way in experiment stage (after finishing reading)
        act = LessonActivity(
            learner_id=learner.id,
            module_id=1,
            lesson_id="py-v2-u1-l02",
            stage="experiment",
            reading_section=4,
            experiment_attempted=False
        )
        db.add(act)
        db.commit()

        m_id, l_id, stage = resolve_resume_target(db, learner.id)
        assert m_id == 1
        assert l_id == "py-v2-u1-l02"
        assert stage == "experiment"

        # 3. Learner finishes m1-l2
        comp = LessonCompletion(
            learner_id=learner.id,
            module_id=1,
            lesson_id="py-v2-u1-l02"
        )
        db.add(comp)
        db.commit()

        # Target advances to lesson 1 because it was never finished.
        m_id, l_id, stage = resolve_resume_target(db, learner.id)
        assert m_id == 1
        assert l_id == "py-v2-u1-l01"


def test_cross_account_isolation_and_progress_reset():
    """Verify two accounts have strictly isolated progress and progress reset is clean."""
    with get_db() as db:
        ts = int(datetime.now(timezone.utc).timestamp())
        u1, l1 = register_user(db, "User One", f"u1_{ts}", f"u1_{ts}@mu.edu", "Pass123456!")
        u2, l2 = register_user(db, "User Two", f"u2_{ts}", f"u2_{ts}@mu.edu", "Pass123456!")

        # Record completion for User One only
        c1 = LessonCompletion(learner_id=l1.id, module_id=1, lesson_id="py-v2-u1-l01")
        db.add(c1)
        db.commit()

        s1 = get_learner_summary(db, l1.id)
        s2 = get_learner_summary(db, l2.id)

        assert s1["total_lessons_completed"] == 1
        assert s2["total_lessons_completed"] == 0

        # Reset progress for User One
        reset_learner_course_progress(db, l1.id)
        s1_after = get_learner_summary(db, l1.id)
        assert s1_after["total_lessons_completed"] == 0
        # User account is preserved
        assert db.query(User).filter(User.id == u1.id).first() is not None
