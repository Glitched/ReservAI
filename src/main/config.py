import os


class Config:
    """Configuration for the main app."""

    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=os.getenv("DB_USER"),
            DB_PASSWORD=os.getenv("DB_PASSWORD"),
            DB_HOST=os.getenv("DB_HOST"),
            DB_NAME=os.getenv("DB_NAME"),
        ),
    )


config = Config
