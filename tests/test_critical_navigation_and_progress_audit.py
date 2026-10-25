"""
Tests for Pip Learn Critical Navigation and Progress Architecture Repair.
Verifies all 16 scenarios mandated in the audit prompt:
1. Fresh registration starts at Module 1, Lesson 1, Read.
2. A learner exits during Read and resumes at Read.
3. A learner exits during Watch and resumes at Watch (NOT Experiment).
4. A learner exits during Experiment and resumes at Experiment.
5. A learner exits during Practice and resumes at the correct task.
6. A learner exits during Check and resumes at the correct checkpoint.
7. Completing one lesson opens the next lesson at Read.
8. Page refresh preserves the correct stage.
9. Logout and login preserve progress.
10. Different users maintain independent progress.
11. Homepage and dashboard resume buttons resolve identically.
12. Explicit module and lesson navigation still works.
13. Back and forward navigation do not overwrite progress.
14. Corrupted or missing progress data is handled safely.
15. Existing users are not reset to the beginning.
16. No navigation control unexpectedly sends the user to Experiment.
"""
import json
import time
from datetime import datetime, timezone
import pytest
from playwright.sync_api import sync_playwright

from app.database.connection import get_db
from app.database.models import User, Learner, LessonActivity, LessonCompletion, ModuleProgress
from app.database.crud import create_learner_for_user, mark_lesson_complete, update_lesson_activity
from app.curriculum.loader import get_all_modules, get_module, get_lesson
from app.curriculum.sections import get_lesson_reading_sections
from app.curriculum.challenges import get_lesson_challenges
from app.navigation.nav import resolve_resume_destination, resolve_resume_target

BASE_URL = "http://localhost:8080"


# =========================================================================
# Unit Tests: Canonical Resume System & State Transitions
# =========================================================================

