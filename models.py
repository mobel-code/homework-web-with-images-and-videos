from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    news: Mapped[list["New"]] =  relationship("New", back_populates="category")


class New(Base):
    __tablename__ = 'news'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(122))
    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    video: Mapped[Optional[str]] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id')) #---- soravolish kerag nega uchun ulaganimizni
    category: Mapped["Category"] = relationship("Category", back_populates="")
