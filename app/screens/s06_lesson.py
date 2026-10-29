"""
Production Lesson Workspace: Read → Watch → Experiment → Practice → Check.
Authoritative Pip Learn implementation adhering to:
- Unified, stable learning workspace
- Five-stage linear educational journey
- Real embedded Corey Schafer YouTube videos with fallback
- Two-column balanced experiment workbench with high-contrast editor
- Three meaningful coding challenges per lesson with real tests
- Focused, one-question-at-a-time checkpoint assessment with retry behavior
- Complete state persistence to SQLite database
"""
import json
from html import escape
from typing import List, Tuple

from nicegui import ui

from app.components.layout import page_shell
from app.components.video_player import render_video_player
from app.curriculum.challenges import get_lesson_challenges
from app.curriculum.checkpoints import get_lesson_checkpoints
from app.curriculum.loader import get_lesson, get_module
from app.curriculum.videos import get_lesson_video
from app.database.connection import get_db
from app.database.crud import (
    get_lesson_activity,
    mark_lesson_complete,
    record_practice_attempt,
    update_lesson_activity,
)
from app.auth.guards import require_auth
import app.navigation.nav as nav
from app.execution.evaluator import evaluate_exercise
from app.execution.runner import run_python_code


STAGES = ["read", "watch", "experiment", "practice", "check"]


from app.curriculum.sections import get_lesson_reading_sections

_reading_sections = get_lesson_reading_sections


