"""
Screen 05: Module Overview
Reusable single template screen dynamically populated with actual data for any of the 8 modules.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.components.artwork import render_artwork
from app.curriculum.loader import get_module
from app.database.connection import get_db
from app.database.crud import get_learner_summary
from app.auth.guards import require_auth
import app.navigation.nav as nav

def render_module_overview_screen(module_id: int):
    with get_db() as db:
        auth = require_auth(db, active_route=f"/module/{module_id}")
        if not auth:
            return
        user, learner = auth
        summary = get_learner_summary(db, learner.id)

    module = get_module(module_id)
    if not module:
        with page_shell(active_route="/curriculum"):
            with ui.column().classes("w-full max-w-4xl mx-auto px-6 py-20 text-center"):
                ui.label("Module Not Found").classes("font-serif text-3xl")
                ui.button("Return to Curriculum", on_click=nav.go_to_curriculum).classes("btn-blue mt-4")
        return

    mod_prog = summary["module_progress"].get(module.id, {"status": "not_started", "pct": 0.0})
    pct = mod_prog["pct"]

    with page_shell(active_route="/curriculum"):
        with ui.column().classes("w-full max-w-6xl mx-auto px-4 sm:px-6 py-10 gap-8"):
            # Breadcrumbs
            with ui.row().classes("items-center gap-2 text-xs text-[#8C857D] font-mono"):
                ui.link("Curriculum", "/curriculum").classes("hover:text-[#161616] no-underline text-[#8C857D]")
                ui.label("›")
                ui.label(module.code).classes("text-[#23342B] font-bold")

            # Module Header
            with ui.row().classes("w-full justify-between items-end flex-wrap gap-4"):
                with ui.column().classes("gap-2 max-w-2xl"):
                    with ui.row().classes("items-center gap-2 flex-wrap"):
                        ui.label(module.code).classes("font-mono text-xs font-bold text-[#23342B] bg-[#EFEAE2] px-2.5 py-0.5 rounded")
                        ui.label(module.syllabus_unit).classes("text-xs text-[#8C857D]")
                        ui.label(f"{module.contact_hours} Hours • {module.assessment_marks} Marks").classes("text-xs text-[#2D6A4F] bg-[#EFEAE2] px-2 py-0.5 rounded font-semibold")

                    ui.label(module.title).classes("editorial-title text-3xl sm:text-4xl")
                    ui.label(module.description).classes("editorial-lead text-sm sm:text-base")

                with ui.column().classes("items-end gap-2"):
                    ui.label(f"Mastery: {pct:.0f}%").classes("text-xs font-mono text-[#8C857D]")
                    first_lesson_id = module.lessons[0].id if module.lessons else "m1-l1"
                    ui.button("Begin Lesson Sequence →", on_click=lambda: nav.open_lesson(module.id, first_lesson_id)).classes("btn-blue text-xs font-semibold px-4 py-2")

            # Module Artwork (Mapped via artwork_id, e.g. ART-05 to ART-12)
            with ui.element("div").classes("w-full"):
                render_artwork(module.artwork_id, height_px=320, show_caption=True)

            # Learning Objectives & Topics Grid
            with ui.row().classes("w-full gap-6 flex-wrap md:flex-nowrap"):
                # Objectives
                with ui.card().classes("pip-card flex-1 p-6 gap-3"):
                    ui.label("LEARNING OBJECTIVES").classes("text-[11px] font-bold text-[#23342B] tracking-wider uppercase font-mono")
                    with ui.column().classes("gap-2.5"):
                        for obj in module.learning_objectives:
                            with ui.row().classes("items-start gap-2"):
                                ui.label("✓").classes("text-xs text-[#2D6A4F] font-bold mt-0.5")
                                ui.label(obj).classes("text-xs text-[#5E5A55] leading-relaxed")

                # Topics
                with ui.card().classes("pip-card flex-1 p-6 gap-3"):
                    ui.label("SYLLABUS TOPICS COVERED").classes("text-[11px] font-bold text-[#23342B] tracking-wider uppercase font-mono")
                    with ui.row().classes("flex-wrap gap-2"):
                        for topic in module.topics_covered:
                            ui.label(topic).classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-3 py-1 rounded")

            # Lessons Sequence Section
            with ui.column().classes("w-full gap-4 mt-2"):
                with ui.row().classes("w-full justify-between items-center"):
                    with ui.column().classes("gap-0"):
                        ui.label("LESSON SEQUENCE").classes("editorial-eyebrow")
                        ui.label("Structured Conceptual Progression").classes("font-serif text-2xl text-[#161616]")
                    ui.label(f"{len(module.lessons)} Lessons").classes("text-xs font-mono text-[#8C857D]")

                with ui.column().classes("w-full gap-3"):
                    for idx, lesson in enumerate(module.lessons, 1):
                        with ui.card().classes("pip-card-interactive w-full p-4 sm:p-5 flex flex-row items-center justify-between gap-4 cursor-pointer").on("click", lambda l_id=lesson.id: nav.open_lesson(module.id, l_id)):
                            with ui.row().classes("items-center gap-4 flex-1"):
                                ui.label(f"{idx:02d}").classes("font-mono text-base font-bold text-[#8C857D]")
                                with ui.column().classes("gap-0.5"):
                                    ui.label(lesson.title).classes("font-serif text-lg text-[#161616] font-medium")
                                    ui.label(lesson.subtitle).classes("text-xs text-[#5E5A55] line-clamp-1")

                            with ui.row().classes("items-center gap-3"):
                                ui.label(f"{lesson.reading_time_min}m read").classes("text-xs text-[#8C857D] font-mono hidden sm:block")
                                ui.button("Study →", on_click=lambda l_id=lesson.id: nav.open_lesson(module.id, l_id)).classes("btn-subtle text-xs py-1 px-3")

            # Practice, Assessment, and Mini-Project Links
            with ui.row().classes("w-full gap-6 mt-2 flex-wrap md:flex-nowrap"):
                # Practice Lab
                with ui.card().classes("pip-card flex-1 p-6 gap-3"):
                    with ui.row().classes("justify-between items-center"):
                        ui.label("PRACTICE LAB").classes("text-[11px] font-bold text-[#23342B] tracking-wider uppercase font-mono")
                        ui.label(f"{len(module.practice_exercises)} Exercises").classes("text-[10px] text-[#8C857D] font-mono")
                    ui.label("Interactive Coding Problems").classes("font-serif text-xl text-[#161616]")
                    ui.label("Reinforce syntax and algorithmic reasoning with test-driven coding challenges.").classes("text-xs text-[#5E5A55]")
                    ui.button("Open Practice Lab →", on_click=lambda: nav.open_practice(module.id)).classes("btn-subtle text-xs mt-2 self-start")

                # Quiz Assessment
                with ui.card().classes("pip-card flex-1 p-6 gap-3"):
                    with ui.row().classes("justify-between items-center"):
                        ui.label("ASSESSMENT").classes("text-[11px] font-bold text-[#6E8098] tracking-wider uppercase font-mono")
                        ui.label(f"{len(module.quiz_questions)} Questions").classes("text-[10px] text-[#8C857D] font-mono")
                    ui.label("Module Mastery Quiz").classes("font-serif text-xl text-[#161616]")
                    ui.label("Prove conceptual understanding against Marwadi University evaluation criteria.").classes("text-xs text-[#5E5A55]")
                    ui.button("Take Assessment →", on_click=lambda: nav.open_quiz(module.id)).classes("btn-subtle text-xs mt-2 self-start")

                # Mini-Project
                with ui.card().classes("pip-card flex-1 p-6 gap-3 bg-[#EFEAE2] border-[#D5CEBF]"):
                    with ui.row().classes("justify-between items-center"):
                        ui.label("PRACTICAL PROJECT").classes("text-[11px] font-bold text-[#23342B] tracking-wider uppercase font-mono")
                        ui.label(f"{module.assessment_marks} Marks").classes("text-[10px] text-[#2D6A4F] font-bold")
                    ui.label(module.project.title).classes("font-serif text-xl text-[#161616]")
                    ui.label(module.project.subtitle).classes("text-xs text-[#5E5A55]")
                    ui.button("Project Workshop →", on_click=lambda: nav.open_projects(module.id)).classes("btn-blue text-xs mt-2 self-start font-semibold")
