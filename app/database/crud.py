"""
CRUD operations and persistence helpers for Pip Learn.
"""
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.database.models import (
    Learner,
    ModuleProgress,
    LessonCompletion,
    QuizAttempt,
    PracticeAttempt,
    ProjectSubmission,
    Achievement,
    LessonActivity,
)

ACTIVE_CURRICULUM_VERSION = "2026.1"

DEFAULT_ACHIEVEMENTS = [
    {
        "code": "FIRST_STEP",
        "title": "First Step",
        "description": "Completed your first interactive Python lesson in Pip Learn.",
        "badge_icon": "emoji_nature"
    },
    {
        "code": "CODE_CRAFTER",
        "title": "Code Crafter",
        "description": "Successfully validated an exercise in the Practice Lab.",
        "badge_icon": "auto_awesome"
    },
    {
        "code": "CALCULATOR_CREATOR",
        "title": "Calculator Creator",
        "description": "Completed the Smart Calculator mini-project in Module 1.",
        "badge_icon": "calculate"
    },
    {
        "code": "CONTROL_MASTER",
        "title": "Control Master",
        "description": "Mastered logic, loops and functions with the Payroll System.",
        "badge_icon": "tune"
    },
    {
        "code": "DATA_ARCHITECT",
        "title": "Data Architect",
        "description": "Built the Inventory Tracker using Python data structures.",
        "badge_icon": "inventory_2"
    },
    {
        "code": "EXCEPTION_SHIELD",
        "title": "Exception Shield",
        "description": "Constructed robust error handling with the Log File Analyzer.",
        "badge_icon": "verified_user"
    },
    {
        "code": "OOP_VIRTUOSO",
        "title": "OOP Virtuoso",
        "description": "Modeled real-world finance with the Banking Account Management System.",
        "badge_icon": "account_balance"
    },
    {
        "code": "SQL_BRIDGE",
        "title": "Database Artisan",
        "description": "Bridged Python and SQLite with the Customer Record Management Application.",
        "badge_icon": "storage"
    },
    {
        "code": "API_NAVIGATOR",
        "title": "API Navigator",
        "description": "Integrated web services with the Weather Dashboard & Automation Tool.",
        "badge_icon": "cloud_sync"
    },
    {
        "code": "ANALYTICS_EXPLORER",
        "title": "Analytics Explorer",
        "description": "Generated insightful charts and statistics with the Sales Analytics Dashboard.",
        "badge_icon": "insights"
    },
    {
        "code": "ACADEMIC_SCHOLAR",
        "title": "MU 01AP0303 Scholar",
        "description": "Completed all 8 syllabus units with verified internal assessment criteria.",
        "badge_icon": "military_tech"
    }
]


def get_learner_by_user_id(db: Session, user_id: int) -> Optional[Learner]:
    """Retrieve learner associated with a specific authenticated user."""
    return db.query(Learner).filter(Learner.user_id == user_id).first()


def create_learner_for_user(
    db: Session,
    user_id: int,
    name: str,
    level: str = "Beginner",
    goal: str = "Master Python for Marwadi University Course 01AP0303 and Practical Engineering"
) -> Learner:
    """Create a new learner profile bound to an authenticated user and initialize 8 modules."""
    learner = Learner(
        user_id=user_id,
        name=name.strip() if name else "Python Learner",
        level=level,
        goal=goal,
        onboarding_completed=False,
    )
    db.add(learner)
    db.commit()
    db.refresh(learner)

    for m_id in range(1, 9):
        prog = ModuleProgress(
            learner_id=learner.id,
            module_id=m_id,
            status="not_started",
            completion_percentage=0.0
        )
        db.add(prog)
    db.commit()
    return learner


def reset_learner_course_progress(db: Session, learner_id: int) -> bool:
    """Destructively reset all progress, attempts, submissions, and achievements for a learner."""
    db.query(LessonActivity).filter(LessonActivity.learner_id == learner_id).delete()
    db.query(LessonCompletion).filter(LessonCompletion.learner_id == learner_id).delete()
    db.query(QuizAttempt).filter(QuizAttempt.learner_id == learner_id).delete()
    db.query(PracticeAttempt).filter(PracticeAttempt.learner_id == learner_id).delete()
    db.query(ProjectSubmission).filter(ProjectSubmission.learner_id == learner_id).delete()
    db.query(Achievement).filter(Achievement.learner_id == learner_id).delete()

    # Reset 8 modules
    modules = db.query(ModuleProgress).filter(ModuleProgress.learner_id == learner_id).all()
    for m in modules:
        m.status = "not_started"
        m.completion_percentage = 0.0
        m.last_accessed = datetime.now(timezone.utc)
    db.commit()
    return True


