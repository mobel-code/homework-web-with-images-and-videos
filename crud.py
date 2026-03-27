from pathlib import Path
import shutil
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas import (CategoryCreate, CategoryResponse,
                     NewCreate, NewResponse)
from models import Category, New
from fastapi import HTTPException, UploadFile
from database import MEDIA_DIR
#--category--
async def create_category(category: CategoryCreate, db: AsyncSession) -> CategoryResponse:
    db_category = Category(**category.model_dump())
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return CategoryResponse.model_validate(db_category)

async def read_categories(db: AsyncSession) -> list[CategoryResponse]:
    results = await db.execute(select(Category))
    return [CategoryResponse.model_validate(category)for category in results.scalar().all()]

async def read_category(category_id: int, db: AsyncSession) -> CategoryResponse:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='hato')

    return CategoryResponse.model_validate(category)


async def update_category(category_id: int,category: CategoryCreate, db: AsyncSession) -> CategoryResponse:
    db_category = await db.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail='hato')

    for attr, value in category.__dict__.items():
        setattr(db_category, attr, value)

    await db.commit()
    await db.refresh(db_category)
    return CategoryResponse.model_validate(db_category)


async def delete_category(category_id: int, db: AsyncSession) -> CategoryResponse:
    category = await db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail='hato')

    await db.delete(category)
    await db.commit()

    return {'message': "ochirildi"}

#--new---
async def create_news(
        new: NewCreate,
        db: AsyncSession,
        image: UploadFile = None,
        video: UploadFile = None
) -> NewResponse:

    if image:
        image_extension = image.filename.split('.'[-1])
        if image_extension.lower() not in ['jpg', 'jpeg', 'png', 'bmp']:
            raise HTTPException(status_code=404, detail='hato')

    if video:
        video_extension = image.filename.split('.'[-1])
        if video_extension.lower() not in ['mp4','avi','mow']:
            raise HTTPException(status_code=404, detail='hato')

    db_new = New(**new.model_dump())
    db.add(db_new)
    await db.commit()
    await db.refresh(db_new)

    if image:
        image_path = Path(MEDIA_DIR) / f'new_{db_new.id}_image.{image_extension}'
        with image_path.open(mode="wb") as buffer:
            shutil.copyfile(image.filename, buffer)

        db_new.image = str(image_path)

    if video:
        video_path = Path(MEDIA_DIR) / f'new_{db_new.id}_video.{video_extension}'
        with video_path.open(mode="wb") as buffer:
            shutil.copyfile(video.filename, buffer)

        db_new.video = str(video_path)

    await db.commit()
    await db.refresh(db_new)
    return NewResponse.model_validate(db_new)

async def read_news(db: AsyncSession) -> list[NewResponse]:
    results = await db.execute(select(New))
    return [NewResponse.model_validate(new)for new in results.scalar().all()]

async def read_new(new_id: int, db: AsyncSession) -> NewResponse:
    new = await db.get(New, new_id)
    if not new:
        raise HTTPException(status_code=404, detail='hato')

    return NewResponse.model_validate(new)


async def update_new(new_id: int,new: NewCreate, db: AsyncSession) -> NewResponse:
    db_new = await db.get(New, new_id)
    if not db_new:
        raise HTTPException(status_code=404, detail='hato')

    for attr, value in new.__dict__.items():
        setattr(db_new, attr, value)

    await db.commit()
    await db.refresh(db_new)
    return NewResponse.model_validate(db_new)


async def delete_new(new_id: int, db: AsyncSession) -> NewResponse:
    new = await db.get(New, new_id)
    if not new:
        raise HTTPException(status_code=404, detail='hato')

    await db.delete(new)
    await db.commit()

    return {'message': "ochirildi"}