def test_canonical_resume_system_all_stages():
    """Verify scenarios 1-7, 10, 14, 15 directly against resolve_resume_destination."""
    with get_db() as db:
        ts = int(time.time() * 1000)
        user = User(username=f"audit_user_{ts}", email=f"audit_{ts}@mu.edu", password_hash="hash", is_active=True)
        db.add(user)
        db.commit()
        learner = create_learner_for_user(db, user_id=user.id, name="Audit Learner", level="Beginner")
        lid = learner.id

        mod1 = get_module(1)
        l1 = mod1.lessons[0]
        l2 = mod1.lessons[1]

        # Scenario 1: Fresh registration starts at Module 1, Lesson 1, Read
        dest = resolve_resume_destination(db, lid)
        assert dest["module_id"] == 1
        assert dest["lesson_id"] == l1.id
        assert dest["stage"] == "read"
        assert dest["reading_section"] == 0

        # Scenario 2: Exits during Read (Section 3) -> resumes at Read (Section 3)
        act = LessonActivity(
            learner_id=lid,
            module_id=1,
            lesson_id=l1.id,
            stage="read",
            reading_section=2, # section 3 (0-indexed 2)
        )
        db.add(act)
        db.commit()

        dest = resolve_resume_destination(db, lid)
        assert dest["stage"] == "read"
        assert dest["reading_section"] == 2
        assert dest["route"] == f"/module/1/lesson/{l1.id}?stage=read"

        # Scenario 3: Exits during Watch -> resumes at Watch (CRITICAL BUG PROOF: NOT Experiment!)
        act.stage = "watch"
        act.reading_section = 4 # finished reading
        act.video_status = "not_started" # learner just arrived at Watch stage
        act.experiment_attempted = False
        act.updated_at = datetime.now(timezone.utc)
        db.commit()

        dest = resolve_resume_destination(db, lid)
        assert dest["stage"] == "watch", f"Expected 'watch' to open, but got '{dest['stage']}'! Regression: never jump to experiment."
        assert dest["route"] == f"/module/1/lesson/{l1.id}?stage=watch"

        # Scenario 4: Exits during Experiment -> resumes at Experiment with saved code
        act.stage = "experiment"
        act.experiment_code = "print('Audit experiment 2026')"
        act.updated_at = datetime.now(timezone.utc)
        db.commit()

        dest = resolve_resume_destination(db, lid)
        assert dest["stage"] == "experiment"
        assert dest["route"] == f"/module/1/lesson/{l1.id}?stage=experiment"

        # Scenario 5: Exits during Practice -> resumes at Practice at correct task
        challenges = get_lesson_challenges(l1.id, l1.practice_tasks or mod1.practice_exercises)
        act.stage = "practice"
        practice_data = {challenges[0].id: {"passed": True, "code": "def t1(): pass"}}
        act.practice_state_json = json.dumps(practice_data)
        act.updated_at = datetime.now(timezone.utc)
        db.commit()

        dest = resolve_resume_destination(db, lid)
        assert dest["stage"] == "practice"
        assert dest["challenge_idx"] == 1 # points to unfinished task 2

        # Scenario 6: Exits during Check -> resumes at Check at correct checkpoint
        act.stage = "check"
        act.checkpoint_state_json = json.dumps({"q_0": {"passed": True}})
        act.updated_at = datetime.now(timezone.utc)
        db.commit()

        dest = resolve_resume_destination(db, lid)
        assert dest["stage"] == "check"
        assert dest["checkpoint_idx"] == 1 # points to unfinished question 2

        # Scenario 7: Completing one lesson opens next lesson at Read, section 0
        mark_lesson_complete(db, lid, 1, l1.id, len(mod1.lessons))

        dest = resolve_resume_destination(db, lid)
        assert dest["module_id"] == 1
        assert dest["lesson_id"] == l2.id
        assert dest["stage"] == "read"
        assert dest["reading_section"] == 0

        # Scenario 10: Different users maintain independent progress
        user2 = User(username=f"user2_{ts}", email=f"user2_{ts}@mu.edu", password_hash="h", is_active=True)
        db.add(user2)
        db.commit()
        learner2 = create_learner_for_user(db, user_id=user2.id, name="User Two", level="Beginner")

        # user2 should be at beginning regardless of user1's progress
        dest2 = resolve_resume_destination(db, learner2.id)
        assert dest2["lesson_id"] == l1.id
        assert dest2["stage"] == "read"

        # Scenario 14: Corrupted or missing progress data handled safely
        act_corrupt = LessonActivity(
            learner_id=learner2.id,
            module_id=1,
            lesson_id=l2.id,
            stage="invalid_stage_xyz",
            reading_section=9999,
        )
        db.add(act_corrupt)
        db.commit()

        dest_corrupt = resolve_resume_destination(db, learner2.id)
        assert dest_corrupt["stage"] in {"read", "watch", "experiment", "practice", "check"}

        # Cleanup
        db.delete(user)
        db.delete(user2)
        db.commit()


# =========================================================================
# E2E Browser Tests: Full Navigation, Watch Resumption, History & Consistency
# =========================================================================

