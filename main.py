from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from schemas import (CategoryCreate, CategoryResponse,
                     NewCreate, NewResponse)
from database import get_db, engine, Base, MEDIA_DIR
import crud


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.mount(f'/{MEDIA_DIR}', StaticFiles(directory='media'),name='media')

#--category--
@app.post('/category/', response_model=CategoryResponse)
async def create_category_endpoint(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
        return await crud.create_category(category, db)

@app.get('/category/', response_model=list[CategoryResponse])
async def read_categories_endpoint(db: AsyncSession = Depends(get_db)):
        return await crud.read_categories(db)

@app.get('/category/{category_id}', response_model=CategoryResponse)
async def read_category_endpoint(category: int, db: AsyncSession = Depends(get_db)):
        return await crud.read_category(category, db)

@app.put('/category/{category_id}', response_model=CategoryResponse)
async def update_category_endpoint(category_id: int,category: CategoryCreate,db: AsyncSession = Depends(get_db)):
    return await crud.update_category(category_id, category, db)

@app.delete('/category/{category_id}', response_model=dict)
async def delete_category_endpoint(category: int, db: AsyncSession = Depends(get_db)):
        return await crud.delete_category(category, db)


#--new--
@app.post('/new/', response_model=NewResponse)
async def create_new_endpoint(name:str,
                              author: str,
                              category_id: int,
                              image: UploadFile = None,
                              video: UploadFile = None,
                              db: AsyncSession = Depends(get_db)
                              ):
        new = NewCreate(name=name, author=author, category_id=category_id)
        return await crud.create_new(new, db, image, video)

@app.get('/new/', response_model=list[NewResponse])
async def read_categories_endpoint(db: AsyncSession = Depends(get_db)):
        return await crud.read_categories(db)

@app.get('/new/{new_id}', response_model=NewResponse)
async def read_new_endpoint(new: int, db: AsyncSession = Depends(get_db)):
        return await crud.read_new(new, db)

@app.put('/new/{new_id}', response_model=NewResponse)
async def update_new_endpoint(new_id: int,new: NewCreate,db: AsyncSession = Depends(get_db)):
    return await crud.update_new(new_id, new, db)

@app.delete('/new/{new_id}', response_model=dict)
async def delete_new_endpoint(new: int, db: AsyncSession = Depends(get_db)):
        return await crud.delete_new(new, db)


if __name__ == '__main__':
    uvicorn.run(app)
