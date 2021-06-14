import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database import models
from app.database.database import engine
from app.routers.security import get_current_active_user
from app.routers import items, users, security, others

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['http://localhost', 'http://localhost:8080']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(items.router, dependencies=[
                   Depends(get_current_active_user)])
app.include_router(users.router, dependencies=[
                   Depends(get_current_active_user)])
app.include_router(security.router)
app.include_router(others.router, dependencies=[
                   Depends(get_current_active_user)])


@app.get("/")
async def root():
    return {'message': 'Hello world'}


if __name__ == "__main__":
    # This is needed for debugging
    uvicorn.run(app, host='0.0.0.0', port=8000)