def render_lesson_screen(module_id: int, lesson_id: str, stage: str = None):
    with get_db() as db:
        auth = require_auth(db, active_route=f"/module/{module_id}/lesson/{lesson_id}")
        if not auth:
            return
        user, learner = auth
        learner_id = learner.id

    module = get_module(module_id)
    lesson = get_lesson(module_id, lesson_id)

    with page_shell(active_route="/curriculum", compact=True, show_footer=False):
        if not module or not lesson:
            with ui.column().classes("w-full max-w-xl mx-auto py-16 text-center gap-4"):
                ui.label("Lesson Not Found").classes("font-serif text-3xl")
                ui.label("The requested lesson does not exist in the curriculum.").classes("text-sm text-[#5E5A55]")
                ui.button("← Return to Curriculum", on_click=nav.go_to_curriculum).classes("btn-blue mx-auto")
            return

        lesson_ids = [item.id for item in module.lessons]
        lesson_index = lesson_ids.index(lesson.id)
        previous_id = lesson_ids[lesson_index - 1] if lesson_index > 0 else None
        next_id = lesson_ids[lesson_index + 1] if lesson_index + 1 < len(lesson_ids) else None

        # Preload curriculum components
        sections = _reading_sections(module, lesson)
        video_info = get_lesson_video(lesson.id)
        challenges = get_lesson_challenges(lesson.id, lesson.practice_tasks or module.practice_exercises)
        checkpoints = lesson.checkpoint_questions or get_lesson_checkpoints(lesson.id, lesson.mini_checkpoint)

        # Fetch persisted activity and completion from SQLite
        with get_db() as db:
            from app.database.models import LessonCompletion
            is_completed = db.query(LessonCompletion).filter(
                LessonCompletion.learner_id == learner_id,
                LessonCompletion.module_id == module.id,
                LessonCompletion.lesson_id == lesson.id,
            ).first() is not None

            activity = get_lesson_activity(db, learner_id, module.id, lesson.id)
            activity_id = activity.id

            raw_practice = json.loads(activity.practice_state_json or "{}")
            raw_checkpoint = json.loads(activity.checkpoint_state_json or "{}")

            # Deterministic stage resolution:
            # 1. Explicit stage parameter requested in URL always takes precedence
            if stage in STAGES:
                init_stage = stage
            elif is_completed:
                # Revisiting a completed lesson starts at Read for review
                init_stage = "read"
            elif activity.stage in STAGES:
                # In-progress lesson: resume at the learner's actual saved stage
                init_stage = activity.stage
            else:
                init_stage = "read"

            saved_state = {
                "stage": init_stage,
                "reading_section": 0 if (is_completed and stage is None) else (activity.reading_section or 0),
                "video_status": activity.video_status or "not_started",
                "notes": activity.notes or "",
                "experiment_code": activity.experiment_code or lesson.executable_code,
                "experiment_attempted": activity.experiment_attempted or False,
                "practice": raw_practice,
                "checkpoint": raw_checkpoint,
            }

        def persist_activity(**kwargs):
            """Persist lesson activity state to SQLite database."""
            with get_db() as db:
                update_lesson_activity(db, activity_id, **kwargs)

        # State containers
        current_read_idx = {"value": max(0, min(saved_state["reading_section"], len(sections) - 1))}

        # Active challenge points to the first unpassed challenge in practice
        first_unpassed_challenge_idx = 0
        for c_idx, ch in enumerate(challenges):
            if not saved_state["practice"].get(ch.id, {}).get("passed", False):
                first_unpassed_challenge_idx = c_idx
                break
        else:
            first_unpassed_challenge_idx = max(0, len(challenges) - 1)
        active_challenge_idx = {"value": first_unpassed_challenge_idx}

        # Active checkpoint points to the first unpassed question
        checkpoint_answers = dict(saved_state["checkpoint"])  # e.g. {"q_0": {"choice": 1, "passed": True}}
        first_unpassed_ckpt_idx = 0
        for q_idx in range(len(checkpoints)):
            if not checkpoint_answers.get(f"q_{q_idx}", {}).get("passed", False):
                first_unpassed_ckpt_idx = q_idx
                break
        else:
            first_unpassed_ckpt_idx = max(0, len(checkpoints) - 1)
        active_checkpoint_idx = {"value": first_unpassed_ckpt_idx}

        # Main Workspace Container
        with ui.column().classes("lesson-shell"):

            # 1. Lesson Context Header Card
            with ui.row().classes("lesson-header-card w-full items-center justify-between gap-4 flex-wrap"):
                with ui.row().classes("items-center gap-3 min-w-0"):
                    ui.button(f"← {module.code}: {module.title}", on_click=lambda: nav.open_module(module.id)).props("flat dense").classes(
                        "text-xs text-[#396DAB] hover:underline font-semibold normal-case p-0"
                    )
                    ui.label("·").classes("text-xs text-[#8C857D]")
                    ui.label(f"LESSON {lesson_index + 1} OF {len(module.lessons)}").classes("editorial-eyebrow")
                    ui.label("—").classes("text-xs text-[#8C857D]")
                    ui.label(lesson.title).classes("font-serif text-2xl leading-none text-[#161616]")
                ui.label(lesson.subtitle).classes("hidden lg:block text-xs text-[#5E5A55] max-w-md truncate")

            # 2. Stage Navigation Tabs
            stage_tabs_list = [
                ("01", "read", "Read"),
                ("02", "watch", "Watch"),
                ("03", "experiment", "Experiment"),
                ("04", "practice", "Practice"),
                ("05", "check", "Check"),
            ]
            stage_tab_elements = {}

            with ui.tabs(value=saved_state["stage"]).props("dense no-caps align=justify").classes("lesson-tabs w-full") as tabs:
                for num, key, label in stage_tabs_list:
                    stage_tab_elements[key] = ui.tab(key, label=f"{num} · {label}")

            def advance_to_stage(target_stage: str):
                if target_stage not in STAGES or saved_state.get("stage") == target_stage:
                    return
                saved_state["stage"] = target_stage
                tabs.set_value(target_stage)
                persist_activity(stage=target_stage)
                # Keep browser URL synchronized with current stage for refresh & history
                ui.run_javascript(f"try {{ window.history.replaceState(null, '', '/module/{module.id}/lesson/{lesson.id}?stage={target_stage}'); }} catch(e) {{}}")
                if target_stage != "watch":
                    ui.run_javascript(
                        "document.querySelectorAll('iframe.youtube-frame').forEach(function(f) {"
                        "  try { f.contentWindow.postMessage('{\"event\":\"command\",\"func\":\"pauseVideo\",\"args\":\"\"}', '*'); } catch(e) {}"
                        "});"
                    )
                render_lesson_navigation.refresh()

            def on_stage_change(event):
                if event.value in STAGES and saved_state.get("stage") != event.value:
                    saved_state["stage"] = event.value
                    persist_activity(stage=event.value)
                    ui.run_javascript(f"try {{ window.history.replaceState(null, '', '/module/{module.id}/lesson/{lesson.id}?stage={event.value}'); }} catch(e) {{}}")
                    if event.value != "watch":
                        ui.run_javascript(
                            "document.querySelectorAll('iframe.youtube-frame').forEach(function(f) {"
                            "  try { f.contentWindow.postMessage('{\"event\":\"command\",\"func\":\"pauseVideo\",\"args\":\"\"}', '*'); } catch(e) {}"
                            "});"
                        )
                    render_lesson_navigation.refresh()

            tabs.on_value_change(on_stage_change)

            # 3. Tab Panels Container (Read, Watch, Experiment, Practice, Check)
            with ui.tab_panels(tabs, value=saved_state["stage"]).props("animated=false keep-alive").classes("lesson-panels w-full"):

                # =========================================================
                # STAGE 01: READ
                # =========================================================
                with ui.tab_panel(stage_tab_elements["read"]).classes("lesson-panel"):
                    @ui.refreshable
                    def render_reading_view():
                        pos = current_read_idx["value"]
                        title, eyebrow, body_md = sections[pos]

                        with ui.column().classes("reading-container"):
                            # Section Progress Tracker
                            with ui.row().classes("w-full items-center justify-between gap-2"):
                                ui.label(eyebrow).classes("editorial-eyebrow")
                                ui.label(f"SECTION {pos + 1} OF {len(sections)}").classes("text-xs font-mono text-[#8C857D]")

                            with ui.element("div").classes("reading-progress-track"):
                                ui.element("div").classes("reading-progress-fill").style(
                                    f"width: {((pos + 1) / len(sections)) * 100}%"
                                )

                            # Section Stepper Pills
                            with ui.row().classes("w-full items-center gap-2 flex-wrap"):
                                for s_idx, (s_title, _, _) in enumerate(sections):
                                    is_cur = s_idx == pos
                                    pill = ui.button(
                                        f"{s_idx + 1}. {s_title}",
                                        on_click=lambda idx=s_idx: jump_to_section(idx)
                                    ).props("flat dense").classes(
                                        f"reading-pill {'active' if is_cur else ''}"
                                    )

                            # Section Content Card
                            with ui.column().classes("workbench-card w-full py-6 px-7"):
                                ui.markdown(body_md).classes("lesson-prose w-full")

                            # Bottom Section Navigation Controls
                            with ui.row().classes("w-full items-center justify-between pt-2 pb-6"):
                                if pos > 0:
                                    ui.button("← Previous Section", on_click=lambda: step_section(-1)).props("outline").classes("btn-subtle")
                                else:
                                    ui.element("div")

                                if pos < len(sections) - 1:
                                    ui.button("Next Section →", on_click=lambda: step_section(1)).classes("btn-blue")
                                else:
                                    next_label = "Continue to Watch Stage →" if video_info else "Continue to Experiment Stage →"
                                    ui.button(next_label, on_click=lambda: advance_to_stage("watch" if video_info else "experiment")).classes("btn-blue")

                    def step_section(delta: int):
                        new_pos = current_read_idx["value"] + delta
                        if 0 <= new_pos < len(sections):
                            current_read_idx["value"] = new_pos
                            persist_activity(reading_section=new_pos, stage="read")
                            render_reading_view.refresh()

                    def jump_to_section(idx: int):
                        if 0 <= idx < len(sections):
                            current_read_idx["value"] = idx
                            persist_activity(reading_section=idx, stage="read")
                            render_reading_view.refresh()

                    render_reading_view()

                # =========================================================
                # STAGE 02: WATCH
                # =========================================================
                with ui.tab_panel(stage_tab_elements["watch"]).classes("lesson-panel"):
                    with ui.row().classes("workspace-grid"):
                        # Video Player Column
                        with ui.column().classes("workspace-pane-left"):
                            with ui.column().classes("workbench-card w-full gap-3"):
                                ui.label("VIDEO TUTORIAL EMBED").classes("editorial-eyebrow")

                                status_label = None

                                def handle_playback_start():
                                    saved_state["video_status"] = "started"
                                    persist_activity(video_status="started")
                                    if status_label:
                                        status_label.set_text("Status: Video active in embedded YouTube player")

                                render_video_player(
                                    video_info=video_info,
                                    saved_video_status=saved_state["video_status"],
                                    on_playback_started=handle_playback_start,
                                    on_status_change=lambda msg: status_label.set_text(msg) if status_label else None,
                                )

                                with ui.row().classes("w-full items-center justify-between text-xs pt-1"):
                                    status_label = ui.label(
                                        "Status: Ready to play" if saved_state["video_status"] == "not_started" else "Status: Playback initialized"
                                    ).classes("text-xs text-[#5E5A55]")
                                    with ui.row().classes("items-center gap-3"):
                                        if video_info:
                                            ui.label(f"Duration: {video_info.duration}").classes("font-mono text-[#8C857D]")
                                            ui.link(
                                                "Open on YouTube ↗",
                                                f"https://www.youtube.com/watch?v={video_info.video_id}",
                                                new_tab=True,
                                            ).classes("text-[#396DAB] hover:underline font-medium")

                        # Video Study Notes Column
                        with ui.column().classes("workspace-pane-right"):
                            with ui.column().classes("workbench-card w-full gap-4"):
                                with ui.column().classes("gap-1"):
                                    ui.label("STUDY COMPANION & NOTES").classes("editorial-eyebrow")
                                    ui.label(video_info.title if video_info else "Continue with Hands-on Experiment").classes("font-serif text-2xl text-[#161616]")
                                    ui.label(f"Creator: {video_info.instructor}" if video_info else "Self-Paced Guided Flow").classes("text-xs font-semibold text-[#396DAB]")

                                if video_info:
                                    ui.label(video_info.relevance).classes("text-sm text-[#5E5A55] leading-relaxed")
                                    with ui.column().classes("gap-1 bg-[#E9F1F9] p-3 rounded-md border-l-4 border-[#4F83BC]"):
                                        ui.label("What to observe in the video:").classes("text-xs font-semibold text-[#161616]")
                                        ui.markdown("- Notice how syntax is entered and executed directly.\n- Observe the terminal output and common mistakes demonstrated.\n- Compare the video examples with your written lesson code.").classes("text-xs text-[#5E5A55]")

                                with ui.row().classes("w-full items-center justify-between mt-2"):
                                    ui.label("Your Study Notes").classes("text-xs font-semibold text-[#161616]")
                                    save_indicator = ui.label("Autosaved to SQLite").classes("text-[11px] font-mono text-[#8C857D]")

                                notes_input = ui.textarea(
                                    placeholder="Take notes on key ideas, syntax tricks, or questions...",
                                    value=saved_state["notes"],
                                ).props("outlined rows=6 spellcheck=false").classes("w-full text-sm font-sans")

                                def on_notes_change(e):
                                    val = e.value if hasattr(e, "value") else str(e)
                                    saved_state["notes"] = val
                                    persist_activity(notes=val)
                                    save_indicator.set_text("✓ Notes saved")

                                notes_input.on_value_change(on_notes_change)

                # =========================================================
                # STAGE 03: EXPERIMENT
                # =========================================================
                with ui.tab_panel(stage_tab_elements["experiment"]).classes("lesson-panel"):
                    with ui.row().classes("workspace-grid"):
                        # Experiment Instructions
                        with ui.column().classes("workspace-pane-left"):
                            with ui.column().classes("workbench-card w-full gap-4"):
                                ui.label("GUIDED LIVE EXPERIMENT").classes("editorial-eyebrow")
                                experiment = lesson.experiment
                                ui.label(experiment.title if experiment else "Predict, Modify, Then Execute").classes("font-serif text-2xl text-[#161616]")
                                ui.label(
                                    experiment.prediction_prompt if experiment else "Modify values in the program to test your mental model. Before clicking Run, predict what the Python interpreter will print."
                                ).classes("text-sm text-[#5E5A55] leading-relaxed")

                                ui.label("Your Output Prediction:").classes("text-xs font-semibold text-[#161616]")
                                prediction_box = ui.input(
                                    placeholder="e.g. I predict line 2 will output...",
                                ).props("outlined dense").classes("w-full text-sm")

                                with ui.column().classes("bg-[#E9F1F9] border-l-4 border-[#4F83BC] p-4 rounded-r gap-1.5"):
                                    ui.label("Suggested Experiments to Try:").classes("font-semibold text-xs text-[#161616]")
                                    instructions = experiment.instructions if experiment else [
                                        "Predict the output", "Run unchanged code", "Observe the result",
                                        "Modify one value", "Run again and explain the difference",
                                    ]
                                    ui.markdown("\n".join(f"{i}. {item}" for i, item in enumerate(instructions, 1))).classes("text-xs text-[#5E5A55]")
                                if experiment:
                                    ui.label(f"Reference behavior: {experiment.expected_output}").classes("text-xs font-mono text-[#5E5A55] whitespace-pre-wrap")


                        # Code Editor & Terminal Pane
                        with ui.column().classes("workspace-pane-right"):
                            with ui.column().classes("workbench-card w-full gap-3"):
                                with ui.row().classes("w-full items-center justify-between"):
                                    ui.label("EXPERIMENT.PY").classes("terminal-header")
                                    with ui.row().classes("items-center gap-2"):
                                        reset_exp_btn = ui.button("Reset Code").props("outline dense").classes("btn-subtle text-xs")
                                        run_exp_btn = ui.button("Run Code ▶").classes("btn-blue text-xs")

                                exp_editor = ui.textarea(
                                    value=saved_state["experiment_code"]
                                ).props("outlined rows=11 spellcheck=false").classes("python-editor w-full")

                                def on_exp_code_change(e):
                                    saved_state["experiment_code"] = e.value
                                    persist_activity(experiment_code=e.value)

                                exp_editor.on_value_change(on_exp_code_change)

                                reset_exp_btn.on_click(lambda: exp_editor.set_value(lesson.experiment.starter_code if lesson.experiment else lesson.executable_code))

                                ui.label("TERMINAL OUTPUT (ISOLATED EXECUTION)").classes("terminal-header mt-1")
                                exp_output = ui.label("Click 'Run Code ▶' to execute this script in an isolated Python subprocess.").classes(
                                    "code-output w-full whitespace-pre-wrap"
                                )
                                exp_diagnostic = ui.label("").classes("text-xs text-[#9D3A3A] hidden")

                                def execute_experiment():
                                    run_exp_btn.disable()
                                    run_exp_btn.set_text("Running…")
                                    res = run_python_code(exp_editor.value)
                                    if res["success"]:
                                        exp_output.set_text(res["stdout"].strip() if res["stdout"].strip() else "(Execution completed with no output to stdout)")
                                        exp_output.classes(replace="code-output w-full whitespace-pre-wrap is-success")
                                        exp_diagnostic.set_visibility(False)
                                    else:
                                        exp_output.set_text(res["stderr"].strip())
                                        exp_output.classes(replace="code-output w-full whitespace-pre-wrap is-error")
                                        if res.get("explanation"):
                                            exp_diagnostic.set_text(f"Diagnostic Insight: {res['explanation']}")
                                            exp_diagnostic.set_visibility(True)

                                    saved_state["experiment_attempted"] = True
                                    persist_activity(experiment_code=exp_editor.value, experiment_attempted=True)
                                    run_exp_btn.enable()
                                    run_exp_btn.set_text("Run Code ▶")

                                run_exp_btn.on_click(execute_experiment)

                # =========================================================
                # STAGE 04: PRACTICE
                # =========================================================
                with ui.tab_panel(stage_tab_elements["practice"]).classes("lesson-panel"):
                    @ui.refreshable
                    def render_practice_view():
                        active_idx = active_challenge_idx["value"]
                        current_ex = challenges[active_idx]
                        current_ex_saved = saved_state["practice"].get(current_ex.id, {})

                        with ui.column().classes("w-full gap-4"):
                            # Challenge Stepper Selector (Separately Refreshable)
                            @ui.refreshable
                            def challenge_selector():
                                with ui.row().classes("w-full items-center gap-2 flex-wrap"):
                                    for c_idx, ch in enumerate(challenges):
                                        is_active = c_idx == active_challenge_idx["value"]
                                        ch_state = saved_state["practice"].get(ch.id, {})
                                        has_passed = ch_state.get("passed", False)
                                        check_badge = " ✓" if has_passed else ""
                                        ui.button(
                                            f"Challenge {c_idx + 1}: {ch.difficulty}{check_badge}",
                                            on_click=lambda i=c_idx: switch_challenge(i)
                                        ).props("dense flat").classes(
                                            f"challenge-tab-btn {'active' if is_active else ''} {'passed' if has_passed else ''}"
                                        )

                            challenge_selector()

                            with ui.row().classes("workspace-grid"):
                                # Left Column: Challenge Description & Hints
                                with ui.column().classes("workspace-pane-left"):
                                    with ui.column().classes("workbench-card w-full gap-3"):
                                        with ui.row().classes("items-center justify-between"):
                                            ui.label(f"{current_ex.difficulty.upper()} CHALLENGE").classes("editorial-eyebrow")
                                            if current_ex_saved.get("passed"):
                                                ui.label("✓ VERIFIED PASSED").classes("text-xs font-semibold text-[#2D6A4F]")

                                        ui.label(current_ex.title).classes("font-serif text-2xl text-[#161616]")
                                        ui.markdown(current_ex.problem_statement).classes("text-sm text-[#5E5A55] leading-relaxed")

                                        with ui.column().classes("gap-1 bg-[#EFEAE2] p-3 rounded"):
                                            ui.label("Expected Behavior & Output:").classes("text-xs font-semibold text-[#161616]")
                                            ui.label(current_ex.input_output_expectations).classes("text-xs font-mono text-[#5E5A55] whitespace-pre-wrap")

                                        if current_ex.hints:
                                            ui.label("Progressive Hints").classes("text-xs font-semibold text-[#161616] mt-1")
                                            for h_idx, hint_text in enumerate(current_ex.hints, 1):
                                                with ui.expansion(f"Hint {h_idx}").classes("w-full text-xs border border-[#E2DCD2] rounded"):
                                                    ui.label(hint_text).classes("p-3 text-xs text-[#5E5A55]")


                                # Right Column: Code Editor & Automated Test Evaluator
                                with ui.column().classes("workspace-pane-right"):
                                    with ui.column().classes("workbench-card w-full gap-3"):
                                        with ui.row().classes("w-full items-center justify-between"):
                                            ui.label("SOLUTION.PY").classes("terminal-header")
                                            with ui.row().classes("items-center gap-2"):
                                                reset_prac_btn = ui.button("Reset").props("outline dense").classes("btn-subtle text-xs")
                                                test_prac_btn = ui.button("Run Tests ▶").classes("btn-blue text-xs")

                                        starter = current_ex_saved.get("code", current_ex.starter_code)
                                        prac_editor = ui.textarea(value=starter).props("outlined rows=11 spellcheck=false").classes("python-editor w-full")

                                        def on_prac_code_change(e):
                                            saved_state["practice"].setdefault(current_ex.id, {})["code"] = e.value
                                            persist_activity(practice_state_json=json.dumps(saved_state["practice"]))

                                        prac_editor.on_value_change(on_prac_code_change)
                                        reset_prac_btn.on_click(lambda: prac_editor.set_value(current_ex.starter_code))

                                        ui.label("AUTOMATED TEST RESULTS").classes("terminal-header mt-1")
                                        results_container = ui.column().classes("w-full gap-2")

                                        with results_container:
                                            if current_ex_saved.get("passed"):
                                                ui.label("✓ All tests passed for this challenge.").classes("text-xs text-[#2D6A4F] font-semibold")
                                            else:
                                                ui.label("Click 'Run Tests ▶' to evaluate your solution against test assertions.").classes("text-xs text-[#5E5A55]")

                                        def execute_practice_tests():
                                            test_prac_btn.disable()
                                            test_prac_btn.set_text("Evaluating…")
                                            eval_res = evaluate_exercise(
                                                prac_editor.value,
                                                current_ex.test_cases,
                                                current_ex.expected_substrings,
                                            )
                                            # Update persisted state
                                            saved_state["practice"][current_ex.id] = {
                                                "code": prac_editor.value,
                                                "passed": eval_res["passed"],
                                            }
                                            persist_activity(practice_state_json=json.dumps(saved_state["practice"]))

                                            with get_db() as db:
                                                record_practice_attempt(
                                                    db,
                                                    learner_id,
                                                    module.id,
                                                    current_ex.id,
                                                    eval_res["passed"],
                                                    prac_editor.value,
                                                    eval_res["message"],
                                                )

                                            results_container.clear()
                                            with results_container:
                                                passed_cases = sum(1 for c in eval_res.get("test_results", []) if c["passed"])
                                                total_cases = len(eval_res.get("test_results", [])) or 1

                                                if eval_res["passed"]:
                                                    with ui.column().classes("w-full bg-[#F0FDF4] border border-[#86EFAC] p-3 rounded gap-1"):
                                                        ui.label(f"✓ {passed_cases} of {total_cases} Tests Passed!").classes("font-semibold text-sm text-[#2D6A4F]")
                                                        ui.label(eval_res["message"]).classes("text-xs text-[#2D6A4F]")
                                                else:
                                                    with ui.column().classes("w-full bg-[#FEF2F2] border border-[#FECACA] p-3 rounded gap-1"):
                                                        ui.label(f"✗ Test Verification Failed ({passed_cases}/{total_cases} passed)").classes("font-semibold text-sm text-[#9D3A3A]")
                                                        ui.label(eval_res["message"]).classes("text-xs text-[#9D3A3A]")

                                                for t_row in eval_res.get("test_results", []):
                                                    icon = "✓" if t_row["passed"] else "✗"
                                                    color = "text-[#2D6A4F]" if t_row["passed"] else "text-[#9D3A3A]"
                                                    with ui.row().classes(f"items-center gap-2 text-xs {color}"):
                                                        ui.label(f"{icon} {t_row['description']}")
                                                    if t_row.get("error"):
                                                        ui.label(t_row["error"]).classes("text-[11px] font-mono text-[#9D3A3A] whitespace-pre-wrap ml-4")

                                            test_prac_btn.enable()
                                            test_prac_btn.set_text("Run Tests ▶")
                                            # Refresh challenge selector to display the checkmark
                                            challenge_selector.refresh()

                                        test_prac_btn.on_click(execute_practice_tests)

                    def switch_challenge(idx: int):
                        active_challenge_idx["value"] = idx
                        render_practice_view.refresh()

                    render_practice_view()

                # =========================================================
                # STAGE 05: CHECK (FOCUSED ONE-QUESTION ASSESSMENT)
                # =========================================================
                with ui.tab_panel(stage_tab_elements["check"]).classes("lesson-panel"):
                    @ui.refreshable
                    def render_check_view():
                        q_idx = active_checkpoint_idx["value"]
                        total_q = len(checkpoints)

                        # Check if learner has completed all checkpoint questions
                        questions_passed = total_q > 0 and all(
                            checkpoint_answers.get(f"q_{i}", {}).get("passed", False)
                            for i in range(total_q)
                        )
                        practice_passed = all(
                            saved_state["practice"].get(challenge.id, {}).get("passed", False)
                            for challenge in challenges
                        )
                        all_passed = questions_passed and saved_state["experiment_attempted"] and practice_passed

                        with ui.column().classes("check-card"):
                            if all_passed:
                                # Celebratory Completion State
                                with ui.column().classes("w-full text-center items-center py-6 gap-4"):
                                    ui.icon("check_circle", size="4rem", color="positive")
                                    ui.label("LESSON CERTIFIED COMPLETE").classes("editorial-eyebrow")
                                    ui.label("Conceptual Mastery Confirmed!").classes("font-serif text-3xl text-[#161616]")
                                    ui.label(
                                        f"You have verified your understanding across Read, Watch, Experiment, Practice, and Check for {lesson.title}."
                                    ).classes("text-sm text-[#5E5A55] max-w-lg leading-relaxed")

                                    with ui.row().classes("gap-3 pt-4"):
                                        ui.button(
                                            "Review Questions",
                                            on_click=lambda: restart_checkpoint()
                                        ).props("outline").classes("btn-subtle")

                                        ui.button(
                                            "Return to Module Overview",
                                            on_click=lambda: nav.open_module_overview(module.id)
                                        ).props("outline").classes("btn-subtle")
                                return

                            # Active Question Assessment Flow
                            curr_q = checkpoints[q_idx]
                            q_key = f"q_{q_idx}"
                            current_saved_ans = checkpoint_answers.get(q_key, {})

                            # Question Header & Progress
                            with ui.row().classes("w-full items-center justify-between"):
                                ui.label(f"QUESTION {q_idx + 1} OF {total_q}").classes("editorial-eyebrow")
                                ui.label(f"Mastery Checkpoint").classes("text-xs text-[#8C857D] font-mono")

                            ui.label(curr_q.question).classes("font-serif text-2xl text-[#161616] leading-snug")

                            # Options Radio Group
                            radio_group = ui.radio(
                                curr_q.options,
                                value=current_saved_ans.get("choice_text"),
                            ).classes("quiz-options-group w-full")

                            # Feedback Banner (Hidden initially unless previously attempted)
                            feedback_box = ui.column().classes("w-full hidden")

                            # Bottom Action Row
                            with ui.row().classes("w-full items-center justify-between pt-4"):
                                with ui.row().classes("items-center gap-2"):
                                    if q_idx > 0:
                                        ui.button("← Previous Question", on_click=lambda: switch_question(q_idx - 1)).props("outline dense").classes("btn-subtle text-xs")

                                check_action_btn = ui.button("Check Answer").classes("btn-blue")
                                continue_action_btn = ui.button(
                                    "Next Question →" if q_idx < total_q - 1 else "Complete & Certify Lesson →"
                                ).classes("btn-blue hidden")

                            def on_check():
                                if not radio_group.value:
                                    ui.notify("Please select an answer first.", color="warning")
                                    return
                                selected_index = curr_q.options.index(radio_group.value)
                                is_correct = (selected_index == curr_q.correct_index)
                                attempts = checkpoint_answers.get(q_key, {}).get("attempts", 0) + 1

                                checkpoint_answers[q_key] = {
                                    "choice_index": selected_index,
                                    "choice_text": radio_group.value,
                                    "passed": is_correct,
                                    "attempts": attempts,
                                }
                                persist_activity(checkpoint_state_json=json.dumps(checkpoint_answers))

                                feedback_box.clear()
                                feedback_box.classes(remove="hidden")

                                with feedback_box:
                                    if is_correct:
                                        with ui.column().classes("check-feedback-banner is-correct w-full"):
                                            ui.label("✓ Correct!").classes("font-semibold text-sm text-[#2D6A4F]")
                                            ui.label(curr_q.explanation).classes("text-xs text-[#2D6A4F] leading-relaxed")
                                        check_action_btn.classes(add="hidden")
                                        continue_action_btn.classes(remove="hidden")
                                    else:
                                        with ui.column().classes("check-feedback-banner is-incorrect w-full"):
                                            ui.label("Not quite yet — Try again").classes("font-semibold text-sm text-[#9D3A3A]")
                                            ui.label(curr_q.explanation).classes("text-xs text-[#9D3A3A] leading-relaxed")
                                            ui.label(f"Attempt {attempts}. Review the relevant Read section, retry its Practice activity, then answer again.").classes("text-[11px] text-[#5E5A55]")

                            def on_continue():
                                if q_idx < total_q - 1:
                                    switch_question(q_idx + 1)
                                else:
                                    # Certification requires evidence from every active stage,
                                    # not merely clicking through the checkpoint.
                                    practice_passed = all(
                                        saved_state["practice"].get(challenge.id, {}).get("passed", False)
                                        for challenge in challenges
                                    )
                                    if not saved_state["experiment_attempted"] or not practice_passed:
                                        missing = []
                                        if not saved_state["experiment_attempted"]:
                                            missing.append("run the Experiment")
                                        if not practice_passed:
                                            missing.append("pass all Practice activities")
                                        ui.notify("Before certification, " + " and ".join(missing) + ".", color="warning")
                                        return
                                    with get_db() as db:
                                        mark_lesson_complete(db, learner_id, module.id, lesson.id, len(module.lessons))
                                    render_check_view.refresh()
                                    render_lesson_navigation.refresh()

                            check_action_btn.on_click(on_check)
                            continue_action_btn.on_click(on_continue)

                            # If already passed this question previously, reveal continue
                            if current_saved_ans.get("passed"):
                                feedback_box.clear()
                                feedback_box.classes(remove="hidden")
                                with feedback_box:
                                    with ui.column().classes("check-feedback-banner is-correct w-full"):
                                        ui.label("✓ Answer Verified").classes("font-semibold text-sm text-[#2D6A4F]")
                                        ui.label(curr_q.explanation).classes("text-xs text-[#2D6A4F]")
                                check_action_btn.classes(add="hidden")
                                continue_action_btn.classes(remove="hidden")

                    def switch_question(idx: int):
                        active_checkpoint_idx["value"] = idx
                        render_check_view.refresh()

                    def restart_checkpoint():
                        checkpoint_answers.clear()
                        persist_activity(checkpoint_state_json=json.dumps({}))
                        active_checkpoint_idx["value"] = 0
                        render_check_view.refresh()
                        render_lesson_navigation.refresh()

                    render_check_view()

            # 4. Bottom Shared Lesson Navigation Footer (Left: Back, Center: Progress, Right: Next)
            @ui.refreshable
            def render_lesson_navigation():
                cur_stage = saved_state.get("stage") if saved_state.get("stage") in STAGES else (tabs.value if tabs.value in STAGES else "read")
                if cur_stage not in STAGES:
                    cur_stage = "read"
                cur_idx = STAGES.index(cur_stage)
                stage_titles = {
                    "read": "Read",
                    "watch": "Watch",
                    "experiment": "Experiment",
                    "practice": "Practice",
                    "check": "Check",
                }

                with ui.row().classes("lesson-nav-footer w-full items-center justify-between gap-4"):
                    # Left: Back / Previous Stage
                    if cur_idx > 0:
                        prev_stage = STAGES[cur_idx - 1]
                        if prev_stage == "watch" and not video_info:
                            prev_stage = "read"
                        ui.button(
                            f"← Back: {stage_titles[prev_stage]}",
                            on_click=lambda _, s=prev_stage: advance_to_stage(s),
                        ).props("outline no-caps").classes("btn-subtle text-xs font-semibold px-4 py-2")
                    else:
                        if previous_id:
                            ui.button(
                                "← Previous Lesson",
                                on_click=lambda: nav.open_lesson(module.id, previous_id, "read"),
                            ).props("outline no-caps").classes("btn-subtle text-xs font-semibold px-4 py-2")
                        else:
                            ui.button(
                                f"← {module.code} Overview",
                                on_click=lambda: nav.open_module(module.id),
                            ).props("outline no-caps").classes("btn-subtle text-xs font-semibold px-4 py-2")

                    # Center: Current stage & learning progress
                    with ui.row().classes("items-center gap-2 flex-wrap justify-center"):
                        ui.label(f"STAGE 0{cur_idx + 1} OF 05").classes("editorial-eyebrow")
                        ui.label("·").classes("text-xs text-[#8C857D]")
                        ui.label(stage_titles[cur_stage].upper()).classes("text-xs font-semibold text-[#161616]")
                        ui.label("·").classes("text-xs text-[#8C857D]")
                        ui.label("Autosaved to SQLite").classes("text-[11px] font-mono text-[#8C857D]")

                    # Right: Next Stage / Continue
                    if cur_idx < len(STAGES) - 1:
                        next_stage = STAGES[cur_idx + 1]
                        if next_stage == "watch" and not video_info:
                            next_stage = "experiment"

                        def handle_next(target: str):
                            if cur_stage == "watch":
                                persist_activity(notes=saved_state["notes"])
                            elif cur_stage == "experiment":
                                persist_activity(experiment_code=saved_state["experiment_code"])
                            advance_to_stage(target)

                        ui.button(
                            f"Next Stage: {stage_titles[next_stage]} →",
                            on_click=lambda _, t=next_stage: handle_next(t),
                        ).classes("btn-blue text-xs font-semibold px-4 py-2")
                    else:
                        # Final stage: Check
                        questions_passed = (
                            len(checkpoints) > 0
                            and all(checkpoint_answers.get(f"q_{i}", {}).get("passed", False) for i in range(len(checkpoints)))
                        )
                        practice_passed = all(
                            saved_state["practice"].get(challenge.id, {}).get("passed", False)
                            for challenge in challenges
                        )
                        all_passed = questions_passed and saved_state["experiment_attempted"] and practice_passed
                        if all_passed:
                            if next_id:
                                ui.button(
                                    "Next Lesson →",
                                    on_click=lambda: nav.open_lesson(module.id, next_id, "read"),
                                ).classes("btn-blue text-xs font-semibold px-4 py-2")
                            else:
                                ui.button(
                                    "Module Assessment & Quiz →",
                                    on_click=lambda: nav.open_quiz(module.id),
                                ).classes("btn-blue text-xs font-semibold px-4 py-2")
                        else:
                            ui.button(
                                "Next Lesson →",
                            ).props("disabled").classes("btn-subtle text-xs font-semibold px-4 py-2 opacity-50 cursor-not-allowed").tooltip(
                                "Complete all check questions to certify this lesson."
                            )

            render_lesson_navigation()
