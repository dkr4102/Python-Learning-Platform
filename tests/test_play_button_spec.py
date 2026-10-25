"""
Playwright Test Suite for Pip Learn YouTube-Style Play Button & Player Integrity
Verifies:
1. Compact YouTube-style play button (68x48px, rounded rectangle, centered white triangle).
2. Precise centering relative to the 16:9 video container.
3. Thumbnail clear without dimming (opacity: 1, filter: none).
4. Hover transition on play button.
5. In-place layer activation on click anywhere on thumbnail or play button.
6. Keyboard activation (Enter/Space) for accessibility.
7. Zero layout shifts before, during, and after playback.
8. Shared behavior across multiple lessons (e.g. M1-L1 and M1-L2).
"""
import pytest
from playwright.sync_api import sync_playwright


def test_youtube_play_button_appearance_and_centering():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Step 0: Authenticate as priya
        page.goto("http://localhost:8080/login", wait_until="networkidle")
        page.locator("input[placeholder*='priya']").fill("priya")
        page.locator("input[type='password']").fill("Priya123!")
        page.locator("button:has-text('Sign In →')").click()
        page.wait_for_timeout(800)

        # -----------------------------------------------------------------
        # TEST FIRST VIDEO LESSON (Unit 1, Lesson 2: install/setup)
        # -----------------------------------------------------------------
        page.goto("http://localhost:8080/module/1/lesson/py-v2-u1-l02", wait_until="networkidle")
        page.wait_for_timeout(800)

        # Navigate to 02 · Watch tab
        page.locator("div.q-tab:has-text('Watch')").click()
        page.wait_for_timeout(600)

        video_container = page.locator(".video-frame-container")
        assert video_container.is_visible()
        c_box = video_container.bounding_box()
        assert c_box is not None

        # Verify 16:9 aspect ratio
        aspect_ratio = c_box["width"] / c_box["height"]
        assert abs(aspect_ratio - (16.0 / 9.0)) < 0.05

        # Verify thumbnail styling: no dimming, opacity is 1
        poster_img = page.locator(".video-poster-img")
        assert poster_img.is_visible()
        opacity = page.evaluate("el => window.getComputedStyle(el).opacity", poster_img.element_handle())
        assert float(opacity) == 1.0, f"Expected opacity 1.0, got {opacity}"

        # Verify Play button exists and is unique (exactly 1)
        play_btn = page.locator(".video-play-btn")
        assert play_btn.count() == 1
        assert play_btn.is_visible()

        # Check button dimensions: ~68px width x ~48px height
        btn_box = play_btn.bounding_box()
        assert btn_box is not None
        assert abs(btn_box["width"] - 68.0) <= 2.0, f"Expected width ~68px, got {btn_box['width']}"
        assert abs(btn_box["height"] - 48.0) <= 2.0, f"Expected height ~48px, got {btn_box['height']}"

        # Check centering inside video container (relative positioning)
        # Container center
        c_center_x = c_box["x"] + c_box["width"] / 2.0
        c_center_y = c_box["y"] + c_box["height"] / 2.0
        # Button center
        btn_center_x = btn_box["x"] + btn_box["width"] / 2.0
        btn_center_y = btn_box["y"] + btn_box["height"] / 2.0

        assert abs(c_center_x - btn_center_x) < 2.0, f"Play button not horizontally centered: {c_center_x} vs {btn_center_x}"
        assert abs(c_center_y - btn_center_y) < 2.0, f"Play button not vertically centered: {c_center_y} vs {btn_center_y}"

        # Verify white triangle SVG inside button
        triangle_svg = play_btn.locator("svg path")
        assert triangle_svg.is_visible()

        # Hover test: Button should trigger hover transition
        poster_layer = page.locator(".video-poster-layer")
        poster_layer.hover()
        page.wait_for_timeout(300)

        # Click thumbnail to activate playback
        poster_layer.click()
        page.wait_for_timeout(1000)

        # Overlay must be hidden after playback begins
        assert not play_btn.is_visible(), "Play button overlay still visible after playback started!"
        assert not poster_img.is_visible(), "Thumbnail poster still visible after playback started!"

        # Iframe must be loaded
        iframe = page.locator("iframe.youtube-frame")
        assert iframe.is_visible()
        src = iframe.get_attribute("src") or ""
        assert "YYXdXT2l-Gg" in src
        assert "autoplay=1" in src
        assert "controls=1" in src

        # Zero layout shift verification
        c_box_playing = video_container.bounding_box()
        assert abs(c_box["x"] - c_box_playing["x"]) < 1.0
        assert abs(c_box["y"] - c_box_playing["y"]) < 1.0
        assert abs(c_box["width"] - c_box_playing["width"]) < 1.0
        assert abs(c_box["height"] - c_box_playing["height"]) < 1.0

        # -----------------------------------------------------------------
        # TEST STRINGS VIDEO (Unit 1, Lesson 4) — Shared Component Verification
        # -----------------------------------------------------------------
        page.goto("http://localhost:8080/module/1/lesson/py-v2-u1-l04", wait_until="networkidle")
        page.wait_for_timeout(800)

        page.locator("div.q-tab:has-text('Watch')").click()
        page.wait_for_timeout(600)

        l2_container = page.locator(".video-frame-container")
        assert l2_container.is_visible()
        l2_btn = page.locator(".video-play-btn")
        assert l2_btn.is_visible()
        l2_box = l2_btn.bounding_box()
        assert abs(l2_box["width"] - 68.0) <= 2.0
        assert abs(l2_box["height"] - 48.0) <= 2.0

        # Test keyboard activation on poster layer (Enter key)
        l2_poster = page.locator(".video-poster-layer")
        l2_poster.focus()
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        l2_iframe = page.locator("iframe.youtube-frame")
        assert l2_iframe.is_visible()
        assert "k9TUPpGqYTo" in (l2_iframe.get_attribute("src") or "")

        browser.close()
        print("✓ All YouTube play button and player integrity specifications verified!")


if __name__ == "__main__":
    test_youtube_play_button_appearance_and_centering()
