"""
Screen 11: Final Report & Evaluation Summary
Comprehensive academic report for Marwadi University Course 01AP0303 with downloadable export.
"""
import json
from datetime import datetime, timezone
from nicegui import ui
from app.components.layout import page_shell
from app.database.connection import get_db
from app.database.crud import get_learner_summary
from app.curriculum.loader import get_all_modules
from app.config import COURSE_CODE, COURSE_NAME, UNIVERSITY, TOTAL_EVALUATION_MARKS
from app.auth.guards import require_auth
import app.navigation.nav as nav

def render_report_screen():
    with get_db() as db:
        auth = require_auth(db, active_route="/report")
        if not auth:
            return
        user, learner = auth
        learner_name = learner.name
        learner_level = learner.level
        summary = get_learner_summary(db, learner.id)

    modules = get_all_modules()

    with page_shell(active_route="/report"):
        with ui.column().classes("w-full max-w-5xl mx-auto px-4 sm:px-6 py-10 gap-8"):
            # Header banner
            with ui.row().classes("w-full justify-between items-end flex-wrap gap-4 pb-4 border-b border-[#E2DCD2]"):
                with ui.column().classes("gap-1"):
                    ui.label(f"{UNIVERSITY} • INTERNAL ASSESSMENT DOSSIER").classes("editorial-eyebrow")
                    ui.label("Final Academic Evaluation Report").classes("editorial-title text-3xl sm:text-4xl")
                    ui.label(f"Course: {COURSE_CODE} - {COURSE_NAME} ({TOTAL_EVALUATION_MARKS} Marks Rubric)").classes("editorial-lead text-sm")

                # Download / Export Actions
                with ui.row().classes("gap-2"):
                    def export_json():
                        export_payload = {
                            "university": UNIVERSITY,
                            "course_code": COURSE_CODE,
                            "course_name": COURSE_NAME,
                            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
                            "learner": summary["learner"],
                            "overall_percentage": summary["overall_percentage"],
                            "total_lessons_completed": summary["total_lessons_completed"],
                            "total_quizzes_taken": summary["total_quizzes_taken"],
                            "total_projects_completed": summary["total_projects_completed"],
                            "module_progress": summary["module_progress"],
                            "achievements": summary["achievements"]
                        }
                        content = json.dumps(export_payload, indent=2)
                        ui.download(content.encode("utf-8"), filename=f"PipLearn_Evaluation_{learner_name.replace(' ', '_')}.json")
                        ui.notify("Academic Dossier JSON downloaded successfully!", color="positive")

                    ui.button("Download Dossier (JSON)", on_click=export_json).classes("btn-blue text-xs font-semibold px-4 py-2")

            # Dossier Metadata Card
            with ui.card().classes("pip-card w-full p-6 gap-4 bg-[#FBF8F3] border border-[#E2DCD2] shadow-sm"):
                ui.label("LEARNER IDENTIFICATION & REGISTRATION").classes("text-[10px] font-bold text-[#8C857D] font-mono tracking-wider")
                with ui.row().classes("w-full justify-between flex-wrap gap-4 text-xs"):
                    with ui.column().classes("gap-1"):
                        ui.label("Learner Name:").classes("text-[#8C857D]")
                        ui.label(learner_name).classes("font-bold text-sm text-[#161616]")
                    with ui.column().classes("gap-1"):
                        ui.label("Skill Level:").classes("text-[#8C857D]")
                        ui.label(learner_level).classes("font-mono text-sm text-[#23342B]")
                    with ui.column().classes("gap-1"):
                        ui.label("Evaluation Framework:").classes("text-[#8C857D]")
                        ui.label("Marwadi University Continuous IA").classes("font-mono text-sm text-[#161616]")
                    with ui.column().classes("gap-1"):
                        ui.label("Assessment Status:").classes("text-[#8C857D]")
                        ui.label("Formative Evaluation Active").classes("font-mono text-sm text-[#2D6A4F] font-bold")

            # Module Breakdown Table
            with ui.column().classes("w-full gap-4 mt-2"):
                with ui.row().classes("w-full justify-between items-center"):
                    with ui.column().classes("gap-0"):
                        ui.label("CURRICULUM BREAKDOWN").classes("editorial-eyebrow")
                        ui.label("Module-by-Module Internal Assessment").classes("font-serif text-2xl text-[#161616]")
                    ui.label("Passing Standard: 60%").classes("text-xs font-mono text-[#8C857D]")

                with ui.card().classes("pip-card w-full p-0 overflow-hidden border border-[#E2DCD2]"):
                    with ui.row().classes("w-full bg-[#EFEAE2] p-3 text-xs font-mono font-bold text-[#5E5A55] border-b border-[#E2DCD2]"):
                        ui.label("Module").classes("w-20")
                        ui.label("Syllabus Unit").classes("flex-1")
                        ui.label("Hours").classes("w-16 text-center")
                        ui.label("Marks").classes("w-16 text-center")
                        ui.label("Lessons").classes("w-20 text-center")
                        ui.label("Quiz Score").classes("w-24 text-center")
                        ui.label("Status").classes("w-24 text-right")

                    for m in modules:
                        mod_prog = summary["module_progress"].get(m.id, {"status": "not_started", "pct": 0.0})
                        pct = mod_prog["pct"]
                        status_str = "Mastered" if pct >= 95 else ("In Progress" if pct > 0 else "Not Started")
                        status_badge = "text-[#2D6A4F] font-bold" if pct >= 95 else ("text-[#B4692C]" if pct > 0 else "text-[#8C857D]")

                        quiz_score_str = f"{mod_prog.get('score', 0):.0f}/{m.assessment_marks}" if "score" in mod_prog else "—"

                        with ui.row().classes("w-full p-3 text-xs border-b border-[#E2DCD2] items-center hover:bg-[#F5F2EC]"):
                            ui.label(m.code).classes("w-20 font-mono font-bold text-[#23342B]")
                            ui.label(m.title).classes("flex-1 font-medium text-[#161616]")
                            ui.label(f"{m.contact_hours}h").classes("w-16 text-center font-mono text-[#5E5A55]")
                            ui.label(f"{m.assessment_marks}m").classes("w-16 text-center font-mono text-[#2D6A4F] font-semibold")
                            ui.label(f"{len(m.lessons)}").classes("w-20 text-center font-mono text-[#5E5A55]")
                            ui.label(quiz_score_str).classes("w-24 text-center font-mono")
                            ui.label(status_str).classes(f"w-24 text-right font-mono {status_badge}")

            # Strengths and Recommended Next Steps
            with ui.row().classes("w-full gap-6 mt-2 flex-wrap md:flex-nowrap"):
                with ui.card().classes("pip-card flex-1 p-6 gap-3"):
                    ui.label("DEMONSTRATED STRENGTHS").classes("text-[11px] font-bold text-[#2D6A4F] tracking-wider uppercase font-mono")
                    with ui.column().classes("gap-2 text-xs text-[#5E5A55]"):
                        ui.label("• Solid conceptual foundation in core syntax, typing, and memory pointers.")
                        ui.label("• Practical proficiency building database-backed CRUD and REST web integrations.")
                        ui.label("• Safe programming habits avoiding SQL injection and unhandled network errors.")

                with ui.card().classes("pip-card flex-1 p-6 gap-3"):
                    ui.label("RECOMMENDED NEXT STEPS").classes("text-[11px] font-bold text-[#B4692C] tracking-wider uppercase font-mono")
                    with ui.column().classes("gap-2 text-xs text-[#5E5A55]"):
                        ui.label("• Complete all 8 module practice exercises in the Practice Laboratory.")
                        ui.label("• Explore multi-table SQLite relational joins and foreign key cascade rules.")
                        ui.label("• Advance to multi-dimensional NumPy array broadcasting for machine learning.")
