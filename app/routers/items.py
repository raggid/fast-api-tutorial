from fastapi import APIRouter, Depends
from app.schemas import item
from typing import List

from sqlalchemy.orm import Session
from app.database.database import get_db

from app.services import items as service


router = APIRouter(prefix='/items', tags=['Items'])


@router.get("/items/", response_model=List[item.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = service.get_items(db, skip=skip, limit=limit)
    return items


@router.post("/{user_id}/items/", response_model=item.Item)
def create_item_for_user(
    user_id: int, item: item.ItemCreate, db: Session = Depends(get_db)
):
    return service.create_user_item(db=db, item=item, user_id=user_id)
