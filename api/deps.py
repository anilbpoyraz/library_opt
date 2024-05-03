from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from typing import Generator

import controller
import controller.patron_controller
import models
import schemas

from core import security
from core.config import settings
from db.database import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/api-login"
)

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> models.Patron:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY, 
            algorithms=[settings.HASH_ALGORITHM]
        )
        print('payload: ', payload)
        token_data = schemas.TokenPayload(**payload)
        print('token_data: ', token_data)
    except (jwt.JWTError , ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate cretentials"
        )
    patron = controller.patron.get(db, id=token_data.patron_id)
    if not controller.patron:
        raise HTTPException(status_code=404, detail="User not found")
    
    return patron

def get_current_active_user(
        current_user: models.Patron = Depends(get_current_user),
) -> models.Patron: 
    if not controller.patron.is_active(current_user):
        raise HTTPException(status_code=400, detail='Inactive user')
    
    return current_user
