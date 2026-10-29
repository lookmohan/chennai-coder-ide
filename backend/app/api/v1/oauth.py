import secrets

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.api.v1.auth import _set_auth_cookies
from app.core.config import get_settings
from app.core.database import get_db
from app.core.errors import AppError
from app.core.rate_limit import client_ip
from app.schemas.common import Envelope
from app.security.oauth import PROVIDERS, authorize_url, fetch_profile, provider_configured
from app.services import oauth_service

router = APIRouter(prefix="/auth/oauth", tags=["auth"])

STATE_COOKIE = "cc_oauth_state"
STATE_COOKIE_PATH = "/api/v1/auth/oauth"


def _require_provider(provider: str) -> None:
    if provider not in PROVIDERS:
        raise AppError("NOT_FOUND", "Unknown sign-in provider.", 404)
    if not provider_configured(provider):
        raise AppError("OAUTH_NOT_CONFIGURED", "That sign-in method isn't set up yet.", 503)


@router.get("/providers", response_model=Envelope[dict])
def providers() -> Envelope[dict]:
    """Which sign-in buttons to show. Only reports on/off, never the secrets."""
    return Envelope(data={name: provider_configured(name) for name in PROVIDERS})


@router.get("/{provider}/start")
def start(provider: str) -> RedirectResponse:
    _require_provider(provider)
    state = secrets.token_urlsafe(32)
    response = RedirectResponse(authorize_url(provider, state), status_code=302)
    response.set_cookie(
        STATE_COOKIE,
        state,
        max_age=600,
        httponly=True,
        secure=get_settings().cookie_secure,
        samesite="lax",
        path=STATE_COOKIE_PATH,
    )
    return response


@router.get("/{provider}/callback")
def callback(
    provider: str,
    request: Request,
    code: str | None = None,
    state: str | None = None,
    db: Session = Depends(get_db),
) -> RedirectResponse:
    home = get_settings().public_app_url.rstrip("/")

    def back_to_login(reason: str) -> RedirectResponse:
        response = RedirectResponse(f"{home}/login?error={reason}", status_code=302)
        response.delete_cookie(STATE_COOKIE, path=STATE_COOKIE_PATH)
        return response

    if provider not in PROVIDERS or not provider_configured(provider):
        return back_to_login("oauth_not_configured")

    expected_state = request.cookies.get(STATE_COOKIE)
    if not code or not state or not expected_state or not secrets.compare_digest(state, expected_state):
        return back_to_login("oauth_state")

    try:
        profile = fetch_profile(provider, code)
        user = oauth_service.sign_in_with_provider(db, profile, ip=client_ip(request))
    except AppError as exc:
        return back_to_login(exc.code.lower())

    response = RedirectResponse(f"{home}/dashboard", status_code=302)
    _set_auth_cookies(response, user)
    response.delete_cookie(STATE_COOKIE, path=STATE_COOKIE_PATH)
    return response
