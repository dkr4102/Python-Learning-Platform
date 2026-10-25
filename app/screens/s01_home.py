"""
Screen 01: Welcome / Home Screen
Pip Learn 2.0 - Restored Clean Editorial Homepage
A calm, beautifully balanced learning environment prioritizing readability,
fine-art composition, and focused software craftsmanship.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.components.artwork import render_artwork
from app.curriculum.loader import get_all_modules
from app.config import COURSE_CODE, COURSE_NAME, UNIVERSITY, SYLLABUS_CONTACT_HOURS
import app.navigation.nav as nav


def render_home_screen():
    with page_shell(active_route="/"):
        # ========================================================
        # 1. HERO SECTION — Centered, Balanced Editorial Composition
        # ========================================================
        with ui.element("section").classes("w-full max-w-5xl mx-auto px-4 sm:px-6 md:px-8 pt-10 sm:pt-14 md:pt-16 pb-12 text-center"):
            with ui.column().classes("w-full items-center text-center gap-5"):
                # Academic Eyebrow
                with ui.row().classes("items-center justify-center gap-2 flex-wrap text-xs"):
                    ui.label(f"{UNIVERSITY} • {COURSE_CODE}").classes("editorial-eyebrow text-[#5088C2]")
                    ui.label("•").classes("text-[#8C857D]")
                    ui.label(f"{SYLLABUS_CONTACT_HOURS} Contact Hours • 8 Units").classes("editorial-eyebrow text-[#8C857D]")

                # Balanced Main Headline (Editorial Serif)
                ui.label("Python, one concept at a time.").classes(
                    "font-serif text-4xl sm:text-5xl md:text-6xl text-[#161616] tracking-tight leading-[1.12] text-center max-w-3xl"
                )

                # Short, Meaningful Supporting Description
                ui.label(
                    "An editorial learning studio where classical artistic warmth meets modern software craftsmanship. "
                    "Master Python systematically through guided reasoning, live sandboxes, test-driven coding labs, and verified portfolio projects."
                ).classes("text-base sm:text-lg text-[#5E5A55] text-center max-w-2xl leading-relaxed font-normal")

                # Two Blue Actions: Start Learning & Explore Curriculum
                with ui.row().classes("items-center justify-center gap-3 sm:gap-4 pt-2 flex-wrap"):
                    ui.button(
                        "Start Learning →",
                        on_click=nav.start_learning
                    ).classes("btn-blue text-sm sm:text-base font-semibold px-7 py-3 rounded-xl shadow-xs")

                    ui.button(
                        "Explore Curriculum",
                        on_click=nav.go_to_curriculum
                    ).classes("btn-blue-outline text-sm sm:text-base font-medium px-6 py-3 rounded-xl")

                # Fine-art Landscape Artwork (ART-01 The Beginning)
                with ui.element("div").classes("w-full max-w-4xl mx-auto mt-8 md:mt-10"):
                    render_artwork(
                        "ART-01",
                        height_px=460,
                        show_caption=True,
                        classes="shadow-sm rounded-2xl overflow-hidden border border-[#E2DCD2]"
                    )

        # ========================================================
        # 2. 5-STAGE LEARNING PHILOSOPHY — Visually Quiet & Focused
        # ========================================================
        with ui.element("section").props('id="about"').classes("w-full bg-[#FAF7F2] border-y border-[#E2DCD2] py-14 px-4 sm:px-6 md:px-8"):
            with ui.column().classes("w-full max-w-5xl mx-auto gap-8"):
                with ui.column().classes("max-w-2xl gap-2"):
                    ui.label("PEDAGOGICAL PHILOSOPHY").classes("editorial-eyebrow text-[#5088C2]")
                    ui.label("Read. Watch. Experiment. Practice. Check.").classes("font-serif text-2xl sm:text-3xl text-[#161616]")
                    ui.label(
                        "Every syllabus concept is internalized through five deliberate stages—from conceptual reading and video observation to live sandboxes and verified checkpoints."
                    ).classes("text-sm text-[#5E5A55] leading-relaxed")

                stages = [
                    ("01", "Read", "Conceptual reasoning, step-by-step analogies, and execution diagrams."),
                    ("02", "Watch", "Curated Corey Schafer instruction with synchronized study notes."),
                    ("03", "Experiment", "Live, isolated Python sandboxes to predict and verify interpreter behavior."),
                    ("04", "Practice", "Tiered coding exercises with diagnostic hints and automated unit tests."),
                    ("05", "Check", "Rigorous concept checkpoints, mastery badges, and capstone projects.")
                ]
                with ui.grid(columns="repeat(auto-fit, minmax(180px, 1fr))").classes("w-full gap-4"):
                    for num, title, desc in stages:
                        with ui.column().classes("h-full bg-white border border-[#E2DCD2] p-5 rounded-xl gap-2 shadow-xs justify-between"):
                            with ui.column().classes("gap-1.5"):
                                ui.label(num).classes("font-mono text-xs text-[#5088C2] font-semibold")
                                ui.label(title).classes("font-serif text-lg text-[#161616] font-medium")
                                ui.label(desc).classes("text-xs text-[#5E5A55] leading-relaxed")

        # ========================================================
        # 3. ACADEMIC SYLLABUS — Clean, Well-Spaced Directory (8 Units)
        # ========================================================
        with ui.element("section").classes("w-full max-w-5xl mx-auto px-4 sm:px-6 md:px-8 py-14"):
            with ui.row().classes("w-full justify-between items-end mb-8 flex-wrap gap-4 pb-3 border-b border-[#E2DCD2]"):
                with ui.column().classes("gap-1"):
                    ui.label("ACADEMIC SYLLABUS").classes("editorial-eyebrow text-[#5088C2]")
                    ui.label("Eight Comprehensive Syllabus Units").classes("font-serif text-2xl sm:text-3xl text-[#161616]")
                    ui.label(f"{SYLLABUS_CONTACT_HOURS} Contact Hours • Structured from Foundational Syntax to Data Analytics").classes("text-xs sm:text-sm text-[#5E5A55]")
                ui.button("View Full Curriculum Explorer →", on_click=nav.go_to_curriculum).props("flat dense").classes("text-xs font-semibold text-[#5088C2] hover:underline normal-case font-mono")

            modules = get_all_modules()
            with ui.grid(columns="repeat(auto-fit, minmax(280px, 1fr))").classes("w-full gap-5"):
                for m in modules:
                    def make_click_handler(m_id):
                        return lambda: nav.open_module(m_id)

                    with ui.card().classes("pip-card-interactive flex flex-col justify-between h-full p-5 rounded-xl bg-white border border-[#E2DCD2] hover:border-[#5088C2] transition-all cursor-pointer shadow-xs gap-3").on("click", make_click_handler(m.id)):
                        with ui.column().classes("w-full gap-2"):
                            with ui.row().classes("w-full justify-between items-center"):
                                ui.label(m.code).classes("text-xs font-mono font-bold text-[#5088C2] bg-[#EBF3FA] px-2.5 py-0.5 rounded-full")
                                ui.label(f"{m.contact_hours} Contact Hours").classes("text-[11px] text-[#8C857D] font-mono")
                            ui.label(m.title).classes("font-serif text-lg text-[#161616] font-medium leading-snug")
                            ui.label(m.description).classes("text-xs text-[#5E5A55] line-clamp-2 leading-relaxed")
                        with ui.row().classes("w-full justify-between items-center text-xs font-mono pt-3 border-t border-[#E2DCD2]/60 text-[#8C857D]"):
                            ui.label(f"Project: {m.project.title}").classes("truncate max-w-[170px]")
                            ui.label("Explore →").classes("text-[#5088C2] font-sans font-semibold")

        # ========================================================
        # 4. LEARNING ENVIRONMENT — Quiet Thoughtful Studio (ART-03 The Study)
        # ========================================================
        with ui.element("section").classes("w-full bg-[#FAF7F2] border-t border-[#E2DCD2] py-14 px-4 sm:px-6 md:px-8"):
            with ui.column().classes("w-full max-w-5xl mx-auto"):
                with ui.row().classes("w-full items-center gap-8 md:gap-12 flex-wrap lg:flex-nowrap"):
                    with ui.column().classes("flex-1 gap-3.5"):
                        ui.label("THE LEARNING ENVIRONMENT").classes("editorial-eyebrow text-[#5088C2]")
                        ui.label("A Quiet Studio for Modern Python Craft").classes("font-serif text-2xl sm:text-3xl text-[#161616] leading-tight")
                        ui.label(
                            "Pip Learn removes gamified noise, flashing streaks, and superficial copy-pasting. "
                            "Instead, it provides an editorial space focused on genuine comprehension, code construction, "
                            "and verified academic mastery."
                        ).classes("text-sm text-[#5E5A55] leading-relaxed")

                        with ui.row().classes("gap-3 pt-2 flex-wrap"):
                            ui.button(
                                "Enter Study Space →",
                                on_click=nav.go_to_dashboard
                            ).classes("btn-blue text-sm font-semibold px-6 py-2.5 rounded-xl")

                            ui.button(
                                "Begin Module 1",
                                on_click=lambda: nav.open_module(1)
                            ).classes("btn-blue-outline text-sm font-medium px-5 py-2.5 rounded-xl")

                    with ui.element("div").classes("w-full lg:w-[400px] flex-shrink-0"):
                        render_artwork("ART-03", height_px=250, show_caption=True, classes="shadow-sm rounded-xl overflow-hidden border border-[#E2DCD2]")
