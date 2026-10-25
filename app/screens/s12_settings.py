"""
Screen 12: Settings & Profile
Learner identity management, environment diagnostics, and study space preferences.
"""
import sys
from nicegui import ui
from app.components.layout import page_shell
from app.database.connection import get_db
from app.database.crud import update_learner_profile, reset_learner_course_progress
from app.auth.guards import require_auth
import app.navigation.nav as nav
from app.config import COURSE_CODE, COURSE_NAME, UNIVERSITY, DB_PATH

def render_settings_screen():
    with get_db() as db:
        auth = require_auth(db, active_route="/settings")
        if not auth:
            return
        user, learner = auth
        learner_id = learner.id
        current_name = learner.name
        current_level = learner.level or "Beginner"
        current_goal = learner.goal or ""
        username = user.username
        email = user.email

    with page_shell(active_route="/settings"):
        with ui.column().classes("w-full max-w-3xl mx-auto px-4 sm:px-6 py-10 gap-8"):
            # Header
            with ui.row().classes("w-full justify-between items-end pb-4 border-b border-[#E2DCD2] flex-wrap gap-4"):
                with ui.column().classes("gap-1"):
                    ui.label("STUDY PREFERENCES & ENVIRONMENT").classes("editorial-eyebrow")
                    ui.label("Settings & Profile").classes("editorial-title text-3xl sm:text-4xl")
                    ui.label("Configure your identity, review database persistence, and verify runtime diagnostics.").classes("editorial-lead text-sm")

                ui.button("Sign Out", on_click=nav.logout).props("outline").classes("btn-subtle text-xs text-[#9D3A3A] px-3.5 py-1.5")

            # Account & Profile Card
            with ui.card().classes("pip-card w-full p-6 sm:p-8 gap-5 shadow-sm"):
                with ui.row().classes("w-full justify-between items-center"):
                    ui.label("AUTHENTICATED LEARNER IDENTITY").classes("text-[10px] font-bold text-[#396DAB] font-mono tracking-wider uppercase")
                    with ui.row().classes("items-center gap-1.5 text-xs text-[#8C857D] font-mono"):
                        ui.label(f"User: @{username}")
                        ui.label("•")
                        ui.label(email)

                name_box = ui.input("Learner Full Name", value=current_name).classes("w-full text-sm")
                level_box = ui.select(
                    options=["Beginner", "Intermediate", "Advanced"],
                    value=current_level,
                    label="Course Skill Track"
                ).classes("w-full text-sm")
                goal_box = ui.textarea("Academic / Practical Goal", value=current_goal).classes("w-full text-sm").props("rows=2")

                def save_settings():
                    with get_db() as db_session:
                        update_learner_profile(db_session, learner_id, name_box.value, level_box.value, goal_box.value)
                    ui.notify("Profile updated successfully!", color="positive")

                ui.button("Save Profile Changes", on_click=save_settings).classes("btn-blue text-xs font-semibold self-start px-4 py-2")

            # Environment Diagnostics Card
            with ui.card().classes("pip-card w-full p-6 sm:p-8 gap-4 bg-[#F5F2EC] border border-[#E2DCD2] shadow-sm"):
                ui.label("PLATFORM ENVIRONMENT & TELEMETRY").classes("text-[10px] font-bold text-[#8C857D] font-mono tracking-wider uppercase")

                diag_items = [
                    ("Python Runtime", f"Python {sys.version.split()[0]} ({sys.platform})"),
                    ("Course Alignment", f"{UNIVERSITY} • {COURSE_CODE}"),
                    ("Database Engine", f"SQLite 3 ({DB_PATH.name})"),
                    ("Execution Sandbox", "Isolated Subprocess (Timeout: 3.5s, Clean TempDir)"),
                    ("Frontend Framework", "NiceGUI (Python-first architecture with Editorial CSS)"),
                    ("Artwork Asset Suite", "12 Fine-Art Oil Masterworks (Optimized WebP 88)")
                ]

                with ui.column().classes("w-full gap-2 text-xs"):
                    for title, val in diag_items:
                        with ui.row().classes("w-full justify-between items-center py-1.5 border-b border-[#E2DCD2]"):
                            ui.label(title).classes("text-[#5E5A55] font-medium")
                            ui.label(val).classes("font-mono text-[#161616]")

            # Danger Zone / Progress Reset Card
            with ui.card().classes("w-full bg-[#FFF8F8] border border-[#F8B4B4] p-6 sm:p-8 rounded-xl gap-4 shadow-sm"):
                with ui.row().classes("items-center gap-2 text-[#9D3A3A]"):
                    ui.icon("warning", size="20px")
                    ui.label("DANGER ZONE — RESET LEARNER PROGRESS").classes("text-xs font-bold font-mono tracking-wider uppercase")

                ui.label(
                    "Resetting your course progress will erase all completed lessons, quiz scores, practice exercise records, "
                    "and unlocked milestone badges for this account. Your login credentials and account will remain active. "
                    "This action cannot be undone."
                ).classes("text-xs text-[#5E5A55] leading-relaxed")

                # Confirmation Dialog
                with ui.dialog() as reset_dialog, ui.card().classes("bg-[#FBF8F3] border border-[#E2DCD2] p-6 max-w-md gap-4"):
                    ui.label("Confirm Course Progress Reset").classes("font-serif text-2xl text-[#161616]")
                    ui.label(
                        "Are you absolutely certain? All your interactive lesson completions, code sandbox notes, "
                        "and assessment grades will be permanently cleared."
                    ).classes("text-xs text-[#5E5A55] leading-relaxed")

                    def confirm_reset():
                        with get_db() as db_session:
                            reset_learner_course_progress(db_session, learner_id)
                        reset_dialog.close()
                        ui.notify("Course progress has been reset to 0%.", color="warning")
                        ui.navigate.to("/dashboard")

                    with ui.row().classes("w-full justify-end gap-3 pt-2"):
                        ui.button("Cancel", on_click=reset_dialog.close).classes("btn-subtle text-xs")
                        ui.button("Yes, Reset My Progress", on_click=confirm_reset).classes("bg-[#9D3A3A] text-white text-xs font-semibold px-4 py-2 rounded")

                ui.button("Reset Course Progress...", on_click=reset_dialog.open).classes("bg-[#9D3A3A] text-white text-xs font-semibold self-start px-4 py-2 rounded")
