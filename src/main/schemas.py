import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Basic information provided when a user is read."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Basic information provided when a user is created."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Basic information provided when a user is updated."""

    pass
