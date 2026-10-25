"""
Screen 04: Curriculum Explorer
Editorial catalog of all eight syllabus units, topics, contact hours, and project milestones.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.components.artwork import render_artwork, render_artwork_thumbnail
from app.curriculum.loader import get_all_modules
from app.database.connection import get_db
from app.database.crud import get_learner_summary
from app.config import COURSE_CODE, COURSE_NAME, UNIVERSITY, SYLLABUS_CONTACT_HOURS, TOTAL_EVALUATION_MARKS
from app.auth.guards import require_auth
import app.navigation.nav as nav

def render_curriculum_screen():
    with get_db() as db:
        auth = require_auth(db, active_route="/curriculum")
        if not auth:
            return
        user, learner = auth
        summary = get_learner_summary(db, learner.id)

    modules = get_all_modules()

    with page_shell(active_route="/curriculum"):
        with ui.column().classes("w-full max-w-6xl mx-auto px-4 sm:px-6 py-8 md:py-10 gap-8"):
            # ========================================================
            # SECTION A — CURRICULUM HERO & COMPOSITION
            # ========================================================
            with ui.card().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] p-6 sm:p-8 rounded-xl shadow-sm gap-6"):
                with ui.row().classes("w-full items-center justify-between gap-6 flex-wrap lg:flex-nowrap"):
                    # Left Column: Editorial details & CTAs
                    with ui.column().classes("flex-1 min-w-[300px] gap-3"):
                        ui.label(f"{UNIVERSITY} • {COURSE_NAME} ({COURSE_CODE})").classes("editorial-eyebrow")
                        ui.label("Curriculum Explorer").classes("editorial-title text-3xl sm:text-4xl")
                        ui.label(
                            "The complete eight-unit Python curriculum spanning 45 contact hours. "
                            "Structured from fundamental syntax through object-oriented architecture, database connectivity, "
                            "REST services, automation, and data analytics."
                        ).classes("editorial-lead text-sm sm:text-base leading-relaxed")

                        # Academic Stat Badges Bar
                        with ui.row().classes("w-full gap-2 pt-1 flex-wrap"):
                            stat_items = [
                                ("SYLLABUS UNITS", "8 Units"),
                                ("CONTACT HOURS", f"{SYLLABUS_CONTACT_HOURS} Hours"),
                                ("EVALUATION MARKS", f"{TOTAL_EVALUATION_MARKS} Marks (100% IA)"),
                                ("PRACTICAL PROJECTS", "10 Functional Apps"),
                            ]
                            for label, val in stat_items:
                                with ui.column().classes("bg-[#EFEAE2] px-3 py-1.5 rounded-md gap-0.5 border border-[#E2DCD2]"):
                                    ui.label(label).classes("text-[9px] font-mono font-bold text-[#6E8098] uppercase tracking-wider")
                                    ui.label(val).classes("text-xs font-semibold text-[#161616]")

                        # Action Buttons
                        with ui.row().classes("gap-3 pt-2"):
                            ui.button("Start Module 1 →", on_click=lambda: nav.open_module(1)).classes("btn-primary text-xs font-semibold px-4 py-2")
                            ui.button("Study Dashboard", on_click=nav.go_to_dashboard).classes("btn-subtle text-xs px-4 py-2")

                    # Right Column: ART-04 The Path integrated seamlessly with deliberate aspect ratio
                    with ui.element("div").classes("w-full lg:w-[420px] flex-shrink-0"):
                        render_artwork("ART-04", height_px=240, show_caption=False)

            # ========================================================
            # SECTION B — MODULE COLLECTION (Clean Scannable Cards)
            # ========================================================
            with ui.column().classes("w-full gap-5"):
                with ui.row().classes("w-full justify-between items-baseline pb-2 border-b border-[#E2DCD2]"):
                    with ui.column().classes("gap-0.5"):
                        ui.label("COURSE UNITS").classes("editorial-eyebrow")
                        ui.label("The Complete Eight Modules").classes("font-serif text-2xl text-[#161616]")
                    ui.label("Marwadi University Syllabus Order").classes("text-xs text-[#8C857D] font-mono hidden sm:block")

                for m in modules:
                    mod_prog = summary.get("module_progress", {}).get(m.id, {"status": "not_started", "pct": 0.0})
                    pct = mod_prog.get("pct", 0.0)

                    with ui.card().classes("pip-card w-full p-5 sm:p-6 gap-4 bg-[#FBF8F3] border border-[#E2DCD2] rounded-xl"):
                        with ui.row().classes("w-full items-start gap-6 flex-wrap md:flex-nowrap"):
                            # Left: Artwork Thumbnail Preview (No production badge)
                            with ui.element("div").classes("w-full md:w-auto flex-shrink-0 flex justify-center md:justify-start"):
                                render_artwork_thumbnail(m.artwork_id, width_px=200, height_px=135)

                            # Right: Module Details & Actions
                            with ui.column().classes("flex-1 min-w-[280px] gap-2"):
                                # Top Metadata Pill Row
                                with ui.row().classes("w-full justify-between items-center flex-wrap gap-2"):
                                    with ui.row().classes("items-center gap-2 flex-wrap"):
                                        ui.label(m.code).classes("font-mono text-xs font-bold text-[#396DAB] bg-[#E9F1F9] px-2.5 py-0.5 rounded")
                                        ui.label(m.syllabus_unit).classes("text-xs text-[#5E5A55] font-medium")
                                        ui.label(f"{m.contact_hours} Hours").classes("text-xs text-[#6E8098] bg-[#EFEAE2] px-2 py-0.5 rounded")
                                        ui.label(f"{m.assessment_marks} Marks").classes("text-xs text-[#2D6A4F] bg-[#EFEAE2] px-2 py-0.5 rounded font-semibold")

                                    # Progress badge
                                    status_color = "text-[#2D6A4F]" if pct >= 100 else ("text-[#4F83BC]" if pct > 0 else "text-[#8C857D]")
                                    ui.label(f"{pct:.0f}% Complete").classes(f"text-xs font-mono font-medium {status_color}")

                                # Heading & Description
                                ui.label(m.title).classes("font-serif text-2xl text-[#161616] leading-tight")
                                ui.label(m.description).classes("text-xs sm:text-sm text-[#5E5A55] leading-relaxed line-clamp-2")

                                # Curated Key Topics Preview Chips (restrained progressive disclosure)
                                with ui.row().classes("flex-wrap gap-1.5 pt-0.5"):
                                    for topic in m.topics_covered[:4]:
                                        ui.label(topic).classes("text-[11px] bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-0.5 rounded")
                                    if len(m.topics_covered) > 4:
                                        ui.label(f"+{len(m.topics_covered) - 4} more topics").classes("text-[11px] text-[#8C857D] px-1.5 py-0.5 font-mono")

                                # Bottom Project & Action Row
                                with ui.row().classes("w-full justify-between items-center pt-3 border-t border-[#E2DCD2] flex-wrap gap-3 mt-1"):
                                    with ui.row().classes("items-center gap-2"):
                                        ui.label("PROJECT:").classes("text-[10px] font-mono font-bold text-[#6E8098]")
                                        ui.label(m.project.title).classes("text-xs text-[#161616] font-medium")

                                    with ui.row().classes("items-center gap-2"):
                                        first_lesson_id = m.lessons[0].id if m.lessons else "m1-l1"
                                        ui.button(
                                            "Explore Module →",
                                            on_click=lambda m_id=m.id: nav.open_module(m_id)
                                        ).classes("btn-primary text-xs font-semibold px-4 py-2")
                                        ui.button(
                                            "Start Lessons",
                                            on_click=lambda m_id=m.id, l_id=first_lesson_id: nav.open_lesson(m_id, l_id)
                                        ).classes("btn-subtle text-xs px-3.5 py-2")
