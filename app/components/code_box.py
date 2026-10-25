"""
Interactive Python code workspace component.
Provides code editing, subprocess isolated execution, output console, and error explanations.
"""
from nicegui import ui
from app.execution.runner import run_python_code

def render_code_box(
    initial_code: str,
    title: str = "Interactive Python Workspace",
    height_lines: int = 10,
    on_success: callable = None
):
    """
    Renders an editable code block with execution console.
    """
    with ui.column().classes("w-full bg-[#1A1E1C] border border-[#2D3330] rounded-lg overflow-hidden font-sans my-4 shadow-sm"):
        # Header bar
        with ui.row().classes("w-full bg-[#141716] px-4 py-2.5 justify-between items-center border-b border-[#2D3330]"):
            with ui.row().classes("items-center gap-2"):
                with ui.element("div").classes("flex gap-1.5"):
                    ui.element("div").classes("w-2.5 h-2.5 rounded-full bg-[#FF5F56]")
                    ui.element("div").classes("w-2.5 h-2.5 rounded-full bg-[#FFBD2E]")
                    ui.element("div").classes("w-2.5 h-2.5 rounded-full bg-[#27C93F]")
                ui.label(title).classes("text-xs text-[#A0AAB2] font-mono ml-2 font-medium")

            with ui.row().classes("items-center gap-2"):
                status_badge = ui.label("Ready").classes("text-[10px] uppercase font-mono px-2 py-0.5 rounded bg-[#23342B] text-[#A3E635]")

        # Code editor area
        editor = ui.textarea(value=initial_code.strip()).classes("w-full bg-[#1A1E1C] text-[#E8EFEA] font-mono text-sm p-4 border-none focus:outline-none resize-y").props(f"rows={height_lines} spellcheck=false")

        # Action bar
        with ui.row().classes("w-full bg-[#141716] px-4 py-2 justify-between items-center border-t border-[#2D3330]"):
            with ui.row().classes("gap-2"):
                reset_btn = ui.button("Reset Code").props("flat size=sm").classes("text-xs text-[#8C857D] hover:text-white font-sans")
                reset_btn.on_click(lambda: editor.set_value(initial_code.strip()))

            run_btn = ui.button("Run Code ▶").props("size=sm").classes("bg-[#23342B] text-white hover:bg-[#2D4237] px-4 py-1 text-xs font-semibold rounded font-sans")

        # Output console (hidden initially or showing default prompt)
        output_container = ui.column().classes("w-full bg-[#111413] p-4 border-t border-[#2D3330] gap-2")
        with output_container:
            ui.label("TERMINAL OUTPUT").classes("text-[10px] tracking-wider font-mono text-[#6E8098] font-bold")
            output_label = ui.label("Click 'Run Code ▶' to execute this script in an isolated Python subprocess.").classes("text-xs font-mono text-[#8C857D] whitespace-pre-wrap")
            explanation_box = ui.label("").classes("text-xs text-[#DCC9A3] italic hidden")

        def handle_run():
            status_badge.set_text("Executing...")
            status_badge.classes(replace="bg-[#B4692C] text-white")
            
            code = editor.value
            result = run_python_code(code)

            if result["success"]:
                status_badge.set_text(f"Success ({result['elapsed_ms']} ms)")
                status_badge.classes(replace="bg-[#23342B] text-[#A3E635]")
                out = result["stdout"].strip() or "[Program completed successfully with no console output]"
                output_label.set_text(out)
                output_label.classes(replace="text-[#A3E635]")
                explanation_box.classes(add="hidden")
                if on_success:
                    on_success(code, result)
            else:
                status_badge.set_text(f"Error ({result['elapsed_ms']} ms)")
                status_badge.classes(replace="bg-[#9D3A3A] text-white")
                err_text = result["stderr"].strip() or "Execution failed."
                output_label.set_text(err_text)
                output_label.classes(replace="text-[#FF7B72]")
                if result.get("explanation"):
                    explanation_box.set_text(f"💡 Diagnostic Insight: {result['explanation']}")
                    explanation_box.classes(remove="hidden")

        run_btn.on_click(handle_run)
