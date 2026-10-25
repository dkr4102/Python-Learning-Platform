"""
Comprehensive Test Suite for Learning Flow Audit, Deterministic Resume Policy,
and Dia Homepage Redesign.
Verifies Examples A-F, navigation consistency, SQLite persistence, and Dia visual elements.
"""
import json
import pytest
from playwright.sync_api import sync_playwright

from app.database.connection import get_db
from app.database.models import (
    User,
    Learner,
    LessonActivity,
    LessonCompletion,
    ModuleProgress,
    UserSession,
)
from app.database.crud import (
    create_learner_for_user,
    ACTIVE_CURRICULUM_VERSION,
    mark_lesson_complete,
)
from app.navigation.nav import resolve_resume_target
from app.curriculum.loader import get_module, get_all_modules
from app.curriculum.challenges import get_lesson_challenges


BASE_URL = "http://localhost:8080"


# =========================================================================
# Unit & Integration Tests: Deterministic Resume State Machine (Examples A-F)
# =========================================================================

def test_resume_policy_examples_a_through_f():
    """
    Test Examples A through F directly against the authoritative resolve_resume_target engine.
    """
    with get_db() as db:
        # 1. Clean test learner
        test_user = db.query(User).filter(User.username == "flow_tester").first()
        if test_user:
            db.delete(test_user)
            db.commit()

        user = User(
            username="flow_tester",
            email="flow_tester@example.com",
            password_hash="mock_hash",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        learner = create_learner_for_user(
            db, user_id=user.id, name="Flow Learner", level="Beginner"
        )
        learner_id = learner.id

        mod1 = get_module(1)
        first_lesson = mod1.lessons[0]
        second_lesson = mod1.lessons[1]
        third_lesson = mod1.lessons[2]

        # -------------------------------------------------------------
        # EXAMPLE A: New learner (registers and clicks Start Learning)
        # Expected: Module 1 -> Lesson 1 -> Read -> Section 1
        # -------------------------------------------------------------
        m_id, l_id, stage = resolve_resume_target(db, learner_id)
        assert m_id == 1, f"Expected Module 1 for new learner, got {m_id}"
        assert l_id == first_lesson.id, f"Expected Lesson {first_lesson.id} for new learner, got {l_id}"
        assert stage == "read", f"Expected stage 'read' for new learner, got {stage}"

        # -------------------------------------------------------------
        # EXAMPLE B: Learner reading
        # User reaches Read Section 4 of Lesson 2, closes browser, returns.
        # Expected: Resume Lesson 2 -> Read -> Section 4 (not Section 1, not Experiment).
        # -------------------------------------------------------------
        act_b = LessonActivity(
            learner_id=learner_id,
            module_id=1,
            lesson_id=second_lesson.id,
            curriculum_version=ACTIVE_CURRICULUM_VERSION,
            stage="read",
            reading_section=3,  # Section 4 (0-indexed 3)
            experiment_attempted=False,
        )
        db.add(act_b)
        db.commit()

        m_id, l_id, stage = resolve_resume_target(db, learner_id)
        assert m_id == 1
        assert l_id == second_lesson.id
        assert stage == "read", f"Expected stage 'read' for incomplete reading, got {stage}"

        # -------------------------------------------------------------
        # EXAMPLE C: Learner experimenting
        # User finishes reading and watching, enters Experiment, edits code, leaves.
        # Expected: Resume Experiment with saved code.
        # -------------------------------------------------------------
        act_b.reading_section = 4  # finished reading
        act_b.stage = "experiment"
        act_b.experiment_code = "print('Custom experimental code by learner')"
        act_b.experiment_attempted = False
        db.commit()

        m_id, l_id, stage = resolve_resume_target(db, learner_id)
        assert m_id == 1
        assert l_id == second_lesson.id
        assert stage == "experiment", f"Expected stage 'experiment', got {stage}"

        # -------------------------------------------------------------
        # EXAMPLE D: Learner practicing
        # User completes two of three exercises, then exits.
        # Expected: Return to Practice -> Exercise 3, preserving prior results.
        # -------------------------------------------------------------
        challenges = get_lesson_challenges(second_lesson.id, second_lesson.practice_tasks or mod1.practice_exercises)
        assert len(challenges) >= 3, "Lesson should have at least 3 practice challenges"

        act_b.experiment_attempted = True
        act_b.stage = "practice"
        # Mark challenge 0 and 1 passed, challenge 2 unpassed
        practice_state = {
            challenges[0].id: {"passed": True, "code": "def passed_one(): pass"},
            challenges[1].id: {"passed": True, "code": "def passed_two(): pass"},
            challenges[2].id: {"passed": False, "code": "def in_progress(): pass"},
        }
        act_b.practice_state_json = json.dumps(practice_state)
        db.commit()

        m_id, l_id, stage = resolve_resume_target(db, learner_id)
        assert m_id == 1
        assert l_id == second_lesson.id
        assert stage == "practice", f"Expected stage 'practice' when exercises remain, got {stage}"

        # -------------------------------------------------------------
        # EXAMPLE E: Lesson completed
        # User passes final checkpoint and exits.
        # Expected: Continue Learning opens the next unfinished lesson at beginning.
        # -------------------------------------------------------------
        mark_lesson_complete(db, learner_id, 1, first_lesson.id, len(mod1.lessons))
        mark_lesson_complete(db, learner_id, 1, second_lesson.id, len(mod1.lessons))

        m_id, l_id, stage = resolve_resume_target(db, learner_id)
        assert m_id == 1
        assert l_id == third_lesson.id, f"Expected next unfinished lesson '{third_lesson.id}', got {l_id}"
        assert stage == "read", f"Expected stage 'read' at the start of next lesson, got {stage}"

        # -------------------------------------------------------------
        # EXAMPLE F: Course completed
        # Display course completion state (/report) rather than arbitrary stage.
        # -------------------------------------------------------------
        all_mods = get_all_modules()
        for mod in all_mods:
            prog = db.query(ModuleProgress).filter(
                ModuleProgress.learner_id == learner_id,
                ModuleProgress.module_id == mod.id,
            ).first()
            if prog:
                prog.status = "completed"
                prog.completion_percentage = 100.0
        db.commit()

        m_id, l_id, stage = resolve_resume_target(db, learner_id)
        assert m_id == -1, "Expected course completion signal (-1)"
        assert stage == "report", f"Expected 'report' state on course completion, got {stage}"

        # Cleanup
        db.delete(user)
        db.commit()


# =========================================================================
# E2E Tests: Playwright UI Verification of Homepage & Learning Navigation
# =========================================================================

def test_homepage_dia_hero_and_navigation():
    """
    Verify the restored clean minimal homepage layout and navigation buttons via headless browser.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # 1. Visit Homepage
        page.goto(BASE_URL, wait_until="networkidle")

        # Verify Header retains existing Pi logo
        pi_logo = page.locator("header .monogram-pi")
        assert pi_logo.count() > 0, "Existing Pi logo must be preserved in header"

        # Verify ART-01 artwork image is present in hero
        hero_art = page.locator("img[src*='01-the-beginning.webp']")
        assert hero_art.count() > 0, "ART-01 landscape artwork must be present"

        # Verify Headline has balanced editorial scale
        headline = page.locator(".font-serif:has-text('Python, one concept at a time.')")
        assert headline.count() > 0, "Hero headline must be present"
        assert "Python, one concept at a time." in headline.inner_text()

        # Verify removal of giant semicircle and full-bleed overlay
        assert page.locator(".dia-half-circle-container").count() == 0, "Giant semicircle must be removed"
        assert page.locator(".hero-dia-bg-wrapper").count() == 0, "Full-bleed hero overlay must be removed"

        # Verify Minimal Navigation on Homepage
        start_btn = page.locator("button:has-text('Start Learning →')")
        assert start_btn.count() > 0, "Start Learning button must be present"

        explore_btn = page.locator("button:has-text('Explore Curriculum')")
        assert explore_btn.count() > 0, "Explore Curriculum button must be present"

        # Verify 5-Stage Learning Philosophy Below Fold
        philosophy_heading = page.locator("text=Read. Watch. Experiment. Practice. Check.")
        assert philosophy_heading.is_visible(), "5-stage philosophy heading must be present"
        assert page.locator("text=Read").first.is_visible()
        assert page.locator("text=Watch").first.is_visible()
        assert page.locator("text=Practice").first.is_visible()
        assert page.locator("text=Check").first.is_visible()

        # Verify Start Learning redirects guest to /start / /login
        start_btn.first.click()
        page.wait_for_timeout(1000)
        current_url = page.url
        assert "/login" in current_url or "/register" in current_url or "/start" in current_url, (
            f"Unauthenticated Start Learning should route through login, got {current_url}"
        )

        browser.close()


def test_responsive_mobile_and_tablet_layout():
    """
    Verify that the clean minimal homepage does not overflow on mobile and tablet viewports.
    """
    viewports = [
        {"name": "Tablet", "width": 768, "height": 1024},
        {"name": "Mobile", "width": 375, "height": 667},
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for vp in viewports:
            context = browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            page = context.new_page()
            page.goto(BASE_URL, wait_until="networkidle")

            # Check for horizontal overflow
            scroll_width = page.evaluate("document.documentElement.scrollWidth")
            client_width = page.evaluate("document.documentElement.clientWidth")
            assert scroll_width <= client_width + 1, f"Horizontal overflow detected on {vp['name']}: {scroll_width} > {client_width}"

            # Verify headline visibility
            headline = page.locator(".font-serif:has-text('Python, one concept at a time.')")
            assert headline.is_visible(), f"Headline must remain visible on {vp['name']}"

            # Verify artwork visibility
            art = page.locator("img[src*='01-the-beginning.webp']")
            assert art.is_visible(), f"Artwork must remain visible on {vp['name']}"

        browser.close()
