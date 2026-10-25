"""
Unified Application Page Shell for Pip Learn.
Ensures correct document flow, full viewport height, and prevents footer overlap.
"""
from contextlib import contextmanager
from nicegui import ui
from app.components.header import render_header
from app.components.footer import render_footer

@contextmanager
def page_shell(active_route: str = "", compact: bool = False, show_footer: bool = True):
    """
    Unified application page shell ensuring:
    - Full viewport height minimum with normal flex-column document flow
    - Sticky editorial header
    - flex-grow main content area
    - Footer at the natural end of the document, mt-auto, never obscuring content
    """
    with ui.column().classes("w-full min-h-screen p-0 m-0 gap-0 justify-between flex flex-col bg-[#F5F2EC] font-sans"):
        render_header(active_route=active_route, compact=compact)
        with ui.element("main").classes("w-full flex-grow flex flex-col"):
            yield
        if show_footer:
            render_footer()
