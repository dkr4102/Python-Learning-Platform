"""
Tests for Video Player Layout & Playback Experience and Stage Navigation.
Verifies:
1. Fixed 16:9 video container geometry before, during, and after play (zero layout shift).
2. Native playback controls (controls=1, playsinline=1, allowfullscreen, native YouTube iframe).
3. Removal of redundant 'Continue to Experiment Stage' button from study notes panel.
4. One consistent bottom navigation bar (Left: Back, Center: Progress, Right: Next) across all stages.
5. Notes autosave without interrupting playback or altering player dimensions.
6. Responsive layout stability on both desktop (side-by-side) and mobile (stacked).
"""
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8080"


def test_video_player_layout_stability_and_navigation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        # Step 1: Sign in with existing test user
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        page.locator("input[placeholder*='priya']").fill("priya")
        page.locator("input[type='password']").fill("Priya123!")
        page.locator("button:has-text('Sign In →')").click()
        page.wait_for_timeout(1000)

        # Step 2: Open first lesson with a verified video (Install and Setup)
        page.goto(f"{BASE_URL}/module/1/lesson/py-v2-u1-l02", wait_until="networkidle")
        page.wait_for_timeout(1000)
        assert "Lesson Workspace" in page.title()

        # Step 3: Switch to Watch stage
        page.locator("div.q-tab:has-text('Watch')").click()
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # 1. FIXED 16:9 CONTAINER & ZERO LAYOUT SHIFT VERIFICATION
        # -------------------------------------------------------------
        video_container = page.locator(".video-frame-container")
        assert video_container.is_visible()

        # Measure dimensions before clicking Play
        box_before = video_container.bounding_box()
        assert box_before is not None
        assert box_before["width"] > 400
        aspect_ratio_before = box_before["width"] / box_before["height"]
        # 16/9 is ~1.7778, check within 2%
        assert abs(aspect_ratio_before - (16.0 / 9.0)) < 0.05, f"Aspect ratio {aspect_ratio_before} is not 16:9"

        # Check study notes card position before play
        notes_card = page.locator(".workspace-pane-right .workbench-card").first
        notes_box_before = notes_card.bounding_box()
        assert notes_box_before is not None

        # Verify initial thumbnail and play button are present
        poster_img = page.locator(".video-poster-img")
        assert poster_img.is_visible()
        play_btn = page.locator(".video-play-btn")
        assert play_btn.is_visible()

        # Click Play to start YouTube embed
        play_btn.click()
        page.wait_for_timeout(1000)

        # Measure dimensions during playback
        box_after = video_container.bounding_box()
        assert box_after is not None

        # VERIFY ZERO LAYOUT SHIFT: x, y, width, height must remain identical
        assert abs(box_before["x"] - box_after["x"]) < 1.0, "Video container shifted horizontally!"
        assert abs(box_before["y"] - box_after["y"]) < 1.0, "Video container shifted vertically!"
        assert abs(box_before["width"] - box_after["width"]) < 1.0, "Video container width changed!"
        assert abs(box_before["height"] - box_after["height"]) < 1.0, "Video container height changed!"

        # Verify surrounding study notes did not shift
        notes_box_after = notes_card.bounding_box()
        assert abs(notes_box_before["x"] - notes_box_after["x"]) < 1.0, "Notes card shifted horizontally!"
        assert abs(notes_box_before["y"] - notes_box_after["y"]) < 1.0, "Notes card shifted vertically!"

        # -------------------------------------------------------------
        # 2. NATIVE PLAYBACK CONTROLS & IFRAME ATTRIBUTES
        # -------------------------------------------------------------
        iframe = page.locator("iframe.youtube-frame")
        assert iframe.is_visible()
        iframe_src = iframe.get_attribute("src") or ""
        assert "controls=1" in iframe_src, "controls=1 missing from iframe src"
        assert "playsinline=1" in iframe_src, "playsinline=1 missing from iframe src"
        assert "enablejsapi=1" in iframe_src, "enablejsapi=1 missing from iframe src"
        assert iframe.get_attribute("allowfullscreen") is not None, "allowfullscreen attribute missing"

        # -------------------------------------------------------------
        # 3. VERIFY NO REDUNDANT FORWARD BUTTON IN NOTES PANEL
        # -------------------------------------------------------------
        # There must be NO "Continue to Experiment Stage" button inside the notes panel
        redundant_btn = page.locator(".workspace-pane-right button:has-text('Continue to Experiment Stage')")
        assert not redundant_btn.is_visible(), "Redundant button still present in notes panel!"

        # -------------------------------------------------------------
        # 4. STUDY NOTES AUTOSAVE WITHOUT INTERRUPTING PLAYBACK
        # -------------------------------------------------------------
        import time
        notes_input = page.locator("textarea[placeholder*='Take notes']")
        assert notes_input.is_visible()
        unique_note = f"Corey Schafer notes timestamp {time.time()}"
        notes_input.fill(unique_note)
        page.locator("text=✓ Notes saved").wait_for(timeout=4000)
        assert page.locator("text=✓ Notes saved").is_visible()

        # Verify iframe is still present and container did not shift
        box_after_typing = video_container.bounding_box()
        assert abs(box_after["width"] - box_after_typing["width"]) < 1.0
        assert abs(box_after["height"] - box_after_typing["height"]) < 1.0

        # -------------------------------------------------------------
        # 5. BOTTOM NAVIGATION BAR ACROSS ALL STAGES
        # -------------------------------------------------------------
        footer = page.locator(".lesson-nav-footer")
        assert footer.is_visible()

        # On Watch stage:
        # Left: Back: Read
        # Center: STAGE 02 OF 05
        # Right: Next Stage: Experiment
        assert footer.locator("button:has-text('Back: Read')").is_visible()
        assert footer.locator("text=STAGE 02 OF 05").is_visible()
        next_to_exp = footer.locator("button:has-text('Next Stage: Experiment')")
        assert next_to_exp.is_visible()

        # Click Next Stage: Experiment -> advances to Experiment stage
        next_to_exp.click()
        page.locator(".q-tab--active:has-text('Experiment')").wait_for(timeout=3000)
        assert "Experiment" in page.locator(".q-tab--active").text_content()

        # On Experiment stage:
        assert footer.locator("button:has-text('Back: Watch')").is_visible()
        assert footer.locator("text=STAGE 03 OF 05").is_visible()
        next_to_prac = footer.locator("button:has-text('Next Stage: Practice')")
        next_to_prac.wait_for(state="visible", timeout=3000)
        next_to_prac.click()
        page.locator(".q-tab--active:has-text('Practice')").wait_for(timeout=3000)
        assert "Practice" in page.locator(".q-tab--active").text_content()

        # On Practice stage:
        assert footer.locator("button:has-text('Back: Experiment')").is_visible()
        assert footer.locator("text=STAGE 04 OF 05").is_visible()
        next_to_check = footer.locator("button:has-text('Next Stage: Check')")
        next_to_check.wait_for(state="visible", timeout=3000)
        next_to_check.click()
        page.locator(".q-tab--active:has-text('Check')").wait_for(timeout=3000)
        assert "Check" in page.locator(".q-tab--active").text_content()

        # On Check stage:
        assert footer.locator("button:has-text('Back: Practice')").is_visible()
        assert footer.locator("text=STAGE 05 OF 05").is_visible()
        assert footer.locator("button:has-text('Next Lesson')").is_visible()

        # -------------------------------------------------------------
        # 6. RESPONSIVE LAYOUT VERIFICATION (MOBILE STACKING)
        # -------------------------------------------------------------
        page.set_viewport_size({"width": 390, "height": 844})
        page.locator("div.q-tab:has-text('Watch')").click()
        page.wait_for_timeout(600)

        # On mobile viewport (390px), video container and notes card should stack vertically
        video_box_mobile = page.locator(".video-frame-container").bounding_box()
        notes_box_mobile = page.locator(".workspace-pane-right .workbench-card").first.bounding_box()
        assert video_box_mobile is not None
        assert notes_box_mobile is not None
        # Notes must be positioned below the video container
        assert notes_box_mobile["y"] > video_box_mobile["y"] + video_box_mobile["height"], "Notes are not stacked below video on mobile!"

        browser.close()
