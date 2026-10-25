"""
Header and navigation component for Pip Learn.
Minimal editorial bar with branding and links to all platform areas.
"""
from nicegui import ui
from app.config import COURSE_CODE
from app.database.connection import get_db
from app.auth.service import get_current_user_and_learner
import app.navigation.nav as nav

def render_header(active_route: str = "", compact: bool = False):
    """Render top navigation bar with dynamic authenticated/unauthenticated state."""
    with get_db() as db:
        auth = get_current_user_and_learner(db)
        is_authenticated = auth is not None
        current_user = auth[0] if auth else None
        current_learner = auth[1] if auth else None

    vertical = "py-2" if compact else "py-3"
    header_classes = f"w-full bg-[#FAF7F2] border-b border-[#E2DCD2] px-4 sm:px-6 md:px-8 {vertical} z-40 text-[#161616] flex items-center justify-between sticky top-0 flex-shrink-0"

    with ui.element("header").classes(header_classes):
        with ui.row().classes("items-center gap-3 sm:gap-6"):
            with ui.link(target="/").classes("flex items-center gap-3 no-underline text-[#161616]"):
                # Monogram logo
                with ui.element("div").classes("monogram-pi w-8 h-8 rounded-lg bg-[#23342B] text-[#FBF8F3] flex items-center justify-center font-serif text-lg font-bold shadow-xs"):
                    ui.label("π")
                ui.label("Pip Learn").classes("font-serif text-xl tracking-tight leading-none text-[#161616]")

        # Middle Navigation Links: Curriculum · Study Space · About
        with ui.row().classes("hidden md:flex items-center gap-6 sm:gap-8 font-sans text-sm text-[#2C2926]"):
            ui.button("Curriculum", on_click=nav.go_to_curriculum).props("flat dense").classes("text-[#2C2926] hover:text-[#161616] text-sm font-normal no-underline normal-case transition-colors")
            if not is_authenticated:
                ui.button("Study Space", on_click=nav.go_to_dashboard).props("flat dense").classes("text-[#2C2926] hover:text-[#161616] text-sm font-normal no-underline normal-case transition-colors")
            ui.button("About", on_click=lambda: ui.run_javascript('document.getElementById("about")?.scrollIntoView({behavior: "smooth"})')).props("flat dense").classes("text-[#2C2926] hover:text-[#161616] text-sm font-normal no-underline normal-case transition-colors")

        with ui.row().classes("items-center gap-2 sm:gap-3"):
            # Mobile menu dropdown
            with ui.button(icon="menu").props("flat round size=sm").classes("md:hidden text-[#161616]"):
                with ui.menu().classes("bg-[#FBF8F3] border border-[#E2DCD2] font-sans p-2 rounded-xl shadow-md"):
                    with ui.menu_item(on_click=nav.go_to_curriculum):
                        ui.label("Curriculum").classes("text-sm text-[#161616]")
                    with ui.menu_item(on_click=nav.go_to_dashboard):
                        ui.label("Study Space").classes("text-sm text-[#161616]")
                    with ui.menu_item(on_click=lambda: ui.run_javascript('document.getElementById("about")?.scrollIntoView({behavior: "smooth"})')):
                        ui.label("About").classes("text-sm text-[#161616]")
                    ui.separator().classes("bg-[#E2DCD2] my-1")
                    if is_authenticated:
                        with ui.menu_item(on_click=nav.go_to_setup):
                            ui.label("Learner Profile").classes("text-xs text-[#5E5A55]")
                        with ui.menu_item(on_click=nav.open_settings):
                            ui.label("Settings").classes("text-xs text-[#5E5A55]")
                        with ui.menu_item(on_click=nav.logout):
                            ui.label("Sign Out").classes("text-xs text-[#9D3A3A] font-semibold")
                    else:
                        with ui.menu_item(on_click=lambda: nav.go_to_login(active_route)):
                            ui.label("Sign In").classes("text-xs text-[#5088C2] font-semibold")
                        with ui.menu_item(on_click=nav.start_learning):
                            ui.label("Get Started").classes("text-xs text-[#161616] font-semibold")

            if is_authenticated:
                learner_display_name = current_learner.name if current_learner else current_user.username
                # Profile name tag
                with ui.row().classes("hidden sm:flex items-center gap-1.5 px-3 py-1.5 bg-white/70 backdrop-blur-sm rounded-xl text-xs font-sans text-[#161616] border border-[#E2DCD2]/60"):
                    ui.icon("account_circle", size="16px").classes("text-[#5088C2]")
                    ui.label(learner_display_name).classes("font-medium truncate max-w-[130px]")

                with ui.button(on_click=nav.open_settings).props("round flat size=sm").classes("text-[#5E5A55] hover:text-[#161616]"):
                    ui.icon("settings", size="18px")
                ui.button("Study Space", on_click=nav.go_to_dashboard).classes("btn-blue text-xs py-1.5 px-3 rounded-lg text-white normal-case")
                ui.button("Logout", on_click=nav.logout).props("flat dense").classes("text-xs text-[#8C857D] hover:text-[#9D3A3A] px-2 normal-case")
            else:
                ui.button("Sign In", on_click=lambda: nav.go_to_login(active_route)).props("flat dense").classes("text-sm font-medium text-[#2C2926] hover:text-[#161616] normal-case")
                ui.button("Get Started", on_click=nav.start_learning).classes("btn-blue text-sm font-medium px-4 py-2 rounded-lg text-white normal-case shadow-xs")
