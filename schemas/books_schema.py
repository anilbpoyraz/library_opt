from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    category: str
    placement: str
    is_available: bool


class BookCreate(BookBase):
    pass


class BookUpdate(BookBase):
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    placement: Optional[str] = None
    is_available: Optional[bool] = None


class BookDelete(BookBase):
    id: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True
