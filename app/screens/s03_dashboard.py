"""
Screen 03: Learning Dashboard
The learner's personal study environment with real progress persistence, active modules, and stats.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.components.artwork import render_artwork
from app.database.connection import get_db
from app.database.crud import get_learner_summary
from app.curriculum.loader import get_all_modules
from app.auth.guards import require_auth
import app.navigation.nav as nav

def render_dashboard_screen():
    with get_db() as db:
        auth = require_auth(db, active_route="/dashboard")
        if not auth:
            return
        user, learner = auth
        learner_id = learner.id
        learner_name = learner.name
        learner_level = learner.level or "Beginner"
        learner_goal = learner.goal or "Master Python for Marwadi University Course 01AP0303"
        summary = get_learner_summary(db, learner.id)

    modules = get_all_modules()

    with page_shell(active_route="/dashboard"):
        with ui.column().classes("w-full max-w-6xl mx-auto px-4 sm:px-6 py-8 md:py-10 gap-8"):
            # ========================================================
            # Dashboard Welcome Header
            # ========================================================
            with ui.row().classes("w-full justify-between items-end flex-wrap gap-4 pb-2"):
                with ui.column().classes("gap-1 max-w-2xl"):
                    ui.label(f"STUDY SPACE • {learner_level.upper()} TRACK").classes("editorial-eyebrow")
                    ui.label(f"Welcome back, {learner_name}").classes("editorial-title text-3xl sm:text-4xl")
                    ui.label(learner_goal).classes("editorial-lead text-sm sm:text-base leading-relaxed")

                with ui.row().classes("gap-3 pt-2"):
                    ui.button("Curriculum Explorer", on_click=nav.go_to_curriculum).classes("btn-subtle text-xs px-3.5 py-2")
                    # Dynamically resume next recommended lesson based on canonical progress
                    ui.button("Continue Learning →", on_click=lambda lid=learner_id: nav.resume_learning(lid)).classes("btn-primary text-xs font-semibold px-4 py-2")

            # Atmospheric Dashboard Artwork: ART-03 (The Study) - Clean editorial integration
            with ui.element("div").classes("w-full"):
                render_artwork("ART-03", height_px=260, show_caption=False)

            # ========================================================
            # Real Metric Cards (Derived directly from SQLite DB)
            # ========================================================
            with ui.row().classes("w-full gap-4 flex-wrap md:flex-nowrap"):
                metrics = [
                    ("COURSE PROGRESS", f"{summary.get('overall_percentage', 0.0):.1f}%", f"{summary.get('completed_modules_count', 0)} of 8 Modules Mastered", "school"),
                    ("LESSONS COMPLETED", f"{summary.get('total_lessons_completed', 0)}", "Interactive theory & demos", "menu_book"),
                    ("PRACTICE EXERCISES", f"{summary.get('total_practice_passed', 0)}", f"{summary.get('total_practice_runs', 0)} total lab runs logged", "terminal"),
                    ("ACHIEVEMENTS", f"{summary.get('achievements_count', 0)}", "Earned academic milestones", "military_tech")
                ]
                for label, value, sub, icon in metrics:
                    with ui.column().classes("flex-1 min-w-[200px] bg-[#FBF8F3] border border-[#E2DCD2] p-5 rounded-xl gap-1.5 shadow-sm"):
                        with ui.row().classes("w-full justify-between items-center text-[#8C857D]"):
                            ui.label(label).classes("text-[10px] font-mono font-semibold tracking-wider text-[#6E8098]")
                            ui.icon(icon, size="20px").classes("text-[#4F83BC]")
                        ui.label(value).classes("font-serif text-3xl text-[#161616] font-bold")
                        ui.label(sub).classes("text-xs text-[#5E5A55]")

            # ========================================================
            # Active Modules Grid
            # ========================================================
            with ui.column().classes("w-full gap-4 mt-2"):
                with ui.row().classes("w-full justify-between items-baseline pb-2 border-b border-[#E2DCD2]"):
                    with ui.column().classes("gap-0"):
                        ui.label("ACADEMIC MODULES").classes("editorial-eyebrow")
                    ui.button("Full Syllabus Explorer →", on_click=nav.go_to_curriculum).props("flat dense").classes("text-xs font-semibold text-[#396DAB] normal-case hover:underline font-mono")

                with ui.grid(columns="repeat(auto-fit, minmax(270px, 1fr))").classes("w-full gap-4"):
                    for m in modules:
                        mod_prog = summary.get("module_progress", {}).get(m.id, {"status": "not_started", "pct": 0.0})
                        pct = mod_prog.get("pct", 0.0)
                        status_text = "Completed" if pct >= 95.0 else ("In Progress" if pct > 0 else "Not Started")
                        status_badge_color = "bg-[#2D6A4F] text-white" if pct >= 95.0 else ("bg-[#4F83BC] text-white" if pct > 0 else "bg-[#EFEAE2] text-[#8C857D]")

                        with ui.card().classes("pip-card-interactive p-5 gap-3 cursor-pointer rounded-xl").on("click", lambda m_id=m.id: nav.open_module(m_id)):
                            with ui.row().classes("w-full justify-between items-center"):
                                ui.label(m.code).classes("text-xs font-mono font-bold text-[#396DAB] bg-[#E9F1F9] px-2 py-0.5 rounded")
                                ui.label(status_text).classes(f"text-[10px] px-2 py-0.5 rounded font-mono uppercase {status_badge_color}")

                            ui.label(m.title).classes("font-serif text-xl text-[#161616] leading-snug")

                            # Progress bar
                            with ui.column().classes("w-full gap-1 pt-1"):
                                with ui.row().classes("w-full justify-between text-[11px] text-[#8C857D] font-mono"):
                                    ui.label("Completion")
                                    ui.label(f"{pct:.0f}%")
                                with ui.element("div").classes("w-full h-1.5 bg-[#EFEAE2] rounded-full overflow-hidden"):
                                    ui.element("div").classes("h-full bg-[#4F83BC] rounded-full transition-all duration-300").style(f"width: {pct}%;")

                            # Clean project name without truncation
                            with ui.column().classes("w-full pt-2 border-t border-[#E2DCD2] gap-1"):
                                with ui.row().classes("w-full justify-between items-center"):
                                    ui.label("PROJECT").classes("text-[9px] font-mono font-bold text-[#8C857D]")
                                    ui.label("Study →").classes("text-xs text-[#396DAB] font-semibold")
                                ui.label(m.project.title).classes("text-xs text-[#161616] font-medium leading-tight")
