"""
Pip Learn 2.0 - Main Application Entrypoint & Router
Marwadi University - Programming with Python (Course: 01AP0303)
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv()

from nicegui import app, ui
from app.config import ARTWORKS_DIR, BASE_DIR
from app.database.connection import init_db
from app.screens.s00_auth import render_login_screen, render_register_screen
from app.screens.s01_home import render_home_screen
from app.screens.s02_setup import render_setup_screen
from app.screens.s03_dashboard import render_dashboard_screen
from app.screens.s04_curriculum import render_curriculum_screen
from app.screens.s05_module import render_module_overview_screen
from app.screens.s06_lesson import render_lesson_screen
from app.screens.s07_practice import render_practice_screen
from app.screens.s08_quiz import render_quiz_screen
from app.screens.s09_project import render_project_screen
from app.screens.s10_achievements import render_achievements_screen
from app.screens.s11_report import render_report_screen
from app.screens.s12_settings import render_settings_screen

# 1. Initialize SQLite Database & Ensure Tables and Schema Migrations
init_db()

# 2. Mount Static Artworks Directory
app.add_static_files("/artworks", str(ARTWORKS_DIR))

# 3. Inject Editorial CSS Style System
css_path = Path(__file__).parent / "visual" / "styles.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        app.add_static_files("/css", str(css_path.parent))


def apply_page_head(title: str = "Pip Learn — Python, one concept at a time."):
    """Set page metadata and include custom font and styling."""
    ui.page_title(title)
    ui.colors(
        primary="#4F83BC",
        secondary="#EFEAE2",
        accent="#6E8098",
        dark="#161616",
        positive="#2D6A4F",
        negative="#9D3A3A",
        info="#6E8098",
        warning="#B4692C"
    )
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            ui.add_head_html(f"<style>{f.read()}</style>")


# ==========================================
# 12 Core Screen Routes
# ==========================================

@ui.page("/")
def page_home():
    apply_page_head("Pip Learn — Editorial Python Studio")
    render_home_screen()


@ui.page("/login")
def page_login(redirect: str = "/dashboard"):
    apply_page_head("Sign In — Pip Learn")
    render_login_screen(redirect_target=redirect)


@ui.page("/register")
def page_register(redirect: str = "/dashboard"):
    apply_page_head("Create Account — Pip Learn")
    render_register_screen(redirect_target=redirect)


@ui.page("/logout")
def page_logout():
    from app.navigation.nav import logout
    logout()


@ui.page("/start")
def page_start():
    apply_page_head("Starting Learning — Pip Learn")
    from app.navigation.nav import start_learning
    start_learning()


@ui.page("/setup")
def page_setup():
    apply_page_head("Learner Setup — Pip Learn")
    render_setup_screen()


@ui.page("/dashboard")
def page_dashboard():
    apply_page_head("Study Space Dashboard — Pip Learn")
    render_dashboard_screen()


@ui.page("/curriculum")
def page_curriculum():
    apply_page_head("Curriculum Explorer — Marwadi University 01AP0303")
    render_curriculum_screen()


@ui.page("/module/{module_id}")
def page_module(module_id: int):
    apply_page_head(f"Module {module_id} Overview — Pip Learn")
    render_module_overview_screen(int(module_id))


@ui.page("/module/{module_id}/lesson/{lesson_id}")
def page_lesson(module_id: int, lesson_id: str, stage: str = None):
    apply_page_head(f"Lesson Workspace — Pip Learn")
    render_lesson_screen(int(module_id), lesson_id, stage=stage)


@ui.page("/practice")
def page_practice(module: int = 1):
    apply_page_head("Practice Laboratory — Pip Learn")
    render_practice_screen(initial_module_id=int(module or 1))


@ui.page("/module/{module_id}/quiz")
def page_quiz(module_id: int):
    apply_page_head(f"Assessment — Module {module_id} — Pip Learn")
    render_quiz_screen(int(module_id))


@ui.page("/projects")
def page_projects(module: int = 1):
    apply_page_head("Practical Project Workshop — Pip Learn")
    render_project_screen(initial_module_id=int(module or 1))


@ui.page("/achievements")
def page_achievements():
    apply_page_head("Achievements & Academic Progression — Pip Learn")
    render_achievements_screen()


@ui.page("/report")
def page_report():
    apply_page_head("Academic Evaluation Report — MU Course 01AP0303")
    render_report_screen()


@ui.page("/settings")
def page_settings():
    apply_page_head("Settings & Profile — Pip Learn")
    render_settings_screen()


if __name__ in {"__main__", "__mp_main__"}:
    import os
    port = int(os.environ.get("PORT", 8080))
    storage_secret = os.environ.get("PIP_STORAGE_SECRET", "pip-learn-marwadi-01ap0303-secret-key-32chars")
    ui.run(
        title="Pip Learn 2.0",
        port=port,
        reload=False,
        show=False,
        storage_secret=storage_secret
    )

