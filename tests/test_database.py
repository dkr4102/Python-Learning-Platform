"""
Tests for SQLite persistence, learner progression, assessment scoring, and achievement unlocks.
"""
import pytest
from app.database.connection import get_db, init_db
from app.database.crud import (
    get_default_learner,
    update_learner_profile,
    mark_lesson_complete,
    record_quiz_attempt,
    record_practice_attempt,
    record_project_submission,
    get_learner_summary,
    get_lesson_activity,
    update_lesson_activity,
)

@pytest.fixture(autouse=True)
def setup_test_db():
    init_db()

def test_learner_initialization():
    with get_db() as db:
        learner = get_default_learner(db)
        assert learner is not None
        assert learner.id > 0
        assert learner.name != ""

def test_learner_profile_update():
    with get_db() as db:
        learner = get_default_learner(db)
        updated = update_learner_profile(db, learner.id, "Dr. Priya Patel", "Intermediate", "Pass 01AP0303 with distinction")
        assert updated.name == "Dr. Priya Patel"
        assert updated.level == "Intermediate"

def test_lesson_completion_and_achievement_unlock():
    with get_db() as db:
        learner = get_default_learner(db)
        success = mark_lesson_complete(db, learner.id, 1, "py-v2-u1-l01", 10)
        assert success is True

        summary = get_learner_summary(db, learner.id)
        assert summary["total_lessons_completed"] >= 1
        ach_codes = [a["code"] for a in summary["achievements"]]
        assert "FIRST_STEP" in ach_codes

def test_quiz_attempt_scoring():
    with get_db() as db:
        learner = get_default_learner(db)
        attempt = record_quiz_attempt(
            db,
            learner.id,
            1,
            score=4.0,
            max_score=5.0,
            answers={"m1-q1": {"is_correct": True}},
            total_module_lessons=10
        )
        assert attempt.score == 4.0
        assert attempt.percentage == 80.0
        assert attempt.passed is True

def test_practice_attempt_and_project_submission():
    with get_db() as db:
        learner = get_default_learner(db)
        p_att = record_practice_attempt(db, learner.id, 1, "m1-ex1", True, "celsius = 37.0", "37.0 C = 98.6 F")
        assert p_att.passed is True

        proj = record_project_submission(db, learner.id, 1, "proj-smart-calc", "Smart Calculator", "25 + 5 = 30", 5)
        assert proj.status == "completed"

        summary = get_learner_summary(db, learner.id)
        ach_codes = [a["code"] for a in summary["achievements"]]
        assert "CALCULATOR_CREATOR" in ach_codes


def test_lesson_activity_persists_without_completing_lesson():
    with get_db() as db:
        learner = get_default_learner(db)
        activity = get_lesson_activity(db, learner.id, 1, "py-v2-u1-l02")
        updated = update_lesson_activity(
            db,
            activity.id,
            stage="experiment",
            reading_section=2,
            experiment_code="score = 42\nprint(score)",
            experiment_attempted=True,
        )
        assert updated.stage == "experiment"
        assert updated.reading_section == 2
        assert updated.experiment_attempted is True
