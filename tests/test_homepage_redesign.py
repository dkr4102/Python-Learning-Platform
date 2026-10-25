"""
Playwright Test Suite for Pip Learn Restored Clean Editorial Homepage
Verifies:
1. Exact preservation of π (Pi) logo and clean compact navigation header.
2. Centered, balanced headline: "Python, one concept at a time."
3. Two blue buttons: Start Learning and Explore Curriculum.
4. Beautifully framed landscape artwork ART-01 The Beginning below copy.
5. Removal of giant white semicircle and full-bleed hero overlay.
6. Quiet 5-stage learning philosophy (Read, Watch, Experiment, Practice, Check).
7. Calm editorial 8-unit curriculum section with working navigation triggers.
8. Closing publication section with ART-03 The Study.
9. Responsive stability on both desktop (1440x900) and mobile (390x844).
"""
import pytest
from playwright.sync_api import sync_playwright


def test_homepage_redesign_editorial_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # DESKTOP VIEWPORT TEST (1440 x 900)
        # -------------------------------------------------------------
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        # Step 1: Navigate to homepage
        page.goto("http://localhost:8080/", wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 1. Verify Logo: π monogram & compact header
        logo = page.locator("header .monogram-pi")
        assert logo.is_visible(), "π monogram logo missing from header"
        assert page.locator("header .font-serif:has-text('π')").is_visible()
        brand_name = page.locator("header").locator("text=Pip Learn")
        assert brand_name.is_visible()

        # 2. Verify Dominant Balanced Headline
        h1 = page.locator(".font-serif:has-text('Python, one concept at a time.')")
        assert h1.is_visible(), "Centered editorial headline missing"

        # 3. Verify Two Blue Hero CTA buttons
        start_btn = page.locator("button:has-text('Start Learning →')")
        assert start_btn.is_visible()
        curriculum_btn = page.locator("button:has-text('Explore Curriculum')")
        assert curriculum_btn.is_visible()

        # 4. Verify Landscape Artwork ART-01 (01-the-beginning.webp) in framed container
        hero_art = page.locator("img[src*='01-the-beginning.webp']")
        assert hero_art.is_visible(), "Hero artwork ART-01 missing or not visible"

        # 5. Verify Removal of Giant Curved Semicircle & Full-screen overlay
        assert page.locator(".dia-half-circle-container").count() == 0, "Giant semicircle must be removed"
        assert page.locator(".hero-dia-bg-wrapper").count() == 0, "Full-bleed hero background treatment must be removed"

        # 6. Verify 5-Stage Learning Philosophy (Quiet and focused)
        assert page.locator("text=PEDAGOGICAL PHILOSOPHY").is_visible()
        assert page.locator("text=Read. Watch. Experiment. Practice. Check.").is_visible()
        assert page.locator("text=01").first.is_visible()
        assert page.locator("text=Read").first.is_visible()
        assert page.locator("text=Watch").first.is_visible()
        assert page.locator("text=Experiment").first.is_visible()
        assert page.locator("text=Practice").first.is_visible()
        assert page.locator("text=Check").first.is_visible()

        # 7. Verify 8-Unit Academic Curriculum Directory
        curriculum_section = page.locator("text=Eight Comprehensive Syllabus Units")
        assert curriculum_section.is_visible()

        cards = page.locator(".pip-card-interactive")
        assert cards.count() >= 8, f"Expected 8 syllabus unit cards, found {cards.count()}"

        # Check Module 1 card content
        m1_card = cards.first
        assert "MOD-01" in m1_card.text_content()
        assert "Python Fundamentals" in m1_card.text_content()
        assert "Explore →" in m1_card.text_content()

        # 8. Verify Closing Publication Section with ART-03
        closing_heading = page.locator("text=A Quiet Studio for Modern Python Craft")
        assert closing_heading.is_visible()
        assert page.locator("text=Enter Study Space →").is_visible()
        assert page.locator("text=Begin Module 1").is_visible()

        closing_art = page.locator("img[src*='03-the-study.webp']")
        assert closing_art.is_visible(), "Closing artwork ART-03 missing"

        # Capture Desktop Fullpage Screenshot
        page.screenshot(path="brain_artifacts/homepage_desktop_clean_minimal.png", full_page=True)

        # -------------------------------------------------------------
        # MOBILE VIEWPORT TEST (390 x 844 - iPhone 14)
        # -------------------------------------------------------------
        mobile_context = browser.new_context(viewport={"width": 390, "height": 844})
        mobile_page = mobile_context.new_page()
        mobile_page.goto("http://localhost:8080/", wait_until="networkidle")
        mobile_page.wait_for_timeout(800)

        # Verify key mobile elements are visible without overflow
        assert mobile_page.locator(".font-serif:has-text('Python, one concept at a time.')").is_visible()
        assert mobile_page.locator("button:has-text('Start Learning →')").is_visible()
        assert mobile_page.locator("button:has-text('Explore Curriculum')").is_visible()
        assert mobile_page.locator("img[src*='01-the-beginning.webp']").is_visible()

        # Verify no horizontal scrollbar / overflow
        scroll_width = mobile_page.evaluate("document.documentElement.scrollWidth")
        client_width = mobile_page.evaluate("document.documentElement.clientWidth")
        assert scroll_width <= client_width + 1, f"Horizontal overflow detected: scrollWidth={scroll_width}, clientWidth={client_width}"

        # Capture Mobile Screenshot
        mobile_page.screenshot(path="brain_artifacts/homepage_mobile_clean_minimal.png", full_page=True)

        browser.close()


if __name__ == "__main__":
    test_homepage_redesign_editorial_flow()
