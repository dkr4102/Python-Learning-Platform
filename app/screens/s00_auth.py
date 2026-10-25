"""
Screen 00: Authentication Screens (Login & Register)
Editorial login and registration interfaces matching Pip Learn's classical aesthetic.
"""
from nicegui import ui
from app.components.layout import page_shell
from app.database.connection import get_db
from app.auth.service import (
    authenticate_user,
    register_user,
    validate_registration_input,
    create_session,
    set_user_session_storage,
)
from app.auth.guards import sanitize_redirect_url, require_guest
from app.navigation.nav import go_to_login, go_to_register


def render_login_screen(redirect_target: str = "/dashboard"):
    """Render unified login screen with rate-limiting and safe redirects."""
    with get_db() as db:
        if not require_guest(db):
            return

    clean_redirect = sanitize_redirect_url(redirect_target, default="/dashboard")

    with page_shell(active_route="/login", show_footer=False):
        with ui.column().classes("w-full max-w-md mx-auto py-12 px-4 sm:px-6 items-center gap-6"):
            # Header Badge
            with ui.row().classes("items-center gap-2"):
                ui.label("MARWADI UNIVERSITY • COURSE 01AP0303").classes("editorial-eyebrow")

            with ui.card().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] p-6 sm:p-8 rounded-2xl shadow-sm gap-5"):
                with ui.column().classes("gap-1"):
                    ui.label("Sign in to Study Space").classes("font-serif text-3xl text-[#161616] tracking-tight")
                    ui.label("Enter your learner credentials to resume your individual Python progress.").classes("text-xs text-[#5E5A55] leading-relaxed")

                # Error container
                error_box = ui.column().classes("w-full hidden bg-[#FDF2F2] border border-[#F8B4B4] text-[#9D3A3A] px-3.5 py-2.5 rounded-lg text-xs leading-normal")
                with error_box:
                    error_msg = ui.label("").classes("text-[#9D3A3A] font-medium")

                # Form Fields
                with ui.column().classes("w-full gap-3 pt-1"):
                    ui.label("Username or Email").classes("text-xs font-semibold text-[#161616] font-sans")
                    username_input = ui.input(placeholder="e.g. priya or priya@marwadi.edu.in").classes("w-full bg-white rounded-lg").props("outlined dense")

                    with ui.row().classes("w-full justify-between items-center"):
                        ui.label("Password").classes("text-xs font-semibold text-[#161616] font-sans")

                    password_input = ui.input(placeholder="••••••••", password=True, password_toggle_button=True).classes("w-full bg-white rounded-lg").props("outlined dense")

                def handle_login():
                    ident = username_input.value or ""
                    pwd = password_input.value or ""
                    if not ident.strip() or not pwd:
                        error_msg.text = "Please enter both username/email and password."
                        error_box.classes(remove="hidden")
                        return

                    try:
                        with get_db() as db:
                            user = authenticate_user(db, ident, pwd)
                            if not user:
                                error_msg.text = "Invalid credentials. Please verify your username and password."
                                error_box.classes(remove="hidden")
                                return

                            # Create session
                            token = create_session(db, user.id)
                            set_user_session_storage(token, user.id)

                            # Check onboarding status
                            from app.database.crud import get_learner_by_user_id
                            learner = get_learner_by_user_id(db, user.id)
                            if learner and not learner.onboarding_completed:
                                ui.navigate.to("/setup")
                            else:
                                ui.navigate.to(clean_redirect)
                    except ValueError as ve:
                        error_msg.text = str(ve)
                        error_box.classes(remove="hidden")
                    except Exception:
                        error_msg.text = "An unexpected error occurred during login. Please try again."
                        error_box.classes(remove="hidden")

                submit_btn = ui.button("Sign In →", on_click=handle_login).classes("btn-primary w-full text-sm font-semibold py-2.5 mt-2")
                username_input.on("keydown.enter", handle_login)
                password_input.on("keydown.enter", handle_login)

                # Registration CTA
                ui.separator().classes("bg-[#E2DCD2]")
                with ui.row().classes("w-full justify-center items-center text-xs text-[#5E5A55] gap-1"):
                    ui.label("First time at Pip Learn?")
                    ui.button("Create an account", on_click=lambda: go_to_register(clean_redirect)).props("flat dense").classes("text-xs text-[#396DAB] font-semibold hover:underline p-0")


