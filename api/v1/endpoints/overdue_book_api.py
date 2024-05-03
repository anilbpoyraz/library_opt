from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from typing import Any
from api import deps

import controller
import schemas


router = APIRouter()

@router.get('/get-all', response_model=schemas.OverdueBookBase)
async def get_all_overdue_books(
    db: Session = Depends(deps.get_db),
    page: int = 0,
    limit: int = 25,
    # current_user: models.Patron = Depends(deps.get_current_user),
) -> Any:
    """ Retrieve all overdue books """
    overdue_books = controller.overdue_book.get_multi(db, offset=page, limit=25)

    return JSONResponse(content={'data': jsonable_encoder(overdue_books)})