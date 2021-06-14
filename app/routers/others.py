from fastapi import APIRouter, Body, Path, Query, Cookie, Header, status
from fastapi.encoders import jsonable_encoder
from typing import Optional, List, Set
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from enum import Enum


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title='The descriptionof the item', max_length=300
    )
    price: float = Field(..., gt=0,
                         description='The price must be greater than 0')
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[Image]] = None


class UserBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    hashed_password: str


class ModelName(str, Enum):
    teste = 'new_test_value'
    gest = 'lenet'


router = APIRouter(prefix='/others', tags=['Others'])


@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {'item_id': item_id}


@router.get("/models")
async def get_model(model_name: ModelName):
    return {'model_name': model_name}


@router.post("/items/{item_id}")
async def create_item(item_id: int, item: Item, user: UserBase, importance: int = Body(...)):
    results = {"item_id": item_id, "item": item,
               "user": user, "importance": importance}
    return results


@router.post("/body_embedded/")
async def body_embedded(user: UserBase = Body(..., embed=True)):
    results = {"user": user}
    return results


@router.get("/query_param_with_validation/")
async def read_items(q: Optional[str] = Query(None, max_length=50, regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@router.get("/required_query_param/")
async def read_items_with_query(q: str = Query(..., max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@router.get("/query_params_list/")
async def query_params_list(q: Optional[List[str]] = Query(None)):
    # Must use Query, else it will be interpreted as request body
    query_items = {"q": q}
    return query_items


@router.get("/query_params_list_with_defaults/")
async def list_with_defaults(q: List[str] = Query(['foo', 'bar'])):
    # Must use Query, else it will be interpreted as request body
    query_items = {"q": q}
    return query_items


@router.get("/path_param_with_validation/{id}")
async def path_param_with_validation(
    q: str,
    id: int = Path(
        ...,
        title="Id of item to get",
        deprecated=True,
        ge=1)
):
    results = {"id": id}
    if q:
        results.update({"q": q})
    return results


@router.get("/cookie_param")
async def cookie_param(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


@router.get("/header_param")
async def header_param(user_agent: Optional[str] = Header(None)):
    return {'User-Agent': user_agent}


@router.get("/header_not_hyphen",
            description='''Will not convert underscores to hyphens, as is common 
    for header parameters''')
async def header_not_hyphen(
    strange_header: Optional[str] = Header(None, convert_underscore=False)
):
    return {'strange-header': strange_header}


@router.get("/duplicate_headers",
            description='''Can receive multiple values for a header''')
async def duplicate_headers(x_token: Optional[List[str]] = Header(None)):
    return {'X-Token values': x_token}


@router.post("/response_model", response_model=UserOut)
async def response_model(user: UserIn):
    hashed_password = "supersecret" + user.password
    user_out = UserOut(**user.dict(), hashed_password=hashed_password)
    return user_out


@router.post("/response_with_status_code", status_code=status.HTTP_201_CREATED)
async def response_with_status_code(name: str):
    return {'name': name}


fake_db = {}


class ItemWithTimestamp(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


@router.put("/convert_to_jsonable/{item_id}", tags=["jsonable"])
async def convert_to_jsonable(item_id: str, item: ItemWithTimestamp):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[item_id] = json_compatible_item_data
    return json_compatible_item_data
