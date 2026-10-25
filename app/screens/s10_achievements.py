"""
Screen 10: Progress & Achievements
Verified academic mastery, assessment history, milestone badges, and performance breakdown.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.components.artwork import render_artwork
from app.database.connection import get_db
from app.database.crud import get_learner_summary, DEFAULT_ACHIEVEMENTS
from app.auth.guards import require_auth
import app.navigation.nav as nav

def render_achievements_screen():
    with get_db() as db:
        auth = require_auth(db, active_route="/achievements")
        if not auth:
            return
        user, learner = auth
        learner_name = learner.name
        summary = get_learner_summary(db, learner.id)

    unlocked_codes = {a["code"] for a in summary["achievements"]}

    with page_shell(active_route="/achievements"):
        with ui.column().classes("w-full max-w-6xl mx-auto px-4 sm:px-6 py-10 gap-8"):
            # Header banner
            with ui.row().classes("w-full justify-between items-end flex-wrap gap-4"):
                with ui.column().classes("gap-1"):
                    ui.label("ACADEMIC PROGRESSION & MASTERY").classes("editorial-eyebrow")
                    ui.label("Achievements & Milestone Records").classes("editorial-title text-3xl sm:text-4xl")
                    ui.label(f"Verifiable internal assessment telemetry for {learner_name}.").classes("editorial-lead text-sm")

                ui.button("Export Academic Report →", on_click=nav.open_report).classes("btn-blue text-xs font-semibold px-4 py-2")

            # Atmospheric Artwork: ART-12 The Observatory
            with ui.element("div").classes("w-full"):
                render_artwork("ART-12", height_px=300, show_caption=True)

            # Overview Metrics Grid
            with ui.row().classes("w-full gap-4 flex-wrap md:flex-nowrap"):
                metrics = [
                    ("OVERALL PROGRESS", f"{summary['overall_percentage']:.1f}%", f"{summary['completed_modules_count']} of 8 Modules Finished", "school"),
                    ("LESSONS MASTERED", str(summary["total_lessons_completed"]), "Interactive modules studied", "auto_stories"),
                    ("ASSESSMENT PASSES", f"{summary['total_quizzes_passed']} / {summary['total_quizzes_taken']}", "Verified quiz evaluations", "fact_check"),
                    ("PROJECT COMPLETIONS", str(summary["total_projects_completed"]), "Working applications tested", "terminal")
                ]
                for label, val, sub, icon in metrics:
                    with ui.column().classes("flex-1 min-w-[200px] bg-[#FBF8F3] border border-[#E2DCD2] p-5 rounded-lg gap-1 shadow-sm"):
                        with ui.row().classes("w-full justify-between items-center text-[#8C857D]"):
                            ui.label(label).classes("text-[10px] font-mono font-semibold tracking-wider")
                            ui.icon(icon, size="18px").classes("text-[#23342B]")
                        ui.label(val).classes("font-serif text-3xl font-bold text-[#161616]")
                        ui.label(sub).classes("text-xs text-[#5E5A55]")

            # Milestone Badges Section
            with ui.column().classes("w-full gap-4 mt-2"):
                with ui.row().classes("w-full justify-between items-center"):
                    with ui.column().classes("gap-0"):
                        ui.label("MILESTONE ACHIEVEMENTS").classes("editorial-eyebrow")
                        ui.label(f"Earned Badges ({len(unlocked_codes)} / {len(DEFAULT_ACHIEVEMENTS)})").classes("font-serif text-2xl text-[#161616]")
                    ui.label("Persisted in SQLite").classes("text-xs font-mono text-[#8C857D]")

                with ui.grid(columns="repeat(auto-fit, minmax(260px, 1fr))").classes("w-full gap-4"):
                    for ach in DEFAULT_ACHIEVEMENTS:
                        is_unlocked = ach["code"] in unlocked_codes
                        card_bg = "bg-[#FBF8F3] border-[#23342B]" if is_unlocked else "bg-[#F5F2EC] border-[#E2DCD2] opacity-60"
                        icon_color = "text-[#23342B]" if is_unlocked else "text-[#8C857D]"

                        with ui.card().classes(f"p-5 rounded-lg gap-2 border {card_bg} shadow-sm"):
                            with ui.row().classes("w-full justify-between items-center"):
                                ui.icon(ach["badge_icon"], size="24px").classes(icon_color)
                                status_text = "UNLOCKED" if is_unlocked else "LOCKED"
                                status_color = "bg-[#2D6A4F] text-white" if is_unlocked else "bg-[#EFEAE2] text-[#8C857D]"
                                ui.label(status_text).classes(f"text-[9px] font-mono font-bold px-2 py-0.5 rounded {status_color}")

                            ui.label(ach["title"]).classes("font-serif text-lg font-bold text-[#161616]")
                            ui.label(ach["description"]).classes("text-xs text-[#5E5A55] leading-relaxed")
