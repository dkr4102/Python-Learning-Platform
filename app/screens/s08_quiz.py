"""
Screen 08: Quiz / Assessment
Focused one-question-at-a-time evaluation with answer persistence, review, diagnostic scoring, and retakes.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.curriculum.loader import get_module
from app.database.connection import get_db
from app.database.crud import record_quiz_attempt
from app.auth.guards import require_auth
import app.navigation.nav as nav

def render_quiz_screen(module_id: int):
    with get_db() as db:
        auth = require_auth(db, active_route=f"/module/{module_id}/quiz")
        if not auth:
            return
        user, learner = auth
        learner_id = learner.id

    module = get_module(module_id)
    if not module:
        with page_shell(active_route="/curriculum"):
            with ui.column().classes("w-full max-w-4xl mx-auto px-6 py-20 text-center"):
                ui.label("Module not found.").classes("font-serif text-2xl")
                ui.button("Return to Curriculum", on_click=nav.go_to_curriculum).classes("btn-primary mt-4")
        return

    questions = module.quiz_questions
    total_q = len(questions)

    # Assessment reactive state
    state = {
        "current_idx": 0,       # 0 to total_q-1 is question view, total_q is review view, total_q+1 is results view
        "answers": {},          # {q_id: selected_value}
        "submitted": False,
        "results": None
    }

    with page_shell(active_route="/curriculum"):
        with ui.column().classes("w-full max-w-4xl mx-auto px-4 sm:px-6 py-8 md:py-12 gap-6"):
            # Header banner
            with ui.row().classes("w-full justify-between items-end flex-wrap gap-4 pb-4 border-b border-[#E2DCD2]"):
                with ui.column().classes("gap-1"):
                    ui.label(f"{module.code} • ACADEMIC ASSESSMENT").classes("editorial-eyebrow")
                    ui.label(f"{module.title} — Assessment").classes("editorial-title text-3xl sm:text-4xl")
                    ui.label(f"Evaluates core concepts against syllabus criteria ({module.assessment_marks} Marks). Pass threshold: 60%.").classes("editorial-lead text-sm")

                ui.button("← Return to Module", on_click=lambda: nav.open_module(module.id)).classes("btn-subtle text-xs px-3.5 py-2")

            # Main Interactive Assessment Container
            @ui.refreshable
            def render_assessment_body():
                idx = state["current_idx"]

                # ----------------------------------------------------
                # VIEW 3: RESULTS SCREEN (Post-Submission)
                # ----------------------------------------------------
                if state["submitted"] and state["results"]:
                    res = state["results"]
                    score = res["score"]
                    pct = res["percentage"]
                    passed = res["passed"]

                    with ui.column().classes("w-full gap-6"):
                        # High-level outcome card
                        with ui.card().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] p-6 sm:p-8 rounded-xl shadow-sm gap-4"):
                            with ui.row().classes("w-full justify-between items-center flex-wrap gap-4"):
                                with ui.column().classes("gap-1"):
                                    ui.label("ACADEMIC ASSESSMENT OUTCOME").classes("text-[10px] font-mono font-bold text-[#6E8098] uppercase tracking-wider")
                                    ui.label(f"Score: {score:.0f} / {total_q} ({pct:.1f}%)").classes("font-serif text-3xl sm:text-4xl text-[#161616]")
                                status_badge = "PASSED (COMPLETED)" if passed else "NEEDS REVIEW"
                                badge_bg = "bg-[#2D6A4F] text-white" if passed else "bg-[#B4692C] text-white"
                                ui.label(status_badge).classes(f"text-xs font-mono font-bold px-3 py-1.5 rounded-lg {badge_bg}")

                            eval_msg = (
                                "Congratulations! You have satisfied the academic mastery criteria for this syllabus unit. Your progress has been updated."
                                if passed else
                                "You scored below the 60% mastery threshold. Review the diagnostic feedback below and retake the assessment when ready."
                            )
                            ui.label(eval_msg).classes("text-sm text-[#5E5A55] leading-relaxed")

                            with ui.row().classes("gap-3 pt-2 flex-wrap"):
                                def restart_assessment():
                                    state["current_idx"] = 0
                                    state["answers"] = {}
                                    state["submitted"] = False
                                    state["results"] = None
                                    render_assessment_body.refresh()

                                ui.button("Retake Assessment", on_click=restart_assessment).classes("btn-subtle text-xs px-4 py-2")
                                ui.button("Return to Module Overview", on_click=lambda: nav.open_module(module.id)).classes("btn-primary text-xs px-4 py-2")
                                if passed:
                                    ui.button("Proceed to Project Workshop →", on_click=lambda: nav.open_projects(module.id)).classes("btn-primary text-xs px-4 py-2")

                        # Detailed diagnostic question review
                        with ui.column().classes("w-full gap-4"):
                            ui.label("Diagnostic Question Review").classes("font-serif text-2xl text-[#161616]")
                            for q_idx, q in enumerate(questions, 1):
                                q_data = res["answers_payload"].get(q.id, {})
                                is_correct = q_data.get("is_correct", False)
                                border_color = "border-l-4 border-l-[#2D6A4F]" if is_correct else "border-l-4 border-l-[#9D3A3A]"

                                with ui.card().classes(f"w-full bg-[#FBF8F3] border border-[#E2DCD2] {border_color} p-5 rounded-lg gap-3"):
                                    with ui.row().classes("w-full justify-between items-center"):
                                        ui.label(f"Question {q_idx} of {total_q}").classes("text-[10px] font-mono text-[#8C857D] uppercase tracking-wider")
                                        outcome_label = "✓ Correct (+1 Mark)" if is_correct else "✗ Incorrect (0 Marks)"
                                        outcome_color = "text-[#2D6A4F]" if is_correct else "text-[#9D3A3A]"
                                        ui.label(outcome_label).classes(f"text-xs font-semibold {outcome_color}")

                                    ui.label(q.question).classes("font-serif text-lg text-[#161616]")

                                    with ui.column().classes("w-full gap-1 pt-1 text-xs"):
                                        chosen = q_data.get("selected", "No answer selected")
                                        ui.label(f"Your answer: {chosen}").classes("text-[#5E5A55] font-medium")
                                        if not is_correct:
                                            ui.label(f"Correct answer: {q.options[q.correct_index]}").classes("text-[#2D6A4F] font-semibold")
                                        with ui.element("div").classes("bg-[#EFEAE2] p-3 rounded mt-1 border border-[#E2DCD2]"):
                                            ui.label(f"Explanation: {q.explanation}").classes("text-[#5E5A55] leading-relaxed")
                    return

                # ----------------------------------------------------
                # VIEW 2: FINAL REVIEW BEFORE SUBMISSION
                # ----------------------------------------------------
                if idx == total_q:
                    unanswered = [i + 1 for i, q in enumerate(questions) if q.id not in state["answers"]]
                    all_answered = len(unanswered) == 0

                    with ui.card().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] p-6 sm:p-8 rounded-xl shadow-sm gap-6"):
                        with ui.column().classes("gap-1"):
                            ui.label("FINAL ASSESSMENT REVIEW").classes("text-[10px] font-mono font-bold text-[#6E8098] uppercase tracking-wider")
                            ui.label("Review Your Answers Before Submitting").classes("font-serif text-3xl text-[#161616]")
                            ui.label(f"You have answered {len(state['answers'])} of {total_q} questions.").classes("text-sm text-[#5E5A55]")

                        # Question summary list
                        with ui.column().classes("w-full gap-3"):
                            for i, q in enumerate(questions):
                                ans = state["answers"].get(q.id)
                                with ui.row().classes("w-full justify-between items-center p-3.5 bg-white border border-[#E2DCD2] rounded-lg flex-wrap gap-2"):
                                    with ui.column().classes("flex-1 min-w-[200px] gap-0.5"):
                                        ui.label(f"Q{i+1}: {q.question}").classes("text-xs font-semibold text-[#161616] line-clamp-1")
                                        ans_text = f"Selected: {ans}" if ans else "Not answered yet"
                                        ans_color = "text-[#396DAB]" if ans else "text-[#9D3A3A]"
                                        ui.label(ans_text).classes(f"text-[11px] {ans_color}")

                                    def jump_to_q(target=i):
                                        state["current_idx"] = target
                                        render_assessment_body.refresh()

                                    ui.button("Edit Answer", on_click=jump_to_q).classes("btn-subtle text-[11px] px-3 py-1")

                        if not all_answered:
                            with ui.element("div").classes("w-full bg-[#FDF2F2] border-l-4 border-[#9D3A3A] p-4 rounded-r"):
                                ui.label(f"Notice: Questions {unanswered} are still unanswered.").classes("text-xs font-medium text-[#9D3A3A]")

                        # Action buttons
                        with ui.row().classes("w-full justify-between items-center pt-4 border-t border-[#E2DCD2] flex-wrap gap-3"):
                            def back_to_last_q():
                                state["current_idx"] = total_q - 1
                                render_assessment_body.refresh()

                            ui.button("← Back to Questions", on_click=back_to_last_q).classes("btn-subtle text-xs px-4 py-2")

                            def submit_assessment():
                                score = 0.0
                                answers_payload = {}
                                for q in questions:
                                    user_val = state["answers"].get(q.id)
                                    chosen_idx = q.options.index(user_val) if user_val in q.options else -1
                                    is_corr = (chosen_idx == q.correct_index)
                                    if is_corr:
                                        score += 1.0
                                    answers_payload[q.id] = {
                                        "question": q.question,
                                        "selected": user_val,
                                        "correct": q.options[q.correct_index],
                                        "is_correct": is_corr
                                    }

                                percentage = (score / total_q) * 100.0
                                passed = percentage >= 60.0

                                # Persist to SQLite
                                with get_db() as db_session:
                                    record_quiz_attempt(
                                        db_session,
                                        learner_id,
                                        module.id,
                                        score,
                                        float(total_q),
                                        answers_payload,
                                        len(module.lessons)
                                    )

                                state["submitted"] = True
                                state["results"] = {
                                    "score": score,
                                    "percentage": percentage,
                                    "passed": passed,
                                    "answers_payload": answers_payload
                                }
                                render_assessment_body.refresh()
                                ui.notify(f"Assessment submitted: {percentage:.0f}%", color="positive" if passed else "warning")

                            ui.button("Submit Assessment & Grade ▶", on_click=submit_assessment).classes("btn-primary text-sm font-semibold px-6 py-2.5")
                    return

                # ----------------------------------------------------
                # VIEW 1: FOCUSED ONE-QUESTION-AT-A-TIME FLOW
                # ----------------------------------------------------
                curr_q = questions[idx]
                curr_ans = state["answers"].get(curr_q.id)

                # Progress header bar
                with ui.column().classes("w-full gap-3"):
                    with ui.row().classes("w-full justify-between items-center"):
                        ui.label(f"QUESTION {idx + 1} OF {total_q}").classes("editorial-eyebrow")
                        ui.label(f"{len(state['answers'])} of {total_q} Answered").classes("text-xs font-mono text-[#8C857D]")

                    # Smooth visual progress bar
                    progress_pct = ((idx + 1) / total_q) * 100
                    with ui.element("div").classes("w-full h-2 bg-[#E2DCD2] rounded-full overflow-hidden"):
                        ui.element("div").classes("h-full bg-[#4F83BC] transition-all duration-300").style(f"width: {progress_pct}%")

                    # Step pills for rapid question jumping
                    with ui.row().classes("w-full gap-2 pt-1 flex-wrap"):
                        for i in range(total_q):
                            q_id = questions[i].id
                            is_active = (i == idx)
                            has_ans = q_id in state["answers"]

                            if is_active:
                                pill_style = "bg-[#4F83BC] text-white border-[#4F83BC]"
                            elif has_ans:
                                pill_style = "bg-[#E9F1F9] text-[#396DAB] border-[#4F83BC]"
                            else:
                                pill_style = "bg-white text-[#8C857D] border-[#E2DCD2]"

                            def make_jump(target=i):
                                state["current_idx"] = target
                                render_assessment_body.refresh()

                            ui.button(f"Q{i+1}", on_click=make_jump).classes(
                                f"text-xs font-mono px-3 py-1 rounded-md border {pill_style} cursor-pointer"
                            )

                # Focused Question Card
                with ui.card().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] p-6 sm:p-8 rounded-xl shadow-sm gap-6"):
                    with ui.column().classes("w-full gap-2"):
                        ui.label("Multiple Choice").classes("text-[10px] font-mono font-bold text-[#6E8098] uppercase tracking-wider")
                        ui.label(curr_q.question).classes("font-serif text-2xl sm:text-3xl text-[#161616] leading-snug")

                    # Answer Options Radio Group
                    with ui.column().classes("w-full gap-2.5"):
                        radio = ui.radio(
                            curr_q.options,
                            value=curr_ans
                        ).props("keep-color").classes("w-full gap-3 text-sm")

                        def on_select(e):
                            state["answers"][curr_q.id] = e.value

                        radio.on_value_change(on_select)

                    # Navigation Footer
                    with ui.row().classes("w-full justify-between items-center pt-4 border-t border-[#E2DCD2] flex-wrap gap-3 mt-2"):
                        # Previous Button
                        if idx > 0:
                            def go_prev():
                                state["current_idx"] = idx - 1
                                render_assessment_body.refresh()
                            ui.button("← Previous Question", on_click=go_prev).classes("btn-subtle text-xs px-4 py-2")
                        else:
                            ui.element("div") # Spacer

                        # Next / Review Button
                        if idx < total_q - 1:
                            def go_next():
                                state["current_idx"] = idx + 1
                                render_assessment_body.refresh()
                            ui.button("Next Question →", on_click=go_next).classes("btn-primary text-xs font-semibold px-4 py-2")
                        else:
                            def go_review():
                                state["current_idx"] = total_q
                                render_assessment_body.refresh()
                            ui.button("Review All Answers →", on_click=go_review).classes("btn-primary text-xs font-semibold px-5 py-2")

            render_assessment_body()
