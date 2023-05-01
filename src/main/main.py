import uuid
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from httpx_oauth.clients.google import GoogleOAuth2
from starlette.types import Lifespan

from .config import config
from .database import sessionmanager
from .models.user import User
from .user_manager import get_user_manager
from .util import get_secret

sessionmanager.init(config.DB_CONFIG)


def init_app():
    """Create the FastAPI Instance."""
    sessionmanager.init(config.DB_CONFIG)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if not sessionmanager.is_initialized():
            await sessionmanager.close()

    server = FastAPI(title="ReservAI", lifespan=lifespan)

    return server


app = init_app()

cookie_transport = CookieTransport(cookie_name="auth", cookie_samesite="strict")


def get_jwt_strategy():
    """Get a fastapi-users JWTStrategy."""
    strat: JWTStrategy[User, uuid.UUID] = JWTStrategy(
        secret=get_secret("JWT_SECRET"), lifetime_seconds=3600
    )
    return strat


auth_backend: AuthenticationBackend[User, uuid.UUID] = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
current_active_user = fastapi_users.current_user(active=True)  # type: ignore


app.include_router(
    # Typing info for the library is incomplete here
    fastapi_users.get_auth_router(auth_backend),  # type: ignore
    prefix="/auth/jwt",
    tags=["auth"],
)


google_oauth_client = GoogleOAuth2(
    get_secret("GOOGLE_OAUTH_CLIENT_ID"), get_secret("GOOGLE_OAUTH_CLIENT_SECRET")
)

app.include_router(
    # Typing info for the library is incomplete here
    fastapi_users.get_oauth_router(  # type: ignore
        google_oauth_client,
        auth_backend,
        get_secret("OAUTH_STATE_SECRET"),
        associate_by_email=True,
        is_verified_by_default=True,
    ),
    prefix="/auth/google",
    tags=["auth"],
)


@app.get("/hello")
def read_root():
    """Let's just prove the server works."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Temporary function."""
    return {"item_id": item_id, "q": q}


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):  # type:ignore
    """Let's just prove authentication works."""
    return {"message": f"Hello {user.email}!"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
