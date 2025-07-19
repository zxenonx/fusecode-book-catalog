from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, description="Title")
    author: str = Field(..., min_length=1, description="Author")
    published_year: int = Field(..., gt=0, le=datetime.now().year, description="Published year")
    summary: Optional[str] = None

class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = Field(None, gt=0, le=2025)
    summary: Optional[str] = None

class Book(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