def get_default_learner(db: Session) -> Learner:
    """Fallback learner retrieval for backward compatibility."""
    learner = db.query(Learner).first()
    if not learner:
        learner = Learner(
            name="Aarav Sharma",
            level="Beginner",
            goal="Master Python for Marwadi University Course 01AP0303 and Practical Engineering"
        )
        db.add(learner)
        db.commit()
        db.refresh(learner)

        # Initialize progress for 8 modules
        for m_id in range(1, 9):
            prog = ModuleProgress(
                learner_id=learner.id,
                module_id=m_id,
                status="not_started",
                completion_percentage=0.0
            )
            db.add(prog)
        db.commit()
    return learner


def get_lesson_activity(db: Session, learner_id: int, module_id: int, lesson_id: str) -> LessonActivity:
    activity = db.query(LessonActivity).filter(
        LessonActivity.learner_id == learner_id,
        LessonActivity.module_id == module_id,
        LessonActivity.lesson_id == lesson_id,
        LessonActivity.curriculum_version == ACTIVE_CURRICULUM_VERSION,
    ).first()
    if not activity:
        activity = LessonActivity(
            learner_id=learner_id,
            module_id=module_id,
            lesson_id=lesson_id,
            curriculum_version=ACTIVE_CURRICULUM_VERSION,
        )
        db.add(activity)
        db.commit()
        db.refresh(activity)
    return activity


def update_lesson_activity(db: Session, activity_id: int, **changes) -> LessonActivity:
    """Persist only known activity fields; reaching a stage never grants completion."""
    activity = db.query(LessonActivity).filter(LessonActivity.id == activity_id).first()
    if not activity:
        raise ValueError("Lesson activity not found")
    allowed = {
        "stage", "reading_section", "video_status", "notes", "experiment_code",
        "experiment_attempted", "practice_state_json", "checkpoint_state_json",
    }
    for key, value in changes.items():
        if key in allowed:
            setattr(activity, key, value)
    activity.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(activity)
    return activity


def update_learner_profile(
    db: Session,
    learner_id: int,
    name: str,
    level: str,
    goal: str,
    onboarding_completed: Optional[bool] = None
) -> Learner:
    learner = db.query(Learner).filter(Learner.id == learner_id).first()
    if learner:
        learner.name = name
        learner.level = level
        learner.goal = goal
        if onboarding_completed is not None:
            learner.onboarding_completed = onboarding_completed
        learner.updated_at = datetime.now(timezone.utc)
        db.commit()
        db.refresh(learner)
    return learner


def mark_lesson_complete(db: Session, learner_id: int, module_id: int, lesson_id: str, total_module_lessons: int) -> bool:
    """Record lesson completion and update module progress percentage."""
    existing = db.query(LessonCompletion).filter(
        LessonCompletion.learner_id == learner_id,
        LessonCompletion.module_id == module_id,
        LessonCompletion.lesson_id == lesson_id,
        LessonCompletion.curriculum_version == ACTIVE_CURRICULUM_VERSION,
    ).first()

    if not existing:
        completion = LessonCompletion(
            learner_id=learner_id,
            module_id=module_id,
            lesson_id=lesson_id,
            curriculum_version=ACTIVE_CURRICULUM_VERSION,
        )
        db.add(completion)
        db.commit()

        # Unlock First Step achievement
        unlock_achievement(db, learner_id, "FIRST_STEP")

    # Recalculate module progress
    recalculate_module_progress(db, learner_id, module_id, total_module_lessons)
    return True


