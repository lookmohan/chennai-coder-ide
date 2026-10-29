from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from app.api.deps import COOKIE_ACCESS, COOKIE_CSRF, get_current_user
from app.core.config import get_settings
from app.core.database import get_db
from app.core.rate_limit import client_ip, enforce_rate_limit, rate_limit
from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import Envelope
from app.schemas.user import UserOut
from app.security.tokens import create_access_token, new_csrf_token
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_auth_cookies(response: Response, user: User) -> None:
    settings = get_settings()
    max_age = settings.jwt_expires_minutes * 60
    common = dict(
        max_age=max_age,
        secure=settings.cookie_secure,
        samesite="lax",
        domain=settings.cookie_domain,
        path="/",
    )
    response.set_cookie(COOKIE_ACCESS, create_access_token(user.id), httponly=True, **common)
    # Readable by the frontend so it can echo the value in X-CSRF-Token.
    response.set_cookie(COOKIE_CSRF, new_csrf_token(), httponly=False, **common)


@router.post(
    "/register",
    status_code=201,
    response_model=Envelope[UserOut],
    dependencies=[Depends(rate_limit("register", lambda s: s.rate_register_per_hour, 3600))],
)
def register(
    payload: RegisterRequest, request: Request, response: Response, db: Session = Depends(get_db)
) -> Envelope[UserOut]:
    user = auth_service.register_user(
        db,
        email=payload.email,
        password=payload.password,
        username=payload.username,
        display_name=payload.display_name,
        ip=client_ip(request),
    )
    _set_auth_cookies(response, user)
    return Envelope(data=UserOut.model_validate(user))


@router.post(
    "/login",
    response_model=Envelope[UserOut],
    dependencies=[Depends(rate_limit("login", lambda s: s.rate_login_per_minute, 60))],
)
def login(
    payload: LoginRequest, request: Request, response: Response, db: Session = Depends(get_db)
) -> Envelope[UserOut]:
    enforce_rate_limit(
        f"login-email:{payload.email.lower()}",
        get_settings().rate_login_per_email_per_15min,
        900,
    )
    user = auth_service.authenticate(
        db, email=payload.email, password=payload.password, ip=client_ip(request)
    )
    _set_auth_cookies(response, user)
    return Envelope(data=UserOut.model_validate(user))


@router.post("/logout", response_model=Envelope[dict])
def logout(response: Response) -> Envelope[dict]:
    settings = get_settings()
    for name in (COOKIE_ACCESS, COOKIE_CSRF):
        response.delete_cookie(name, path="/", domain=settings.cookie_domain)
    return Envelope(data={"logged_out": True})


@router.get("/me", response_model=Envelope[UserOut])
def me(user: User = Depends(get_current_user)) -> Envelope[UserOut]:
    return Envelope(data=UserOut.model_validate(user))
