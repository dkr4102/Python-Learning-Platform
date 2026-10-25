"""
SQLAlchemy models for learner progress, assessments, practice and projects.
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

def utc_now():
    return datetime.now(timezone.utc)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    learner = relationship("Learner", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_token = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="sessions")


class Learner(Base):
    __tablename__ = "learners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, unique=True)
    name = Column(String(100), default="Python Learner", nullable=False)
    level = Column(String(50), default="Beginner", nullable=False)
    goal = Column(String(200), default="Master Python for Academic and Real-World Excellence")
    onboarding_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="learner")
    module_progress = relationship("ModuleProgress", back_populates="learner", cascade="all, delete-orphan")
    lesson_completions = relationship("LessonCompletion", back_populates="learner", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="learner", cascade="all, delete-orphan")
    practice_attempts = relationship("PracticeAttempt", back_populates="learner", cascade="all, delete-orphan")
    project_submissions = relationship("ProjectSubmission", back_populates="learner", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="learner", cascade="all, delete-orphan")
    lesson_activities = relationship("LessonActivity", back_populates="learner", cascade="all, delete-orphan")


class ModuleProgress(Base):
    __tablename__ = "module_progress"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    module_id = Column(Integer, nullable=False)  # 1 to 8
    curriculum_version = Column(String(20), default="2026.1", nullable=False)
    status = Column(String(30), default="not_started")  # not_started, in_progress, completed
    completion_percentage = Column(Float, default=0.0)
    last_accessed = Column(DateTime, default=utc_now)

    learner = relationship("Learner", back_populates="module_progress")


class LessonCompletion(Base):
    __tablename__ = "lesson_completions"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    module_id = Column(Integer, nullable=False)
    lesson_id = Column(String(50), nullable=False)
    curriculum_version = Column(String(20), default="2026.1", nullable=False)
    completed_at = Column(DateTime, default=utc_now)

    learner = relationship("Learner", back_populates="lesson_completions")


class LessonActivity(Base):
    """Durable work-in-progress state; navigation is not completion."""
    __tablename__ = "lesson_activities"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    module_id = Column(Integer, nullable=False)
    lesson_id = Column(String(50), nullable=False)
    curriculum_version = Column(String(20), default="2026.1", nullable=False)
    stage = Column(String(20), default="read")
    reading_section = Column(Integer, default=0)
    video_status = Column(String(30), default="not_started")
    notes = Column(Text, default="")
    experiment_code = Column(Text, default="")
    experiment_attempted = Column(Boolean, default=False)
    practice_state_json = Column(Text, default="{}")
    checkpoint_state_json = Column(Text, default="{}")
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    learner = relationship("Learner", back_populates="lesson_activities")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    module_id = Column(Integer, nullable=False)
    curriculum_version = Column(String(20), default="2026.1", nullable=False)
    score = Column(Float, nullable=False)
    max_score = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    passed = Column(Boolean, default=False)
    answers_json = Column(Text, default="{}")
    attempted_at = Column(DateTime, default=utc_now)

    learner = relationship("Learner", back_populates="quiz_attempts")


class PracticeAttempt(Base):
    __tablename__ = "practice_attempts"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    module_id = Column(Integer, nullable=False)
    exercise_id = Column(String(50), nullable=False)
    curriculum_version = Column(String(20), default="2026.1", nullable=False)
    passed = Column(Boolean, default=False)
    code_submitted = Column(Text, default="")
    output_or_error = Column(Text, default="")
    attempted_at = Column(DateTime, default=utc_now)

    learner = relationship("Learner", back_populates="practice_attempts")


class ProjectSubmission(Base):
    __tablename__ = "project_submissions"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    module_id = Column(Integer, nullable=False)
    project_id = Column(String(50), nullable=False)
    curriculum_version = Column(String(20), default="2026.1", nullable=False)
    title = Column(String(100), nullable=False)
    status = Column(String(30), default="completed")  # in_progress, completed
    execution_result = Column(Text, default="")
    completed_at = Column(DateTime, default=utc_now)

    learner = relationship("Learner", back_populates="project_submissions")


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    learner_id = Column(Integer, ForeignKey("learners.id"), nullable=False)
    code = Column(String(50), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    badge_icon = Column(String(50), default="school")
    unlocked_at = Column(DateTime, default=utc_now)

    learner = relationship("Learner", back_populates="achievements")
