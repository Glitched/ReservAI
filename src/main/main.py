from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import config
from .database import sessionmanager

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

    from .views.user import router as user_router

    server.include_router(user_router, prefix="/api", tags=["user"])
    return server


app = init_app()


@app.get("/hello")
def read_root():
    """Let's just prove the server works."""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    """Temporary function."""
    return {"item_id": item_id, "q": q}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
