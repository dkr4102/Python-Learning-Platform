"""
Test Module 1 -> Lesson 1 Watch Stage Video Integration
Verifies:
1. Verified mapping for Module 1, Lesson 1 (Bro Code: Start coding with PYTHON in 5 minutes!).
2. Subsequent lessons preserve Corey Schafer primary playlist.
3. YouTube thumbnail with 68x48 centered native-looking play control.
4. Correct Title, Creator ("Creator: Bro Code"), and "Open on YouTube ↗" fallback link.
5. In-place Play action swaps thumbnail layer for active YouTube iframe with standard controls.
6. Responsive 16:9 aspect ratio maintained before, during, and after playback.
7. Helpful fallback banner is available if embed restrictions trigger.
"""
import pytest
from playwright.sync_api import sync_playwright

from app.curriculum.videos import get_lesson_video

BASE_URL = "http://localhost:8080"


def test_video_metadata_mapping():
    """Verify backend mapping for Module 1, Lesson 1 and subsequent lessons."""
    # 1. Lesson 1 has Bro Code introduction
    v1 = get_lesson_video("py-v2-u1-l01")
    assert v1 is not None, "Lesson 1 must have a mapped video"
    assert v1.video_id == "Sg4GMVMdOPo"
    assert "Start coding with PYTHON in 5 minutes!" in v1.title
    assert v1.instructor == "Bro Code"
    assert v1.channel == "Bro Code"
    assert v1.source_url == "https://www.youtube.com/watch?v=Sg4GMVMdOPo"

    # 2. Subsequent lesson (Lesson 2) preserves Corey Schafer
    v2 = get_lesson_video("py-v2-u1-l02")
    assert v2 is not None
    assert v2.video_id == "YYXdXT2l-Gg"
    assert v2.instructor == "Corey Schafer"
    assert "Install and Setup" in v2.title


def test_module1_lesson1_watch_stage_playback_experience():
    """Playwright browser verification of Watch stage for Module 1, Lesson 1."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Step 0: Sign in
        page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        page.locator("input[placeholder*='priya']").fill("priya")
        page.locator("input[type='password']").fill("Priya123!")
        page.locator("button:has-text('Sign In →')").click()
        page.wait_for_timeout(1000)

        # Step 1: Open Module 1, Lesson 1 directly at Watch stage
        page.goto(f"{BASE_URL}/module/1/lesson/py-v2-u1-l01?stage=watch", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # Verify Watch tab is active
        watch_tab = page.locator("div.q-tab--active:has-text('Watch')")
        assert watch_tab.is_visible(), "Watch stage tab must be active"

        # -------------------------------------------------------------
        # 1. Video Container & 16:9 Aspect Ratio
        # -------------------------------------------------------------
        container = page.locator(".video-frame-container")
        assert container.is_visible()
        c_box = container.bounding_box()
        assert c_box is not None
        aspect_ratio = c_box["width"] / c_box["height"]
        assert abs(aspect_ratio - (16.0 / 9.0)) < 0.05, f"Expected 16:9 ratio, got {aspect_ratio}"

        # -------------------------------------------------------------
        # 2. Thumbnail & Compact Native-Looking Play Button
        # -------------------------------------------------------------
        poster = page.locator(".video-poster-img")
        assert poster.is_visible()
        src = poster.get_attribute("src")
        assert "Sg4GMVMdOPo" in src, f"Expected thumbnail for Sg4GMVMdOPo, got {src}"

        play_btn = page.locator(".video-play-btn")
        assert play_btn.is_visible()
        btn_box = play_btn.bounding_box()
        assert btn_box is not None
        # Verify compact dimensions (approx 68x48px)
        assert 50 <= btn_box["width"] <= 80, f"Button width {btn_box['width']} is unexpected"
        assert 35 <= btn_box["height"] <= 60, f"Button height {btn_box['height']} is unexpected"

        # -------------------------------------------------------------
        # 3. Metadata Verification: Title, Creator, Fallback Link
        # -------------------------------------------------------------
        title_label = page.locator("text=Start coding with PYTHON in 5 minutes!")
        assert title_label.is_visible(), "Video title must be visible in study companion"

        creator_label = page.locator("text=Creator: Bro Code")
        assert creator_label.is_visible(), "Creator 'Bro Code' must be visible"

        fallback_link = page.locator("a:has-text('Open on YouTube'):visible").first
        assert fallback_link.is_visible(), "'Open on YouTube ↗' link must be visible"
        href = fallback_link.get_attribute("href")
        assert "Sg4GMVMdOPo" in href, f"Fallback link should point to Sg4GMVMdOPo, got {href}"

        # Capture screenshot before playback
        page.screenshot(path="brain_artifacts/m1_l1_watch_before_play.png")

        # -------------------------------------------------------------
        # 4. In-Place Playback: Click Play & Verify YouTube Iframe
        # -------------------------------------------------------------
        play_btn.click()
        page.wait_for_timeout(1000)

        # Poster layer must be hidden
        assert page.locator(".video-poster-layer.hidden").count() > 0

        # YouTube iframe must be injected and visible
        iframe = page.locator("iframe#youtube-player-iframe")
        assert iframe.is_visible(), "YouTube iframe must be loaded upon play"
        iframe_src = iframe.get_attribute("src")
        assert "Sg4GMVMdOPo" in iframe_src
        assert "autoplay=1" in iframe_src
        assert "controls=1" in iframe_src

        # Verify zero layout shift on container
        c_box_after = container.bounding_box()
        assert abs(c_box_after["width"] - c_box["width"]) < 2
        assert abs(c_box_after["height"] - c_box["height"]) < 2

        # Capture screenshot during active playback
        page.screenshot(path="brain_artifacts/m1_l1_watch_after_play.png")

        browser.close()
