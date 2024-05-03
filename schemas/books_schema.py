from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional

class BookBase(BaseModel):
    """ Book object base schema class """
    title: str
    author: str
    category: str
    placement: str
    is_available: bool


class BookCreate(BookBase):
    """ Book object create schema class """
    pass


class BookUpdate(BookBase):
    """ Book object update schema class  """
    title: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    placement: Optional[str] = None
    is_available: Optional[bool] = None


class BookDelete(BookBase):
    """ Book object delete schema class """
    id: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True
