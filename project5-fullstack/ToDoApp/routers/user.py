from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from pydantic import BaseModel, Field

from ..database import SessionLocal
from ..models import Todos, Users
from .auth import get_current_user, bcrypt_context



router = APIRouter(
    prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=5)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    return db.query(Users).filter(Users.id == user.get('id')).first()



@router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id'))\
                                .first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User model not found')

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put('/change_phone_number/', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency,
                              new_phone_number: str = Query(min_length=10, max_length=13)):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id'))\
                                .first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User model not found')

    user_model.phone_number = new_phone_number
    db.add(user_model)
    db.commit()