def recalculate_module_progress(db: Session, learner_id: int, module_id: int, total_module_lessons: int):
    completed_lessons = db.query(LessonCompletion).filter(
        LessonCompletion.learner_id == learner_id,
        LessonCompletion.module_id == module_id,
        LessonCompletion.curriculum_version == ACTIVE_CURRICULUM_VERSION,
    ).count()

    quiz_passed = db.query(QuizAttempt).filter(
        QuizAttempt.learner_id == learner_id,
        QuizAttempt.module_id == module_id,
        QuizAttempt.curriculum_version == ACTIVE_CURRICULUM_VERSION,
        QuizAttempt.passed == True
    ).first() is not None

    completed_project_ids = {
        row[0] for row in db.query(ProjectSubmission.project_id).filter(
        ProjectSubmission.learner_id == learner_id,
        ProjectSubmission.module_id == module_id,
        ProjectSubmission.curriculum_version == ACTIVE_CURRICULUM_VERSION,
        ProjectSubmission.status == "completed"
        ).all()
    }
    from app.curriculum.loader import get_module
    curriculum_module = get_module(module_id)
    required_project_ids = {project.id for project in curriculum_module.projects} if curriculum_module else set()
    project_done = bool(required_project_ids) and required_project_ids <= completed_project_ids

    # Weighting: Lessons 50%, Quiz 25%, Project 25%
    lesson_pct = (completed_lessons / max(total_module_lessons, 1)) * 50.0
    quiz_pct = 25.0 if quiz_passed else 0.0
    project_pct = 25.0 if project_done else 0.0
    total_pct = min(round(lesson_pct + quiz_pct + project_pct, 1), 100.0)

    status = "not_started"
    if total_pct >= 95.0:
        status = "completed"
    elif total_pct > 0.0:
        status = "in_progress"

    progress = db.query(ModuleProgress).filter(
        ModuleProgress.learner_id == learner_id,
        ModuleProgress.module_id == module_id,
        ModuleProgress.curriculum_version == ACTIVE_CURRICULUM_VERSION,
    ).first()

    if not progress:
        progress = ModuleProgress(
            learner_id=learner_id,
            module_id=module_id,
            curriculum_version=ACTIVE_CURRICULUM_VERSION,
            status=status,
            completion_percentage=total_pct
        )
        db.add(progress)
    else:
        progress.status = status
        progress.completion_percentage = total_pct
        progress.last_accessed = datetime.now(timezone.utc)

    db.commit()

    # Check for overall completion
    all_completed = db.query(ModuleProgress).filter(
        ModuleProgress.learner_id == learner_id,
        ModuleProgress.curriculum_version == ACTIVE_CURRICULUM_VERSION,
        ModuleProgress.status == "completed"
    ).count()
    if all_completed >= 8:
        unlock_achievement(db, learner_id, "ACADEMIC_SCHOLAR")


