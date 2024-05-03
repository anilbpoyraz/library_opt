from pydantic import BaseModel, Field

from uuid import UUID, uuid4
from typing import Optional


class PatronBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class PatronCreate(PatronBase):
    password: str


class PatronUpdate(PatronBase):
    password: str


class PatrondDelete(PatronBase):
    id: UUID = Field(default_factory=uuid4)
    
    class Config:
        orm_mode = True


class PatronsLogin(BaseModel):
    email: Optional[str]
    password: Optional[str]
