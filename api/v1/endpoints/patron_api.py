from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from api import deps
from core.security import get_password_hash

import models
import controller
import schemas

router = APIRouter()


@router.post("/create", response_model=schemas.PatronBase)
async def create_user(
    patron_add: schemas.PatronCreate,
    db: Session = Depends(deps.get_db),
    # current_user: models.Patron = Depends(deps.get_current_user),
) -> Any:
    """ Create a new user """
    patron = controller.patron.get_by_email(db, email=patron_add.email)
    if patron:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists!"
        )
    patron_add.password = get_password_hash(patron_add.password)
    patron = controller.patron.create(db, obj_in=patron_add)

    return JSONResponse(content={'data': jsonable_encoder(patron)})