def render_register_screen(redirect_target: str = "/dashboard"):
    """Render new learner registration screen."""
    with get_db() as db:
        if not require_guest(db):
            return

    clean_redirect = sanitize_redirect_url(redirect_target, default="/dashboard")

    with page_shell(active_route="/register", show_footer=False):
        with ui.column().classes("w-full max-w-lg mx-auto py-10 px-4 sm:px-6 items-center gap-6"):
            # Header Badge
            with ui.row().classes("items-center gap-2"):
                ui.label("MARWADI UNIVERSITY • COURSE 01AP0303").classes("editorial-eyebrow")

            with ui.card().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] p-6 sm:p-8 rounded-2xl shadow-sm gap-5"):
                with ui.column().classes("gap-1"):
                    ui.label("Create Learner Account").classes("font-serif text-3xl text-[#161616] tracking-tight")
                    ui.label("Register your personal learning workspace. Your progress, code, and notes are securely isolated.").classes("text-xs text-[#5E5A55] leading-relaxed")

                # Error container
                error_box = ui.column().classes("w-full hidden bg-[#FDF2F2] border border-[#F8B4B4] text-[#9D3A3A] px-3.5 py-2.5 rounded-lg text-xs leading-normal")
                with error_box:
                    error_msg = ui.label("").classes("text-[#9D3A3A] font-medium")

                # Form Fields
                with ui.column().classes("w-full gap-3 pt-1"):
                    ui.label("Full Name").classes("text-xs font-semibold text-[#161616] font-sans")
                    name_input = ui.input(placeholder="e.g. Aarav Sharma").classes("w-full bg-white rounded-lg").props("outlined dense")

                    ui.label("Username").classes("text-xs font-semibold text-[#161616] font-sans")
                    username_input = ui.input(placeholder="e.g. aarav_sharma").classes("w-full bg-white rounded-lg").props("outlined dense")

                    ui.label("Email Address").classes("text-xs font-semibold text-[#161616] font-sans")
                    email_input = ui.input(placeholder="e.g. aarav@student.marwadi.edu.in").classes("w-full bg-white rounded-lg").props("outlined dense")

                    ui.label("Password (at least 6 characters)").classes("text-xs font-semibold text-[#161616] font-sans")
                    password_input = ui.input(placeholder="••••••••", password=True, password_toggle_button=True).classes("w-full bg-white rounded-lg").props("outlined dense")

                    ui.label("Confirm Password").classes("text-xs font-semibold text-[#161616] font-sans")
                    confirm_input = ui.input(placeholder="••••••••", password=True, password_toggle_button=True).classes("w-full bg-white rounded-lg").props("outlined dense")

                def handle_register():
                    name = name_input.value or ""
                    username = username_input.value or ""
                    email = email_input.value or ""
                    pwd = password_input.value or ""
                    confirm = confirm_input.value or ""

                    validation_err = validate_registration_input(name, username, email, pwd, confirm)
                    if validation_err:
                        error_msg.text = validation_err
                        error_box.classes(remove="hidden")
                        return

                    try:
                        with get_db() as db:
                            user, learner = register_user(
                                db=db,
                                name=name,
                                username=username,
                                email=email,
                                password=pwd
                            )
                            # Start session
                            token = create_session(db, user.id)
                            set_user_session_storage(token, user.id)

                            # First-time onboarding flow (Phase 4)
                            ui.navigate.to("/setup")
                    except ValueError as ve:
                        error_msg.text = str(ve)
                        error_box.classes(remove="hidden")
                    except Exception as ex:
                        error_msg.text = "Registration error. Please check your information and try again."
                        error_box.classes(remove="hidden")

                submit_btn = ui.button("Create Account & Begin →", on_click=handle_register).classes("btn-primary w-full text-sm font-semibold py-2.5 mt-2")
                confirm_input.on("keydown.enter", handle_register)

                # Login CTA
                ui.separator().classes("bg-[#E2DCD2]")
                with ui.row().classes("w-full justify-center items-center text-xs text-[#5E5A55] gap-1"):
                    ui.label("Already have an account?")
                    ui.button("Sign in here", on_click=lambda: go_to_login(clean_redirect)).props("flat dense").classes("text-xs text-[#396DAB] font-semibold hover:underline p-0")
