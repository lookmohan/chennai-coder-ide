"""Google and GitHub sign-in (OAuth 2.0 authorization code flow).

Only the provider is trusted to say who the person is. We use the email it reports,
and only treat it as a match for an existing account when the provider says it is verified.
"""
import logging
from dataclasses import dataclass
from urllib.parse import urlencode

import httpx

from app.core.config import get_settings
from app.core.errors import AppError

logger = logging.getLogger("app.oauth")

PROVIDERS = ("google", "github")


@dataclass(frozen=True)
class OAuthProfile:
    provider: str
    external_id: str
    email: str
    email_verified: bool
    display_name: str
    username_hint: str
    avatar_url: str | None


def provider_configured(provider: str) -> bool:
    s = get_settings()
    if provider == "google":
        return bool(s.google_client_id and s.google_client_secret)
    if provider == "github":
        return bool(s.github_client_id and s.github_client_secret)
    return False


def callback_url(provider: str) -> str:
    return f"{get_settings().public_app_url.rstrip('/')}/api/v1/auth/oauth/{provider}/callback"


def authorize_url(provider: str, state: str) -> str:
    s = get_settings()
    if provider == "google":
        params = {
            "client_id": s.google_client_id,
            "redirect_uri": callback_url(provider),
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "prompt": "select_account",
        }
        return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)
    params = {
        "client_id": s.github_client_id,
        "redirect_uri": callback_url(provider),
        "scope": "read:user user:email",
        "state": state,
    }
    return "https://github.com/login/oauth/authorize?" + urlencode(params)


def fetch_profile(provider: str, code: str) -> OAuthProfile:
    try:
        if provider == "google":
            return _google(code)
        return _github(code)
    except AppError:
        raise
    except (httpx.HTTPError, KeyError, ValueError, TypeError) as exc:
        logger.warning("oauth_exchange_failed", extra={"provider": provider})
        raise AppError("OAUTH_FAILED", "Sign-in with that account didn't work. Please try again.", 502) from exc


def _google(code: str) -> OAuthProfile:
    s = get_settings()
    with httpx.Client(timeout=10) as client:
        token = client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": s.google_client_id,
                "client_secret": s.google_client_secret,
                "redirect_uri": callback_url("google"),
                "grant_type": "authorization_code",
            },
        )
        token.raise_for_status()
        access = token.json()["access_token"]

        info = client.get(
            "https://openidconnect.googleapis.com/v1/userinfo",
            headers={"Authorization": f"Bearer {access}"},
        )
        info.raise_for_status()
        data = info.json()

    email = str(data.get("email") or "").strip().lower()
    local_part = email.split("@")[0] if email else "learner"
    return OAuthProfile(
        provider="google",
        external_id=str(data["sub"]),
        email=email,
        email_verified=data.get("email_verified") in (True, "true"),
        display_name=str(data.get("name") or local_part),
        username_hint=local_part,
        avatar_url=data.get("picture"),
    )


def _github(code: str) -> OAuthProfile:
    s = get_settings()
    with httpx.Client(timeout=10) as client:
        token = client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "code": code,
                "client_id": s.github_client_id,
                "client_secret": s.github_client_secret,
                "redirect_uri": callback_url("github"),
            },
            headers={"Accept": "application/json"},
        )
        token.raise_for_status()
        access = token.json()["access_token"]

        headers = {"Authorization": f"Bearer {access}", "Accept": "application/vnd.github+json"}
        user = client.get("https://api.github.com/user", headers=headers)
        user.raise_for_status()
        emails = client.get("https://api.github.com/user/emails", headers=headers)
        emails.raise_for_status()

    u = user.json()
    primary = next((e for e in emails.json() if e.get("primary") and e.get("verified")), None)
    if primary is None:
        raise AppError(
            "OAUTH_NO_VERIFIED_EMAIL",
            "Your GitHub account needs a verified primary email before you can sign in with it.",
            400,
        )
    return OAuthProfile(
        provider="github",
        external_id=str(u["id"]),
        email=str(primary["email"]).strip().lower(),
        email_verified=True,
        display_name=str(u.get("name") or u["login"]),
        username_hint=str(u["login"]),
        avatar_url=u.get("avatar_url"),
    )