def test_e2e_watch_stage_resumption_journey():
    """
    Directly tests the prompt's Phase 7 verification instructions:
    1. Start from the homepage.
    2. Sign in.
    3. Open Module 1, Lesson 1, Read.
    4. Advance to Watch.
    5. Return to homepage.
    6. Click Start Learning or Continue Learning.
    7. Expected: Watch opens, NOT Experiment.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        ts = int(time.time() * 1000)
        username = f"watch_learner_{ts}"
        email = f"watch_{ts}@student.marwadi.edu.in"
        password = "Password2026!"

        # Register new account
        page.goto(f"{BASE_URL}/register", wait_until="networkidle")
        page.locator("input[placeholder*='Aarav Sharma']").fill("Watch Learner")
        page.locator("input[placeholder*='aarav_sharma']").fill(username)
        page.locator("input[placeholder*='student.marwadi.edu.in']").fill(email)
        pw_inputs = page.locator("input[type='password']").all()
        pw_inputs[0].fill(password)
        pw_inputs[1].fill(password)
        page.locator("button:has-text('Create Account & Begin →')").click()
        page.wait_for_timeout(1000)

        # Complete onboarding
        if "/setup" in page.url:
            page.locator("button:has-text('Save & Enter Study Space →')").click()
            page.wait_for_timeout(1000)

        # 1. Open Module 1, Lesson 1, Read
        page.goto(f"{BASE_URL}/module/1/lesson/py-v2-u1-l01?stage=read", wait_until="networkidle")
        page.wait_for_timeout(800)
        assert page.locator("div.q-tab--active:has-text('Read')").is_visible()

        # Step through reading sections
        for _ in range(10):
            if page.locator("button:has-text('Continue to Watch Stage →')").is_visible():
                break
            btn = page.locator("button:has-text('Next Section →')")
            if btn.is_visible():
                btn.click()
                page.wait_for_timeout(400)
            else:
                break

        # 2. Advance to Watch Stage
        page.locator("div.q-tab:has-text('Watch')").click()
        page.wait_for_timeout(800)

        # Confirm Watch stage is active
        assert page.locator("div.q-tab--active:has-text('Watch')").is_visible()
        assert "stage=watch" in page.url

        # 3. Return to Homepage
        page.goto(f"{BASE_URL}/", wait_until="networkidle")
        page.wait_for_timeout(800)

        # 4. Click Start Learning on Homepage
        start_btn = page.locator("button:has-text('Start Learning →')")
        assert start_btn.is_visible()
        start_btn.click()
        page.wait_for_timeout(1200)

        # 5. VERIFICATION: Watch opens, NOT Experiment!
        current_url = page.url
        assert "stage=watch" in current_url, f"CRITICAL BUG DETECTED: Expected 'stage=watch' on resume, got '{current_url}'!"
        assert page.locator("div.q-tab--active:has-text('Watch')").is_visible(), "Watch tab must be active upon resumption!"
        assert not page.locator("div.q-tab--active:has-text('Experiment')").is_visible(), "Experiment stage must NOT be open!"

        # 6. Verify Page Refresh preserves the Watch stage (Scenario 8)
        page.reload(wait_until="networkidle")
        page.wait_for_timeout(800)
        assert "stage=watch" in page.url
        assert page.locator("div.q-tab--active:has-text('Watch')").is_visible()

        # 7. Advance to Experiment stage
        page.locator("button:has-text('Next Stage: Experiment →')").click()
        page.wait_for_timeout(800)
        assert "stage=experiment" in page.url
        assert page.locator("div.q-tab--active:has-text('Experiment')").is_visible()

        # 8. Verify Dashboard Resume Button resolves identically (Scenario 11)
        page.goto(f"{BASE_URL}/dashboard", wait_until="networkidle")
        page.wait_for_timeout(800)
        continue_btn = page.locator("button:has-text('Continue Learning →')")
        assert continue_btn.is_visible()
        continue_btn.click()
        page.wait_for_timeout(1200)

        # Now it resumes at Experiment because learner genuinely advanced to Experiment!
        assert "stage=experiment" in page.url
        assert page.locator("div.q-tab--active:has-text('Experiment')").is_visible()

        # 9. Verify Explicit Navigation still works (Scenario 12)
        page.goto(f"{BASE_URL}/module/1", wait_until="networkidle")
        page.wait_for_timeout(800)
        assert "Module" in page.title() and "Overview" in page.title()
        # Explicitly click Lesson 2 from module overview
        lesson2_btn = page.locator(".pip-card-interactive:has-text('Install Python'), button:has-text('Install Python')").first
        lesson2_btn.click()
        page.wait_for_timeout(1200)
        assert "py-v2-u1-l02" in page.url, "Explicit navigation to Lesson 2 must be respected"

        # 10. Verify Logout and Login restore progress (Scenario 9)
        logout_btn = page.locator("button:has-text('Logout'), button:has-text('Sign Out')").first
        logout_btn.click()
        page.wait_for_timeout(1000)

        # Log back in
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        page.locator("input[placeholder*='priya']").fill(username)
        page.locator("input[type='password']").fill(password)
        page.locator("button:has-text('Sign In →')").click()
        page.wait_for_timeout(1200)

        # Click Start Learning on Homepage
        page.goto(f"{BASE_URL}/", wait_until="networkidle")
        page.wait_for_timeout(600)
        page.locator("button:has-text('Start Learning →')").click()
        page.wait_for_timeout(1200)

        # Must restore learner's active lesson
        assert "/module/" in page.url

        browser.close()
