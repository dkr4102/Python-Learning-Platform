"""
Pip Learn 2.0 - Real Authentication and Session Management Service
Implements Argon2id password hashing, database-persisted sessions,
NiceGUI storage integration, rate limiting, and learner binding.
"""
import re
import secrets
import time
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Dict, List
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from nicegui import app

from app.database.models import User, UserSession, Learner, utc_now
from app.database.crud import create_learner_for_user, get_learner_by_user_id

# Argon2id password hasher (RFC 9106 compliant)
ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MB
    parallelism=2,
    hash_len=32,
    salt_len=16
)

# In-memory rate limiting tracker: identifier -> list of failure timestamps
_FAILED_LOGINS: Dict[str, List[float]] = {}
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_WINDOW_SECONDS = 300  # 5 minutes


def hash_password(password: str) -> str:
    """Hash password using Argon2id."""
    return ph.hash(password)


def verify_password(hash_str: str, password: str) -> bool:
    """Verify password against Argon2id hash."""
    try:
        return ph.verify(hash_str, password)
    except (VerifyMismatchError, InvalidHashError, Exception):
        return False


def is_rate_limited(identifier: str) -> bool:
    """Check if identifier (IP or username) exceeded failed login threshold."""
    now = time.time()
    attempts = _FAILED_LOGINS.get(identifier, [])
    # Filter attempts within lockout window
    recent = [t for t in attempts if now - t < LOCKOUT_WINDOW_SECONDS]
    _FAILED_LOGINS[identifier] = recent
    return len(recent) >= MAX_FAILED_ATTEMPTS


def record_failed_attempt(identifier: str):
    """Record a failed login attempt for rate limiting."""
    now = time.time()
    attempts = _FAILED_LOGINS.setdefault(identifier, [])
    attempts.append(now)


def reset_failed_attempts(identifier: str):
    """Clear rate limiting history on successful authentication."""
    if identifier in _FAILED_LOGINS:
        del _FAILED_LOGINS[identifier]


def validate_registration_input(
    name: str,
    username: str,
    email: str,
    password: str,
    password_confirm: str
) -> Optional[str]:
    """Validate registration form fields. Returns error message or None if valid."""
    if not name or len(name.strip()) < 2:
        return "Please enter your full name (at least 2 characters)."
    if not username or len(username.strip()) < 3:
        return "Username must be at least 3 characters long."
    if not re.match(r"^[a-zA-Z0-9_.-]+$", username.strip()):
        return "Username may only contain letters, numbers, underscores, dots, or dashes."
    if not email or not re.match(r"^[^@]+@[^@]+\.[^@]+$", email.strip()):
        return "Please enter a valid email address."
    if not password or len(password) < 6:
        return "Password must be at least 6 characters long."
    if password != password_confirm:
        return "Passwords do not match."
    return None


def register_user(
    db: Session,
    name: str,
    username: str,
    email: str,
    password: str,
    level: str = "Beginner",
    goal: str = "Master Python for Marwadi University Course 01AP0303 and Practical Engineering"
) -> Tuple[User, Learner]:
    """
    Create a new user account with Argon2id password hashing and initialize
    their learner profile. Enforces duplicate account prevention.
    """
    clean_username = username.strip().lower()
    clean_email = email.strip().lower()
    clean_name = name.strip()

    # Duplicate check
    existing_user = db.query(User).filter(
        (User.username.ilike(clean_username)) | (User.email.ilike(clean_email))
    ).first()
    if existing_user:
        if existing_user.username.lower() == clean_username:
            raise ValueError("This username is already taken. Please choose another.")
        else:
            raise ValueError("An account with this email address already exists.")

    password_hash = hash_password(password)

    user = User(
        username=clean_username,
        email=clean_email,
        password_hash=password_hash,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    learner = create_learner_for_user(
        db=db,
        user_id=user.id,
        name=clean_name,
        level=level,
        goal=goal
    )
    return user, learner


def authenticate_user(db: Session, identifier: str, password: str) -> Optional[User]:
    """
    Authenticate against persisted account records.
    Supports either username or email as the identifier.
    Applies rate limiting check.
    """
    clean_id = identifier.strip().lower()
    if is_rate_limited(clean_id):
        raise ValueError("Too many failed login attempts. Please wait 5 minutes before trying again.")

    user = db.query(User).filter(
        ((User.username.ilike(clean_id)) | (User.email.ilike(clean_id))) &
        (User.is_active == True)
    ).first()

    if not user or not verify_password(user.password_hash, password):
        record_failed_attempt(clean_id)
        return None

    reset_failed_attempts(clean_id)
    return user


def create_session(db: Session, user_id: int, duration_days: int = 14) -> str:
    """Generate a cryptographically secure session token and persist to SQLite."""
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=duration_days)

    session = UserSession(
        session_token=token,
        user_id=user_id,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    return token


def invalidate_session(db: Session, session_token: str) -> bool:
    """Revoke a session in SQLite."""
    if not session_token:
        return False
    deleted = db.query(UserSession).filter(UserSession.session_token == session_token).delete()
    db.commit()
    return deleted > 0


def cleanup_expired_sessions(db: Session) -> int:
    """Remove expired sessions from the database."""
    deleted = db.query(UserSession).filter(UserSession.expires_at < utc_now()).delete()
    db.commit()
    return deleted


def set_user_session_storage(token: str, user_id: int):
    """Store session token and user ID in NiceGUI encrypted user storage."""
    try:
        app.storage.user["session_token"] = token
        app.storage.user["user_id"] = user_id
    except Exception:
        pass


def clear_user_session_storage():
    """Clear NiceGUI encrypted user storage."""
    try:
        app.storage.user.clear()
    except Exception:
        pass


def get_current_session_token() -> Optional[str]:
    """Retrieve session token from current NiceGUI user context."""
    try:
        return app.storage.user.get("session_token")
    except Exception:
        return None


def get_current_user_and_learner(db: Session) -> Optional[Tuple[User, Learner]]:
    """
    Authoritative server-side session validation.
    Validates session token against SQLite user_sessions table, checks expiration,
    and returns (User, Learner). If invalid or expired, clears user storage and returns None.
    """
    token = get_current_session_token()
    if not token:
        return None

    # Check session in database
    session_rec = db.query(UserSession).filter(
        UserSession.session_token == token
    ).first()

    if not session_rec:
        clear_user_session_storage()
        return None

    # Verify expiration (handle both naive and timezone-aware)
    now = datetime.now(timezone.utc)
    exp = session_rec.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)

    if exp <= now:
        db.delete(session_rec)
        db.commit()
        clear_user_session_storage()
        return None

    user = db.query(User).filter(
        User.id == session_rec.user_id,
        User.is_active == True
    ).first()

    if not user:
        db.delete(session_rec)
        db.commit()
        clear_user_session_storage()
        return None

    learner = get_learner_by_user_id(db, user.id)
    if not learner:
        # Auto-create bound learner if missing
        learner = create_learner_for_user(db, user.id, name=user.username)

    return user, learner
