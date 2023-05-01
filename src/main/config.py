from main.util import get_secret


class Config:
    """Configuration for the main app."""

    DB_CONFIG = (
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=get_secret("DB_USER"),
            DB_PASSWORD=get_secret("DB_PASS"),
            DB_HOST=get_secret("DB_HOST"),
            DB_NAME=get_secret("DB_NAME"),
        ),
    )


config = Config
