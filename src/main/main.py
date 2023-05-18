import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from httpx_oauth.clients.google import GoogleOAuth2

from .config import config
from .database import sessionmanager
from .models.user import User, get_user_manager
from .util import get_secret

cookie_transport = CookieTransport(cookie_max_age=3600)


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


def init_app(init_db: bool = True):
    """Create the FastAPI Instance."""
    # lifespan is optional, but pyright doesn't like it
    lifespan = None  # type: ignore

    if init_db:
        sessionmanager.init(config.DB_CONFIG)

        @asynccontextmanager
        async def lifespan(app: FastAPI):
            yield
            if not sessionmanager.is_initialized():
                await sessionmanager.close()

    server = FastAPI(title="ReservAI", lifespan=lifespan)

    return server


app = init_app()


google_oauth_client = GoogleOAuth2(
    get_secret("GOOGLE_OAUTH_CLIENT_ID"), get_secret("GOOGLE_OAUTH_CLIENT_SECRET")
)

app.include_router(
    # Our library doesn't have strict enough types for our linter
    fastapi_users.get_oauth_router(  # type: ignore
        google_oauth_client,
        auth_backend,
        get_secret("OAUTH_STATE_SECRET"),
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


app.mount("/", StaticFiles(directory="static", html=True), name="static")
