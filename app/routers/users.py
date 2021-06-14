from fastapi import APIRouter, Depends, HTTPException
from app.schemas import user
from typing import List

from sqlalchemy.orm import Session
from app.database.database import get_db

from app.services import users as services

router = APIRouter(prefix='/users', tags=['Users'])


@router.post("/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    db_user = services.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    return services.create_user(db, user)


@router.get("/", response_model=List[user.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = services.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=user.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = services.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
