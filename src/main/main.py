from typing import Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from main.models.user import User
from main.util import get_secret

app = FastAPI()


cookie_transport = CookieTransport(cookie_name="auth", cookie_samesite="strict")


def get_jwt_strategy():
    """Get a fastapi-users JWTStrategy."""
    strat: JWTStrategy[User, Any] = JWTStrategy(
        secret=get_secret("JWT_SECRET"), lifetime_seconds=3600
    )
    return strat


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
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
