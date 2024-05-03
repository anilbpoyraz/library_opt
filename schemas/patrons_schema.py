from pydantic import BaseModel, Field

from uuid import UUID, uuid4
from typing import Optional


class PatronBase(BaseModel):
    """ Patron object base schema class """
    first_name: str
    last_name: str
    email: str


class PatronCreate(PatronBase):
    """ Patron object create schema class """
    password: str


class PatronUpdate(PatronBase):
    """ Patron object update schema class  """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class PatrondDelete(PatronBase):
    """ Patron object delete schema class """
    id: UUID = Field(default_factory=uuid4)
    
    class Config:
        orm_mode = True


class PatronsLogin(BaseModel):
    """ Schema class for Patron login """
    email: Optional[str]
    password: Optional[str]
