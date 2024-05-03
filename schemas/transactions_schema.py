from pydantic import BaseModel

from typing import Optional


class TransactionBase(BaseModel):
    book_id: str
    patron_id: str
    checkout_date: str
    return_date: str
    user_return_date: Optional[str] = None
    is_active: bool


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    book_id: Optional[str] = None
    patron_id: Optional[str] = None
    checkout_date: Optional[str] = None
    return_date: Optional[str] = None
    user_return_date: Optional[str] = None
    is_active: Optional[bool] = None