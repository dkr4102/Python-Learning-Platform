"""
Database connection and session handling.
"""
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import DATABASE_URL, DB_PATH
from app.database.models import Base

# Create SQLite engine with foreign key support enabled
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
_schema_ready = False

def init_db():
    """Create tables if they don't already exist and safely migrate legacy columns."""
    from sqlalchemy import text
    from argon2 import PasswordHasher
    from datetime import datetime, timezone
    import shutil

    global _schema_ready
    Base.metadata.create_all(bind=engine)

    # Namespace historical progress before changing lesson meanings. Back up
    # the SQLite file once, immediately before the first curriculum migration.
    with engine.connect() as conn:
        versioned_tables = [
            "module_progress", "lesson_completions", "lesson_activities",
            "quiz_attempts", "practice_attempts", "project_submissions",
        ]
        needs_curriculum_migration = any(
            "curriculum_version" not in [r[1] for r in conn.execute(text(f"PRAGMA table_info({table});")).fetchall()]
            for table in versioned_tables
        )
        if needs_curriculum_migration and DB_PATH.exists():
            backup = DB_PATH.with_name(f"{DB_PATH.name}.pre_curriculum_2026_1.bak")
            if not backup.exists():
                shutil.copy2(DB_PATH, backup)

        for table in versioned_tables:
            columns = [r[1] for r in conn.execute(text(f"PRAGMA table_info({table});")).fetchall()]
            if "curriculum_version" not in columns:
                conn.execute(text(
                    f"ALTER TABLE {table} ADD COLUMN curriculum_version VARCHAR(20) "
                    "NOT NULL DEFAULT 'legacy-v1';"
                ))
        conn.commit()

        # New module-progress rows start at zero; legacy percentages are kept
        # for audit/history and are never reinterpreted as 2026.1 completion.
        learner_ids = [row[0] for row in conn.execute(text("SELECT id FROM learners")).fetchall()]
        for learner_id in learner_ids:
            for module_id in range(1, 9):
                exists = conn.execute(text(
                    "SELECT 1 FROM module_progress WHERE learner_id=:lid AND module_id=:mid "
                    "AND curriculum_version='2026.1' LIMIT 1"
                ), {"lid": learner_id, "mid": module_id}).fetchone()
                if not exists:
                    conn.execute(text(
                        "INSERT INTO module_progress "
                        "(learner_id,module_id,curriculum_version,status,completion_percentage,last_accessed) "
                        "VALUES (:lid,:mid,'2026.1','not_started',0.0,:now)"
                    ), {"lid": learner_id, "mid": module_id, "now": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")})
        conn.commit()

        # Migrate columns on learners table if missing.
        res = conn.execute(text("PRAGMA table_info(learners);")).fetchall()
        col_names = [r[1] for r in res]
        if "user_id" not in col_names:
            conn.execute(text("ALTER TABLE learners ADD COLUMN user_id INTEGER REFERENCES users(id);"))
        if "onboarding_completed" not in col_names:
            conn.execute(text("ALTER TABLE learners ADD COLUMN onboarding_completed BOOLEAN DEFAULT 0;"))
        conn.commit()

        # Ensure default demo learner exists (for tests and immediate local exploration)
        user_res = conn.execute(text("SELECT id FROM users WHERE username = 'priya';")).fetchone()
        if not user_res:
            ph = PasswordHasher()
            pwd_hash = ph.hash("Priya123!")
            now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                text("INSERT INTO users (username, email, password_hash, is_active, created_at, updated_at) "
                     "VALUES ('priya', 'priya.patel@marwadi.edu.in', :hash, 1, :now, :now);"),
                {"hash": pwd_hash, "now": now_str}
            )
            user_id = conn.execute(text("SELECT last_insert_rowid();")).scalar()
            learner_exists = conn.execute(text("SELECT id FROM learners WHERE user_id = :uid;"), {"uid": user_id}).fetchone()
            if not learner_exists:
                conn.execute(
                    text("INSERT INTO learners (user_id, name, level, goal, onboarding_completed, created_at, updated_at) "
                         "VALUES (:uid, 'Dr. Priya Patel', 'Beginner', 'Master Python for MU 01AP0303', 1, :now, :now);"),
                    {"uid": user_id, "now": now_str}
                )
            conn.commit()
        else:
            user_id = user_res[0]
            # Link legacy unlinked learners if any
            res_legacy = conn.execute(text("SELECT id, name FROM learners WHERE user_id IS NULL;")).fetchall()
            for row in res_legacy:
                learner_id = row[0]
                conn.execute(
                    text("UPDATE learners SET user_id = :uid, onboarding_completed = 1 WHERE id = :lid;"),
                    {"uid": user_id, "lid": learner_id}
                )
            conn.commit()

    _schema_ready = True

@contextmanager
def get_db():
    """Provide a transactional scope around a series of operations."""
    if not _schema_ready:
        init_db()
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
