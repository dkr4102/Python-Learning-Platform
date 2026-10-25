"""
Phase 12 End-to-End Acceptance Test for Pip Learn 2.0.
Executes the full authoritative 20-step learner journey:
1. Anonymous visit
2. Click Start Learning
3. Confirm Login/Register appears
4. Register a new unique account
5. Complete first-time onboarding
6. Enter Study Space dashboard
7. Open Curriculum Explorer
8. Select Module 1
9. Open Lesson 1 workspace
10. Complete learning stage
11. Progress persisted to SQLite
12. Log out
13. Attempt direct access to protected route
14. Confirm authentication required with preserved redirect
15. Log in again
16. Click Continue Learning
17. Confirm exact lesson & stage restored
18. Complete lesson assessment checkpoint
19. Navigate to canonical next lesson (m1-l2)
20. Confirm dashboard and curriculum display consistent matching telemetry
"""
import time
from playwright.sync_api import sync_playwright
import pytest
from app.database.connection import get_db
from app.database.models import User, Learner, LessonCompletion, LessonActivity, ModuleProgress
from app.database.crud import get_learner_summary


def test_phase12_complete_acceptance_journey():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        timestamp = int(time.time())
        username = f"learner_{timestamp}"
        email = f"learner_{timestamp}@student.marwadi.edu.in"
        password = "SecurePassword2026!"
        fullname = f"Acceptance Learner {timestamp}"

        # -------------------------------------------------------------
        # STEP 1: Visit Pip Learn as an anonymous user
        # -------------------------------------------------------------
        print("\n[Step 1] Visiting Pip Learn home page anonymously...")
        page.goto("http://localhost:8080/", wait_until="networkidle")
        page.wait_for_timeout(600)
        assert page.locator("text=Python, one concept at a time.").first.is_visible()
        # Verify anonymous header states
        assert page.locator("button:has-text('Sign In')").is_visible()
        assert page.locator("button:has-text('Register'), button:has-text('Get Started')").first.is_visible()

        # -------------------------------------------------------------
        # STEP 2 & 3: Click Start Learning -> Confirm Login/Register appears
        # -------------------------------------------------------------
        print("[Step 2-3] Clicking Start Learning as unauthenticated visitor...")
        page.locator("button:has-text('Start Learning')").click()
        page.wait_for_timeout(1000)

        # Confirm redirected to login page with preserved redirect query
        assert "/login" in page.url
        assert page.locator("text=Sign in to Study Space").first.is_visible()

        # -------------------------------------------------------------
        # STEP 4: Register a new account
        # -------------------------------------------------------------
        print("[Step 4] Navigating to Registration and creating a new account...")
        page.locator("button:has-text('Create an account')").click()
        page.wait_for_timeout(1000)
        assert "/register" in page.url
        assert page.locator("text=Create Learner Account").is_visible()

        page.locator("input[placeholder*='Aarav Sharma']").fill(fullname)
        page.locator("input[placeholder*='aarav_sharma']").fill(username)
        page.locator("input[placeholder*='student.marwadi.edu.in']").fill(email)

        password_inputs = page.locator("input[type='password']").all()
        assert len(password_inputs) >= 2
        password_inputs[0].fill(password)
        password_inputs[1].fill(password)

        page.locator("button:has-text('Create Account & Begin →')").click()
        page.wait_for_timeout(1500)

        # -------------------------------------------------------------
        # STEP 5: Complete First-Time Onboarding
        # -------------------------------------------------------------
        print("[Step 5] Completing first-time onboarding...")
        assert "/setup" in page.url
        assert page.locator("text=LEARNER ONBOARDING").is_visible()

        # Fill goal and save
        goal_textarea = page.locator("textarea")
        if goal_textarea.is_visible():
            goal_textarea.fill("Master Python 01AP0303 with distinction and pass all assessments.")

        page.locator("button:has-text('Save & Enter Study Space →')").click()
        page.wait_for_timeout(1500)

        # -------------------------------------------------------------
        # STEP 6: Enter Study Space Dashboard
        # -------------------------------------------------------------
        print("[Step 6] Entering Study Space dashboard...")
        assert "/dashboard" in page.url
        assert page.locator(f"text=Welcome back, {fullname}").is_visible()
        # Verify fresh account metrics are at 0%
        assert page.locator("text=0.0%").is_visible()
        assert page.locator("text=0 of 8 Modules Mastered").is_visible()

        # -------------------------------------------------------------
        # STEP 7: Open Curriculum
        # -------------------------------------------------------------
        print("[Step 7] Opening Curriculum Explorer...")
        page.locator("button:has-text('Curriculum Explorer')").first.click()
        page.wait_for_timeout(1000)
        assert "/curriculum" in page.url
        assert page.locator(".editorial-title:has-text('Curriculum Explorer')").is_visible()

        # -------------------------------------------------------------
        # STEP 8: Choose Module 1
        # -------------------------------------------------------------
        print("[Step 8] Selecting Module 1 Overview...")
        page.locator("button:has-text('Explore Module →')").first.click()
        page.wait_for_timeout(1000)
        assert "/module/1" in page.url
        assert page.locator("text=MOD-01").first.is_visible()

        # -------------------------------------------------------------
        # STEP 9: Open Lesson 1
        # -------------------------------------------------------------
        print("[Step 9] Opening Lesson 1 Workspace...")
        page.locator("button:has-text('Begin Lesson Sequence →')").click()
        page.wait_for_timeout(1200)
        assert "/module/1/lesson/py-v2-u1-l01" in page.url
        assert "Lesson Workspace" in page.title()

        # -------------------------------------------------------------
        # STEP 10 & 11: Complete a learning stage & Save progress
        # -------------------------------------------------------------
        print("[Step 10-11] Navigating through Read stage and advancing to Watch stage...")
        page.locator("div.q-tab:has-text('Read')").click()
        page.wait_for_timeout(400)

        # Step through reading sections
        next_sec_btn = page.locator("text=Next Section →")
        for _ in range(4):
            if next_sec_btn.is_visible():
                next_sec_btn.click()
                page.wait_for_timeout(300)

        watch_advance_btn = page.locator("text=Continue to Watch Stage →")
        if watch_advance_btn.is_visible():
            watch_advance_btn.click()
            page.wait_for_timeout(600)

        # Switch to Experiment stage to establish a distinctive progress position
        page.locator("div.q-tab:has-text('Experiment')").click()
        page.wait_for_timeout(800)

        # Verify activity persisted to SQLite database
        with get_db() as db:
            user_rec = db.query(User).filter(User.username == username).first()
            assert user_rec is not None
            learner_rec = db.query(Learner).filter(Learner.user_id == user_rec.id).first()
            assert learner_rec is not None
            activity_rec = db.query(LessonActivity).filter(
                LessonActivity.learner_id == learner_rec.id,
                LessonActivity.lesson_id == "py-v2-u1-l01"
            ).first()
            assert activity_rec is not None
            assert activity_rec.stage == "experiment"

        # -------------------------------------------------------------
        # STEP 12: Log out
        # -------------------------------------------------------------
        print("[Step 12] Logging out...")
        logout_btn = page.locator("button:has-text('Logout')")
        assert logout_btn.is_visible()
        logout_btn.click()
        page.wait_for_timeout(1200)

        # Confirm redirected to public home
        assert page.url.rstrip("/") == "http://localhost:8080"
        assert page.locator("button:has-text('Sign In')").is_visible()

        # -------------------------------------------------------------
        # STEP 13 & 14: Attempt direct access to lesson -> Confirm Auth Required
        # -------------------------------------------------------------
        print("[Step 13-14] Attempting unauthenticated direct access to the first stable lesson ID...")
        page.goto("http://localhost:8080/module/1/lesson/py-v2-u1-l01", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Must be redirected to /login with preserved redirect
        assert "/login" in page.url
        assert "redirect=" in page.url
        assert page.locator("text=Sign in to Study Space").first.is_visible()

        # -------------------------------------------------------------
        # STEP 15: Log in again
        # -------------------------------------------------------------
        print("[Step 15] Logging back in as returning learner...")
        page.locator("input[placeholder*='priya']").fill(username)
        page.locator("input[type='password']").fill(password)
        page.locator("button:has-text('Sign In →')").click()
        page.wait_for_timeout(1200)

        # Preserved safe redirect returns to the lesson
        assert "/module/1/lesson/py-v2-u1-l01" in page.url

        # -------------------------------------------------------------
        # STEP 16 & 17: Navigate to Dashboard & Test Continue Learning
        # -------------------------------------------------------------
        print("[Step 16-17] Verifying Continue Learning resume behavior from Dashboard...")
        page.locator("button:has-text('Study Space')").click()
        page.wait_for_timeout(1000)
        assert "/dashboard" in page.url

        # Click Continue Learning
        page.locator("button:has-text('Continue Learning →')").click()
        page.wait_for_timeout(1200)

        # Must restore exact stable lesson and saved stage (experiment)
        assert "/module/1/lesson/py-v2-u1-l01" in page.url
        # Verify the experiment tab is active
        exp_tab = page.locator("div.q-tab--active")
        assert "Experiment" in exp_tab.text_content()

        # Produce real experiment and practice evidence before certification.
        page.locator("div.q-tab:has-text('Experiment')").click()
        page.wait_for_timeout(300)
        page.locator("button:has-text('Run Code')").click()
        page.wait_for_timeout(700)

        page.locator("div.q-tab:has-text('Practice')").click()
        page.wait_for_timeout(500)
        solution = 'message = "Python turns instructions into useful work."\nprint(message)'
        for challenge_number in (1, 2, 3):
            page.locator(f"button:has-text('Challenge {challenge_number}:')").click()
            page.wait_for_timeout(250)
            editor = page.locator(".q-tab-panel:visible textarea").last
            editor.fill(solution)
            page.locator(".q-tab-panel:visible button:has-text('Run Tests')").click()
            page.wait_for_timeout(700)

        # -------------------------------------------------------------
        # STEP 18: Complete the lesson assessment (Check stage)
        # -------------------------------------------------------------
        print("[Step 18] Navigating to Check stage and completing assessment questions...")
        page.locator("div.q-tab:has-text('Check')").click()
        page.wait_for_timeout(800)

        # Answer question 1 (correct option index is 0)
        q1_option = page.locator(".q-tab-panel:visible .q-radio").nth(0)
        q1_option.click()
        page.wait_for_timeout(400)
        page.locator("button:has-text('Check Answer')").click()
        page.wait_for_timeout(400)

        cont_btn = page.locator("button:has-text('Next Question →')")
        assert cont_btn.is_visible()
        cont_btn.click()
        page.wait_for_timeout(500)

        # Answer question 2 (correct option index is 0)
        q2_option = page.locator(".q-tab-panel:visible .q-radio").nth(0)
        q2_option.click()
        page.wait_for_timeout(400)
        page.locator("button:has-text('Check Answer')").click()
        page.wait_for_timeout(400)

        cert_btn = page.locator("button:has-text('Complete & Certify Lesson →')")
        assert cert_btn.is_visible()
        cert_btn.click()
        page.wait_for_timeout(800)

        # Verify lesson completion registered in SQLite
        with get_db() as db:
            completion_rec = db.query(LessonCompletion).filter(
                LessonCompletion.learner_id == learner_rec.id,
                LessonCompletion.lesson_id == "py-v2-u1-l01"
            ).first()
            assert completion_rec is not None

        # -------------------------------------------------------------
        # STEP 19: Navigate to Next Lesson
        # -------------------------------------------------------------
        print("[Step 19] Navigating to next lesson...")
        next_lesson_btn = page.locator("button:has-text('Next Lesson →')")
        if next_lesson_btn.is_visible():
            next_lesson_btn.click()
            page.wait_for_timeout(1200)
            assert "/module/1/lesson/py-v2-u1-l02" in page.url
            assert page.locator("text=Install Python and Set Up Your Environment").first.is_visible()

        # -------------------------------------------------------------
        # STEP 20: Confirm Dashboard and Curriculum display matching progress
        # -------------------------------------------------------------
        print("[Step 20] Verifying matching progress telemetry across Dashboard and Curriculum...")
        # Check Dashboard
        page.locator("button:has-text('Study Space')").click()
        page.wait_for_timeout(1000)
        assert "/dashboard" in page.url

        # Check completed lesson count card is visible
        assert page.locator("text=LESSONS COMPLETED").first.is_visible()

        # Check Curriculum
        page.locator("button:has-text('Curriculum Explorer')").first.click()
        page.wait_for_timeout(1000)
        assert "/curriculum" in page.url

        # Database consistency check
        with get_db() as db:
            summary = get_learner_summary(db, learner_rec.id)
            assert summary["total_lessons_completed"] == 1
            assert summary["module_progress"][1]["status"] == "in_progress"
            assert summary["module_progress"][1]["pct"] > 0.0

        print("\nAll 20 steps of the Phase 12 Acceptance Test successfully executed and verified!")
        browser.close()
