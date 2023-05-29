from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from .auth import current_active_user, google_oauth_router
from .config import config
from .database import sessionmanager
from .models.user import User


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


# Register our google oauth routes to /auth/google/...
app.include_router(
    google_oauth_router,
    prefix="/auth/google",
    tags=["auth"],
)


@app.get("/auth")
def read_auth(user: User = Depends(current_active_user)):
    """Let's just prove auth works."""
    return {"message": "You are logged in!", "email": user.email}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Temporary function."""
    return {"item_id": item_id, "q": q}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
