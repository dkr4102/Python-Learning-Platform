"""
Route guards and redirect safety for Pip Learn.
Enforces authentication on protected routes and prevents open redirect vulnerabilities.
"""
from urllib.parse import quote, unquote
from typing import Optional, Tuple
from nicegui import ui
from sqlalchemy.orm import Session

from app.database.models import User, Learner
from app.auth.service import get_current_user_and_learner


def is_safe_redirect_url(url: Optional[str]) -> bool:
    """Ensure redirect destination is a safe relative path within the application."""
    if not url:
        return False
    url = url.strip()
    # Must start with single / and not //, /\, or contain scheme
    if not url.startswith("/") or url.startswith("//") or url.startswith("/\\"):
        return False
    if "://" in url:
        return False
    return True


def sanitize_redirect_url(url: Optional[str], default: str = "/dashboard") -> str:
    """Return sanitized redirect URL or safe default."""
    if url and is_safe_redirect_url(url):
        return url
    return default


def require_auth(db: Session, active_route: str = "") -> Optional[Tuple[User, Learner]]:
    """
    Guard for protected learning pages.
    - If unauthenticated: redirect to /login with preserved safe destination.
    - If authenticated but onboarding not completed: redirect to /setup.
    - Returns (User, Learner) on success.
    """
    auth = get_current_user_and_learner(db)
    if not auth:
        if active_route and is_safe_redirect_url(active_route) and active_route != "/dashboard":
            safe_dest = quote(active_route, safe="")
            ui.navigate.to(f"/login?redirect={safe_dest}")
        else:
            ui.navigate.to("/login")
        return None

    user, learner = auth

    # First-time onboarding enforcement (Phase 4)
    if not learner.onboarding_completed and active_route != "/setup":
        ui.navigate.to("/setup")
        return None

    return user, learner


def require_guest(db: Session) -> bool:
    """
    Guard for public login/register pages.
    If learner is already authenticated, redirects directly to dashboard.
    Returns True if user is a guest, False if redirected.
    """
    auth = get_current_user_and_learner(db)
    if auth:
        ui.navigate.to("/dashboard")
        return False
    return True
