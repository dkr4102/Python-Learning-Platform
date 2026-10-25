"""
Cohesive editorial footer for Pip Learn.
"""
from nicegui import ui
from app.config import COURSE_CODE, COURSE_NAME, UNIVERSITY, SYLLABUS_CONTACT_HOURS, TOTAL_EVALUATION_MARKS

def render_footer():
    """Render application footer in normal document flow."""
    with ui.element("footer").classes("w-full bg-[#EFEAE2] border-t border-[#E2DCD2] text-[#5E5A55] py-12 px-6 mt-auto font-sans flex-shrink-0"):
        with ui.column().classes("max-w-6xl mx-auto w-full gap-8"):
            with ui.row().classes("w-full justify-between items-start flex-wrap gap-8"):
                with ui.column().classes("gap-2 max-w-sm"):
                    with ui.row().classes("items-center gap-2"):
                        with ui.element("div").classes("w-6 h-6 rounded bg-[#23342B] text-white flex items-center justify-center font-serif text-sm font-bold"):
                            ui.label("π")
                        ui.label("Pip Learn 2.0").classes("font-serif text-xl text-[#161616]")
                    ui.label("Python, one concept at a time. An editorial learning studio where classical artistic warmth meets modern software craftsmanship.").classes("text-xs text-[#5E5A55] leading-relaxed")
                    ui.label(f"Built for {UNIVERSITY} • {COURSE_NAME} ({COURSE_CODE})").classes("text-xs text-[#8C857D] mt-2 font-medium")

                with ui.column().classes("gap-2 text-xs"):
                    ui.label("ACADEMIC STRUCTURE").classes("text-[11px] font-semibold text-[#161616] tracking-wider uppercase")
                    ui.label(f"Total Syllabus Units: 8 Units ({SYLLABUS_CONTACT_HOURS} Contact Hours)")
                    ui.label(f"Evaluated Modules: 7 Modules + Common IA ({TOTAL_EVALUATION_MARKS} Marks)")
                    ui.link("Course Syllabus Traceability", "/report").classes("text-[#23342B] hover:underline no-underline")
                    ui.link("Final Evaluation Report", "/report").classes("text-[#23342B] hover:underline no-underline")

                with ui.column().classes("gap-2 text-xs"):
                    ui.label("LEARNING SUITE").classes("text-[11px] font-semibold text-[#161616] tracking-wider uppercase")
                    ui.link("Curriculum Explorer", "/curriculum").classes("text-[#5E5A55] hover:text-[#161616] no-underline")
                    ui.link("Practice Laboratory", "/practice").classes("text-[#5E5A55] hover:text-[#161616] no-underline")
                    ui.link("Project Workshop", "/projects").classes("text-[#5E5A55] hover:text-[#161616] no-underline")
                    ui.link("Achievements & Mastery", "/achievements").classes("text-[#5E5A55] hover:text-[#161616] no-underline")

                with ui.column().classes("gap-2 text-xs"):
                    ui.label("SYSTEM & SAFETY").classes("text-[11px] font-semibold text-[#161616] tracking-wider uppercase")
                    ui.label("Subprocess Execution Sandbox: Active")
                    ui.label("Persistence: SQLite 3 DB")
                    ui.label("Artwork Collection: 12 Fine-Art Oil Masterworks")
                    ui.link("Profile & Reset", "/settings").classes("text-[#5E5A55] hover:text-[#161616] no-underline")

            ui.separator().classes("bg-[#E2DCD2]")
            with ui.row().classes("w-full justify-between items-center text-xs text-[#8C857D] flex-wrap gap-4"):
                ui.label("© 2026 Pip Learn Platform. Marwadi University Department of Computer Engineering.")
                ui.label("Crafted with NiceGUI, Python 3.15, SQLite & Scientific Stack.")
