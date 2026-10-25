"""
Screen 07: Practice Lab
Interactive coding challenges with test assertions, hints, and automated evaluation.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.curriculum.loader import get_all_modules, get_module
from app.execution.evaluator import evaluate_exercise
from app.database.connection import get_db
from app.database.crud import record_practice_attempt
from app.auth.guards import require_auth
import app.navigation.nav as nav

def render_practice_screen(initial_module_id: int = 1):
    with get_db() as db:
        auth = require_auth(db, active_route=f"/practice?module={initial_module_id}")
        if not auth:
            return
        user, learner = auth
        learner_id = learner.id

    modules = get_all_modules()
    current_module = get_module(initial_module_id) or modules[0]
    exercises = current_module.practice_exercises
    current_exercise = exercises[0] if exercises else None

    with page_shell(active_route="/practice"):
        with ui.column().classes("w-full max-w-6xl mx-auto px-4 sm:px-6 py-10 gap-8"):
            # Header banner
            with ui.row().classes("w-full justify-between items-end flex-wrap gap-4"):
                with ui.column().classes("gap-1"):
                    ui.label("PRACTICE LABORATORY").classes("editorial-eyebrow")
                    ui.label("Interactive Coding Problems").classes("editorial-title text-3xl sm:text-4xl")
                    ui.label("Validate Python solutions against multi-case test assertions in an isolated sandbox.").classes("editorial-lead text-sm")

                # Module selector dropdown
                with ui.row().classes("items-center gap-2"):
                    ui.label("Module:").classes("text-xs text-[#8C857D] font-mono")
                    mod_options = {m.id: f"{m.code}: {m.title}" for m in modules}
                    mod_select = ui.select(
                        options=mod_options,
                        value=current_module.id
                    ).classes("bg-white border border-[#E2DCD2] rounded text-xs min-w-[240px]")
                    mod_select.on_value_change(lambda e: nav.open_practice(e.value))

            if not current_exercise:
                ui.label("No practice exercises registered for this module yet.").classes("text-base text-[#5E5A55] p-6")
                return

            # Main Workspace Container: 2-Column Split
            with ui.row().classes("w-full gap-6 items-start flex-wrap lg:flex-nowrap"):
                # Left Column: Problem Briefing, Hints & Requirements
                with ui.column().classes("w-full lg:w-5/12 gap-5"):
                    # Problem Card
                    with ui.card().classes("pip-card w-full p-6 gap-3"):
                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label(current_exercise.difficulty.upper()).classes("text-[10px] font-mono font-bold bg-[#EFEAE2] text-[#23342B] px-2 py-0.5 rounded")
                            ui.label(f"Exercise ID: {current_exercise.id}").classes("text-[10px] text-[#8C857D] font-mono")

                        ui.label(current_exercise.title).classes("font-serif text-2xl text-[#161616]")
                        ui.label(current_exercise.problem_statement).classes("text-sm text-[#5E5A55] leading-relaxed")

                        # Expectations
                        with ui.column().classes("w-full bg-[#EFEAE2] p-3.5 rounded gap-1 mt-2"):
                            ui.label("INPUT / OUTPUT EXPECTATION").classes("text-[10px] font-bold text-[#23342B] font-mono")
                            ui.label(current_exercise.input_output_expectations).classes("text-xs text-[#5E5A55]")

                    # Step-by-Step Expandable Hints
                    with ui.card().classes("pip-card w-full p-6 gap-3"):
                        ui.label("GUIDED HINTS").classes("text-[10px] font-bold text-[#6E8098] uppercase tracking-wider font-mono")
                        with ui.column().classes("w-full gap-2"):
                            for idx, hint in enumerate(current_exercise.hints, 1):
                                with ui.expansion(f"Hint {idx}", icon="lightbulb").classes("text-xs bg-[#FBF8F3] border border-[#E2DCD2] rounded"):
                                    ui.label(hint).classes("p-3 text-xs text-[#5E5A55] leading-relaxed")

                    # Reference Solution Toggle
                    with ui.expansion("View Reference Solution", icon="visibility").classes("w-full text-xs bg-[#EFEAE2] border border-[#E2DCD2] rounded"):
                        ui.markdown(f"```python\n{current_exercise.solution.strip()}\n```").classes("p-3")

                # Right Column: Interactive Code Editor & Test Runner
                with ui.column().classes("w-full lg:w-7/12 gap-4"):
                    with ui.card().classes("pip-card w-full p-6 gap-4"):
                        with ui.row().classes("w-full justify-between items-center"):
                            ui.label("PYTHON CODE EDITOR").classes("text-xs font-semibold text-[#161616]")
                            status_chip = ui.label("Ready for Testing").classes("text-[10px] font-mono bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-0.5 rounded")

                        editor = ui.textarea(value=current_exercise.starter_code.strip()).classes(
                            "python-editor w-full"
                        ).props("outlined rows=14 spellcheck=false")

                        with ui.row().classes("w-full justify-between items-center pt-2 border-t border-[#E2DCD2] flex-wrap gap-2"):
                            ui.button("Reset Starter Code", on_click=lambda: editor.set_value(current_exercise.starter_code.strip())).classes("btn-subtle text-xs px-3 py-1.5")
                            validate_btn = ui.button("Validate Solution ▶").classes("btn-blue text-xs font-semibold px-4 py-2")

                        # Test Assertion Results Display
                        test_results_container = ui.column().classes("w-full bg-[#F5F2EC] border border-[#E2DCD2] rounded p-4 gap-3 mt-1")
                        with test_results_container:
                            ui.label("TEST ASSERTIONS & VALIDATION REPORT").classes("text-[10px] font-bold text-[#8C857D] font-mono")
                            test_cases_list = ui.column().classes("w-full gap-2")

                        def handle_validation():
                            code = editor.value
                            eval_res = evaluate_exercise(
                                code,
                                current_exercise.test_cases,
                                current_exercise.expected_substrings
                            )
                            passed = eval_res["passed"]

                            # Clear and update test results UI
                            test_cases_list.clear()
                            with test_cases_list:
                                for tc in eval_res.get("test_results", []):
                                    is_p = tc.get("passed", False)
                                    badge_bg = "bg-[#2D6A4F] text-white" if is_p else "bg-[#9D3A3A] text-white"
                                    badge_icon = "✓ Passed" if is_p else "✗ Failed"

                                    with ui.row().classes("w-full justify-between items-center p-2.5 bg-white border border-[#E2DCD2] rounded"):
                                        with ui.column().classes("gap-0.5"):
                                            ui.label(tc.get("description", "Test Case")).classes("text-xs font-semibold text-[#161616]")
                                            if tc.get("actual"):
                                                ui.label(f"Output: {tc['actual']}").classes("text-[10px] font-mono text-[#5E5A55]")
                                            if tc.get("error"):
                                                ui.label(f"Error: {tc['error']}").classes("text-[10px] font-mono text-[#9D3A3A]")
                                        ui.label(badge_icon).classes(f"text-[10px] font-mono font-bold px-2 py-0.5 rounded {badge_bg}")

                            if passed:
                                status_chip.set_text("PASSED ALL ASSERTIONS")
                                status_chip.classes(replace="bg-[#2D6A4F] text-white")
                                ui.notify("All test assertions passed! Exercise recorded.", color="positive")
                            else:
                                status_chip.set_text("VALIDATION FAILED")
                                status_chip.classes(replace="bg-[#9D3A3A] text-white")
                                ui.notify("Some test assertions failed. Review the output below.", color="negative")

                            # Persist to database
                            with get_db() as db_session:
                                record_practice_attempt(
                                    db_session,
                                    learner_id,
                                    current_module.id,
                                    current_exercise.id,
                                    passed,
                                    code,
                                    eval_res.get("message", "")
                                )

                        validate_btn.on_click(handle_validation)
