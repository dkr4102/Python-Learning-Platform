"""
Screen 02: Learner Setup / Onboarding
Personalize learner name, skill level, academic goals, and entry module recommendation.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.database.connection import get_db
from app.database.crud import update_learner_profile
from app.auth.guards import require_auth
from app.config import UNIVERSITY, COURSE_CODE, COURSE_NAME
import app.navigation.nav as nav

def render_setup_screen():
    with get_db() as db:
        auth = require_auth(db, active_route="/setup")
        if not auth:
            return
        user, learner = auth
        learner_id = learner.id
        current_name = learner.name if learner.name not in {"Python Learner", ""} else ""
        current_level = learner.level or "Beginner"
        current_goal = learner.goal or ""

    with page_shell(active_route="/setup"):
        with ui.column().classes("w-full max-w-xl mx-auto px-4 sm:px-6 py-10 md:py-14 gap-8"):
            # Header
            with ui.column().classes("gap-2 text-center w-full items-center"):
                ui.label("LEARNER ONBOARDING").classes("editorial-eyebrow")
                ui.label("Welcome to Pip Learn").classes("editorial-title text-3xl sm:text-4xl")
                ui.label(f"Personalize your learning space for {UNIVERSITY} {COURSE_CODE} ({COURSE_NAME}).").classes("editorial-lead text-sm")

            # Setup Card
            with ui.card().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] p-6 sm:p-8 rounded-xl gap-6 shadow-sm"):
                # Name input
                with ui.column().classes("w-full gap-1.5"):
                    with ui.row().classes("w-full justify-between items-baseline"):
                        ui.label("Full Name").classes("text-xs font-semibold text-[#161616]")
                        ui.label("Required").classes("text-[10px] text-[#8C857D] font-mono")
                    name_input = ui.input(
                        value=current_name,
                        placeholder="Your full name (e.g. Alex Morgan)"
                    ).props("outlined dense").classes("w-full bg-white text-sm")

                # Skill level selection
                with ui.column().classes("w-full gap-1.5"):
                    ui.label("Current Python Familiarity").classes("text-xs font-semibold text-[#161616]")
                    options = [
                        "Beginner (New to programming)",
                        "Intermediate (Familiar with syntax & loops)",
                        "Advanced (Looking for systematic mastery)"
                    ]
                    initial_val = options[0]
                    if "Intermediate" in current_level:
                        initial_val = options[1]
                    elif "Advanced" in current_level:
                        initial_val = options[2]

                    level_select = ui.select(
                        options=options,
                        value=initial_val
                    ).props("outlined dense").classes("w-full bg-white text-sm")

                # Objective textarea
                with ui.column().classes("w-full gap-1.5"):
                    with ui.row().classes("w-full justify-between items-baseline"):
                        ui.label("Primary Academic / Career Objective").classes("text-xs font-semibold text-[#161616]")
                        ui.label("Optional").classes("text-[10px] text-[#8C857D] font-mono")
                    goal_input = ui.textarea(
                        value=current_goal,
                        placeholder="e.g. Master Python 01AP0303 with distinction and build real-world software applications"
                    ).props("outlined rows=3").classes("w-full bg-white text-sm")

                # Dynamic recommendation callout
                recommendation_box = ui.column().classes("w-full bg-[#E9F1F9] p-4 rounded-lg border-l-4 border-[#4F83BC] gap-1")
                with recommendation_box:
                    ui.label("RECOMMENDED PATHWAY").classes("text-[10px] font-mono font-bold text-[#396DAB] uppercase tracking-wider")
                    rec_label = ui.label("Module 1: Python Fundamentals — Recommended for complete conceptual mastery.").classes("text-xs text-[#5E5A55] leading-relaxed")

                def update_recommendation():
                    val = level_select.value or ""
                    if "Intermediate" in val:
                        rec_label.set_text("Module 3: Data Structures or Module 5: OOP — Fast-track to structured data modeling and object architecture.")
                    elif "Advanced" in val:
                        rec_label.set_text("Module 6: SQLite Persistence or Module 8: Data Analytics — Direct access to capstone modules.")
                    else:
                        rec_label.set_text("Module 1: Python Fundamentals — Recommended for complete conceptual mastery.")

                level_select.on_value_change(update_recommendation)

                # Actions
                with ui.row().classes("w-full justify-between items-center pt-4 border-t border-[#E2DCD2] flex-wrap gap-3"):
                    ui.button("Cancel", on_click=lambda: ui.navigate.to("/")).classes("btn-subtle text-xs")

                    def save_and_continue():
                        entered_name = (name_input.value or "").strip()
                        clean_name = entered_name if entered_name else "Learner"
                        sel_level = level_select.value or "Beginner"
                        if "Intermediate" in sel_level:
                            clean_level = "Intermediate"
                        elif "Advanced" in sel_level:
                            clean_level = "Advanced"
                        else:
                            clean_level = "Beginner"

                        entered_goal = (goal_input.value or "").strip()
                        clean_goal = entered_goal if entered_goal else f"Master Python for {UNIVERSITY} {COURSE_CODE}"

                        with get_db() as db_session:
                            update_learner_profile(db_session, learner_id, clean_name, clean_level, clean_goal, onboarding_completed=True)

                        ui.notify(f"Welcome, {clean_name}! Profile configured.", color="positive")
                        ui.navigate.to("/dashboard")

                    ui.button("Save & Enter Study Space →", on_click=save_and_continue).classes("btn-primary text-sm font-semibold")
