from typing import Optional
from pydantic import BaseModel

#--category--
class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        from_attributes = True


#--New--
class NewCreate(BaseModel):
    name: str
    author: str
    image: Optional[str] = None
    video: Optional[str] = None
    category_id: int

class NewResponse(NewCreate):
    id: int

    class Config:
        from_attributes = True