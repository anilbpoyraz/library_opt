from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import  JSONResponse
from sqlalchemy.orm import Session

import controller
import models
import schemas
from api import deps
from core import security
from core.config import settings

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login_access_token(
    db: Session = Depends(deps.get_db),
    login_data: schemas.PatronsLogin = Body()
) -> Any:
    """ 
    OAuth2 compatible token login, get an access token for future requests 
    """
    patron = controller.patron.authenticate(
        db, email=login_data.email, password=login_data.password
    )
    if not patron:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not controller.patron.is_active(patron):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "patron_id": patron.id,
        "email": patron.email
    }
    result = {
        "access_token": security.create_access_token(
            token_data, 
            expires_delta=access_token_expires
        ),
        "token_type": "Bearer",
    }
    
    return result
