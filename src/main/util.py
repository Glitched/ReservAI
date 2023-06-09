import os
from typing import Literal

Secret = Literal[
    "DB_USER",
    "DB_PASS",
    "DB_HOST",
    "DB_NAME",
    "JWT_SECRET",
    "VERIFICATION_TOKEN_SECRET",
    "RESET_PASSWORD_TOKEN_SECRET",
    "GOOGLE_OAUTH_CLIENT_ID",
    "GOOGLE_OAUTH_CLIENT_SECRET",
    "OAUTH_STATE_SECRET",
]


def get_secret(secret: Secret):
    """Read a secret from the environment variable."""
    cred = os.getenv(secret)

    # Return cred if it's defined
    if cred is not None:
        return cred

    # Throw in production, otherwise return "example-cred"
    if is_prod():
        raise Exception(f"Undefined secret: {secret}")

    return "example-cred"


def is_prod():
    """is_prod returns true if we're in production."""
    env = os.getenv("env", "dev")
    return env.lower() == "prod"