def record_quiz_attempt(
    db: Session,
    learner_id: int,
    module_id: int,
    score: float,
    max_score: float,
    answers: Dict[str, Any],
    total_module_lessons: int
) -> QuizAttempt:
    percentage = (score / max(max_score, 1.0)) * 100.0
    passed = percentage >= 60.0

    attempt = QuizAttempt(
        learner_id=learner_id,
        module_id=module_id,
        curriculum_version=ACTIVE_CURRICULUM_VERSION,
        score=score,
        max_score=max_score,
        percentage=round(percentage, 1),
        passed=passed,
        answers_json=json.dumps(answers)
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    recalculate_module_progress(db, learner_id, module_id, total_module_lessons)
    return attempt


def record_practice_attempt(
    db: Session,
    learner_id: int,
    module_id: int,
    exercise_id: str,
    passed: bool,
    code_submitted: str,
    output_or_error: str
) -> PracticeAttempt:
    attempt = PracticeAttempt(
        learner_id=learner_id,
        module_id=module_id,
        exercise_id=exercise_id,
        curriculum_version=ACTIVE_CURRICULUM_VERSION,
        passed=passed,
        code_submitted=code_submitted,
        output_or_error=output_or_error
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    if passed:
        unlock_achievement(db, learner_id, "CODE_CRAFTER")
    return attempt


def record_project_submission(
    db: Session,
    learner_id: int,
    module_id: int,
    project_id: str,
    title: str,
    execution_result: str,
    total_module_lessons: int
) -> ProjectSubmission:
    submission = db.query(ProjectSubmission).filter(
        ProjectSubmission.learner_id == learner_id,
        ProjectSubmission.module_id == module_id,
        ProjectSubmission.project_id == project_id,
        ProjectSubmission.curriculum_version == ACTIVE_CURRICULUM_VERSION,
    ).first()

    if not submission:
        submission = ProjectSubmission(
            learner_id=learner_id,
            module_id=module_id,
            project_id=project_id,
            curriculum_version=ACTIVE_CURRICULUM_VERSION,
            title=title,
            status="completed",
            execution_result=execution_result
        )
        db.add(submission)
    else:
        submission.status = "completed"
        submission.execution_result = execution_result
        submission.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(submission)

    # Unlock module-specific project achievement
    achievement_keys = {
        1: "CALCULATOR_CREATOR",
        2: "CONTROL_MASTER",
        3: "DATA_ARCHITECT",
        4: "EXCEPTION_SHIELD",
        5: "OOP_VIRTUOSO",
        6: "SQL_BRIDGE",
        7: "API_NAVIGATOR",
        8: "ANALYTICS_EXPLORER"
    }
    if module_id in achievement_keys:
        unlock_achievement(db, learner_id, achievement_keys[module_id])

    recalculate_module_progress(db, learner_id, module_id, total_module_lessons)
    return submission


def unlock_achievement(db: Session, learner_id: int, code: str) -> Optional[Achievement]:
    existing = db.query(Achievement).filter(
        Achievement.learner_id == learner_id,
        Achievement.code == code
    ).first()
    if existing:
        return existing

    item = next((a for a in DEFAULT_ACHIEVEMENTS if a["code"] == code), None)
    if not item:
        return None

    ach = Achievement(
        learner_id=learner_id,
        code=code,
        title=item["title"],
        description=item["description"],
        badge_icon=item["badge_icon"]
    )
    db.add(ach)
    db.commit()
    db.refresh(ach)
    return ach


def get_learner_summary(db: Session, learner_id: int) -> Dict[str, Any]:
    learner = db.query(Learner).filter(Learner.id == learner_id).first()
    if not learner:
        return {}

    progress_list = db.query(ModuleProgress).filter(ModuleProgress.learner_id == learner_id, ModuleProgress.curriculum_version == ACTIVE_CURRICULUM_VERSION).all()
    completions = db.query(LessonCompletion).filter(LessonCompletion.learner_id == learner_id, LessonCompletion.curriculum_version == ACTIVE_CURRICULUM_VERSION).all()
    quiz_attempts = db.query(QuizAttempt).filter(QuizAttempt.learner_id == learner_id, QuizAttempt.curriculum_version == ACTIVE_CURRICULUM_VERSION).all()
    practice_attempts = db.query(PracticeAttempt).filter(PracticeAttempt.learner_id == learner_id, PracticeAttempt.curriculum_version == ACTIVE_CURRICULUM_VERSION).all()
    projects = db.query(ProjectSubmission).filter(ProjectSubmission.learner_id == learner_id, ProjectSubmission.curriculum_version == ACTIVE_CURRICULUM_VERSION).all()
    achievements = db.query(Achievement).filter(Achievement.learner_id == learner_id).all()

    overall_pct = 0.0
    if progress_list:
        overall_pct = round(sum(p.completion_percentage for p in progress_list) / 8.0, 1)

    completed_modules_count = sum(1 for p in progress_list if p.status == "completed")

    return {
        "learner": {
            "id": learner.id,
            "name": learner.name,
            "level": learner.level,
            "goal": learner.goal,
            "created_at": learner.created_at.strftime("%Y-%m-%d %H:%M")
        },
        "overall_percentage": overall_pct,
        "completed_modules_count": completed_modules_count,
        "total_lessons_completed": len(completions),
        "total_quizzes_taken": len(quiz_attempts),
        "total_quizzes_passed": sum(1 for q in quiz_attempts if q.passed),
        "total_practice_runs": len(practice_attempts),
        "total_practice_passed": sum(1 for p in practice_attempts if p.passed),
        "total_projects_completed": len(projects),
        "achievements_count": len(achievements),
        "module_progress": {p.module_id: {"status": p.status, "pct": p.completion_percentage} for p in progress_list},
        "achievements": [{"code": a.code, "title": a.title, "description": a.description, "icon": a.badge_icon} for a in achievements]
    }
