"""
End-to-end integration and browser tests for the definitive Pip Learn lesson workspace.
Tests the complete 5-stage learning journey:
Read → Watch → Experiment → Practice → Check → Certification
"""
import time
from playwright.sync_api import sync_playwright
import pytest
from app.database.connection import get_db
from app.database.models import LessonActivity, LessonCompletion


def test_complete_lesson_journey():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Step 0: Authenticate
        page.goto("http://localhost:8080/login", wait_until="networkidle")
        page.wait_for_timeout(800)
        page.locator("input[placeholder*='priya']").fill("priya")
        page.locator("input[type='password']").fill("Priya123!")
        page.locator("button:has-text('Sign In →')").click()
        page.wait_for_timeout(1000)

        # Step 1: Open Lesson 1
        page.goto("http://localhost:8080/module/1/lesson/py-v2-u1-l01", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Verify page title and header
        assert "Lesson Workspace" in page.title()
        header = page.locator(".lesson-header-card")
        assert header.is_visible()
        assert "Welcome to Programming and Python" in header.text_content()

        # -------------------------------------------------------------
        # STAGE 01: READ
        # -------------------------------------------------------------
        print("Testing Stage 01: Read...")
        # Switch explicitly to 01 · Read tab and Section 1 pill to test clean journey
        page.locator("div.q-tab:has-text('Read')").click()
        page.wait_for_timeout(600)
        page.locator("button:has-text('1. Prerequisites')").click()
        page.wait_for_timeout(600)

        # Check section 1 is loaded
        assert page.locator("text=SECTION 1 OF 5").is_visible()
        page.screenshot(path="brain_artifacts/test_stage_01_sec1.png")

        # Step through reading sections
        next_sec_btn = page.locator("text=Next Section →")
        for i in range(2, 6):
            next_sec_btn.click()
            page.wait_for_timeout(400)
            assert page.locator(f"text=SECTION {i} OF 5").is_visible()

        page.screenshot(path="brain_artifacts/test_stage_01_sec5.png")

        # Lesson 1 advances to Watch stage (now verified with Bro Code intro)
        watch_advance_btn = page.locator("button:has-text('Continue to Watch Stage →')")
        assert watch_advance_btn.is_visible()
        watch_advance_btn.click()
        page.wait_for_timeout(800)

        # Verify Watch stage is active
        assert page.locator("div.q-tab--active:has-text('Watch')").is_visible()

        # Advance to Experiment stage
        exp_advance_btn = page.locator("button:has-text('Next Stage: Experiment →')")
        assert exp_advance_btn.is_visible()
        exp_advance_btn.click()
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # STAGE 03: EXPERIMENT
        # -------------------------------------------------------------
        print("Testing Stage 03: Experiment...")
        exp_tab = page.locator(".q-tab--active")
        assert "Experiment" in exp_tab.text_content()

        # Fill prediction
        pred_input = page.locator("input[placeholder*='I predict']")
        assert pred_input.is_visible()
        pred_input.fill("I predict one line explaining that Python turns instructions into useful work.")

        # Run starter code
        run_exp_btn = page.locator("button:has-text('Run Code ▶')")
        assert run_exp_btn.is_visible()
        run_exp_btn.click()
        page.wait_for_timeout(2000)

        output_el = page.locator(".code-output")
        assert "Python turns instructions into useful work." in output_el.text_content()
        page.screenshot(path="brain_artifacts/test_stage_03_executed.png")

        # Click bottom navigation Next Stage: Practice
        page.locator(".lesson-nav-footer button:has-text('Next Stage: Practice')").click()
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # STAGE 04: PRACTICE
        # -------------------------------------------------------------
        print("Testing Stage 04: Practice...")
        prac_tab = page.locator(".q-tab--active")
        assert "Practice" in prac_tab.text_content()

        # Verify 3 challenges exist
        assert page.locator("button:has-text('Challenge 1')").is_visible()
        assert page.locator("button:has-text('Challenge 2')").is_visible()
        assert page.locator("button:has-text('Challenge 3')").is_visible()

        solution = 'message = "Python turns instructions into useful work."\nprint(message)'
        for challenge_number in (1, 2, 3):
            page.locator(f"button:has-text('Challenge {challenge_number}:')").click()
            page.wait_for_timeout(250)
            page.locator(".q-tab-panel:visible textarea").last.fill(solution)
            page.locator(".q-tab-panel:visible button:has-text('Run Tests')").click()
            page.wait_for_timeout(800)
            assert page.locator(".q-tab-panel:visible").get_by_text("Tests Passed", exact=False).is_visible()
        page.screenshot(path="brain_artifacts/test_stage_04_passed.png")

        # Click bottom navigation Next Stage: Check
        page.locator(".lesson-nav-footer button:has-text('Next Stage: Check')").click()
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # STAGE 05: CHECK
        # -------------------------------------------------------------
        print("Testing Stage 05: Check...")
        check_tab = page.locator(".q-tab--active")
        assert "Check" in check_tab.text_content()

        # If already certified complete from earlier test, click Review Questions to start fresh
        review_btn = page.locator("button:has-text('Review Questions')")
        if review_btn.is_visible():
            review_btn.click()
            page.wait_for_timeout(600)

        # Question 1
        assert page.locator("text=QUESTION 1 OF 2").is_visible()

        # Select incorrect option first to test diagnostic retry behavior
        inc_opt = page.locator("text=It requires memorising CPython bytecode before coding")
        inc_opt.click()
        page.locator("button:has-text('Check Answer')").click()
        page.wait_for_timeout(500)
        assert page.locator("text=Not quite yet — Try again").is_visible()
        page.screenshot(path="brain_artifacts/test_stage_05_incorrect_feedback.png")

        # Now select correct option
        cor_opt = page.get_by_role("radio", name="What programs are, why Python is useful, and where it is used.")
        cor_opt.click()
        page.locator("button:has-text('Check Answer')").click()
        page.wait_for_timeout(500)
        assert page.locator("text=✓ Correct!").is_visible()

        # Advance to Question 2
        page.locator("button:has-text('Next Question →')").click()
        page.wait_for_timeout(800)
        assert page.locator("text=QUESTION 2 OF 2").is_visible()

        # Select correct option for Question 2
        q2_opt = page.get_by_role("radio", name="Predict the effect, run it, then explain the observed difference")
        q2_opt.click()
        page.locator("button:has-text('Check Answer')").click()
        page.wait_for_timeout(500)
        assert page.locator("text=✓ Correct!").is_visible()

        # Complete and certify lesson
        page.locator("button:has-text('Complete & Certify Lesson →')").click()
        page.wait_for_timeout(1000)

        # Verify completion certificate state
        assert page.locator("text=LESSON CERTIFIED COMPLETE").is_visible()
        assert page.locator("text=Conceptual Mastery Confirmed!").is_visible()
        assert page.locator("button:has-text('Next Lesson →')").is_visible()
        page.screenshot(path="brain_artifacts/test_stage_05_certified.png")

        # -------------------------------------------------------------
        # DATABASE PERSISTENCE VERIFICATION
        # -------------------------------------------------------------
        with get_db() as db:
            act = db.query(LessonActivity).filter(LessonActivity.lesson_id == "py-v2-u1-l01").first()
            assert act is not None
            assert act.stage == "check"
            assert act.experiment_attempted is True

            comp = db.query(LessonCompletion).filter(LessonCompletion.lesson_id == "py-v2-u1-l01").first()
            assert comp is not None

        browser.close()
        print("✓ All 5 stages and database persistence verified successfully!")


if __name__ == "__main__":
    test_complete_lesson_journey()
