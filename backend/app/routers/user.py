from fastapi import APIRouter
from pydantic import BaseModel

from app.database import SessionLocal
from app.models.user import User

router = APIRouter()


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


@router.post("/")
def create_user(user: UserCreate):
    db = SessionLocal()

    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }