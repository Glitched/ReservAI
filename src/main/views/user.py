from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.user import User as UserModel

router = APIRouter(prefix="/user", tags=["user"])


class UserSchemaBase(BaseModel):
    email: str | None = None
    full_name: str | None = None


class UserSchemaCreate(UserSchemaBase):
    pass


class UserSchema(UserSchemaBase):
    id: str

    class Config:
        orm_mode = True


@router.get("/get-user", response_model=UserSchema)
async def get_user(id: str, db: AsyncSession = Depends(get_db)):
    """Get info about a user by ID."""
    user = await UserModel.get(db, id)
    return user


@router.get("/get-users", response_model=list[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    """Get info about all users."""
    users = await UserModel.get_all(db)
    return users


@router.post("/create-user", response_model=UserSchema)
async def create_user(user: UserSchemaCreate, db: AsyncSession = Depends(get_db)):
    """Create a new user."""
    user = await UserModel.create(db, **user.dict())
    return user
