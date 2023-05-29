import uuid
from typing import Any

from fastapi.responses import RedirectResponse, Response
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from httpx_oauth.clients.google import GoogleOAuth2

from .models.user import User, get_user_manager
from .util import get_secret


class CookieRedirectTransport(CookieTransport):
    """Custom cookie transport thar redirects the user after a succesful login."""

    async def get_login_response(self, token: str) -> Response:
        """Redirect the user on successful login."""
        response = RedirectResponse("/auth")
        return self._set_login_cookie(response, token)


cookie_transport = CookieRedirectTransport(cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    """Initialize the FastAPI-Users JWTStrategy."""
    return JWTStrategy(secret=get_secret("JWT_SECRET"), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


# Our library doesn't provide enough type information here.
current_active_user: Any = fastapi_users.current_user(active=True)


google_oauth_client = GoogleOAuth2(
    get_secret("GOOGLE_OAUTH_CLIENT_ID"), get_secret("GOOGLE_OAUTH_CLIENT_SECRET")
)


# Our library doesn't have strict enough types for our linter
google_oauth_router = fastapi_users.get_oauth_router(  # type: ignore
    google_oauth_client,
    auth_backend,
    get_secret("OAUTH_STATE_SECRET"),
    is_verified_by_default=True,
)
