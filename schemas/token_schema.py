from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    patron_id: Optional[str] = None
    username: Optional[str] = None
