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

@router.get("/get", response_model=schemas.PatronBase)
async def get_users(
    db: Session = Depends(deps.get_db),
    page: int = 0,
    limit: int = 25,
    # current_user: models.Patron = Depends(deps.get_current_user),
) -> Any:
    """ Get all patrons """
    patrons = controller.patron.get_multi(db, offset=page, limit=limit)

    return JSONResponse(content={'data': jsonable_encoder(patrons)})

@router.patch("/update", response_model=schemas.PatronBase)
async def update_user(
    patron_id: str, update_data: schemas.PatronUpdate,
    db: Session = Depends(deps.get_db)
) -> Any:
    """ Update patron by id """

    db_patron = controller.patron.get(db=db, id=patron_id)
    print('db_patron: ', db_patron)
    if db_patron is None:
        raise HTTPException(status_code=404, detail="Patron not found")
    
    if 'password' in update_data:
        db_patron.password = get_password_hash(update_data.password)

    updated_patron = controller.patron.update(
        db=db,
        db_obj=db_patron,
        obj_in=update_data.dict(exclude_unset=True)
    )

    return updated_patron

@router.delete('/delete', response_model=schemas.PatrondDelete)
async def delete_patron(
    patron_id: str, db: Session = Depends(deps.get_db)
) -> Any:
    """ Delete patron by id """
    db_patron = controller.patron.get(db=db, id=patron_id)
    if db_patron is None:
        raise HTTPException(status_code=404, detail="Patron not found")
    
    return controller.patron.remove(db=db, id=patron_id)