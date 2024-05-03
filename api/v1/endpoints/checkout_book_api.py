from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from typing import Any

from api import deps

import controller
import schemas
import models

router = APIRouter()

@router.get('/get-all', response_model=schemas.CheckedOutBookBase)
async def get_all_checkout_books(
    db: Session = Depends(deps.get_db),
    page: int = 0,
    limit: int = 25,
    # current_user: models.Patron = Depends(deps.get_current_user),
) -> Any:
    """ Retrieve all checkedout books """
    checked_out_books = controller.checkedout_book.get_multi(db, offset=page, limit=limit)
    print('checked_out_books[0]: ', jsonable_encoder(checked_out_books[0].transactions.book_id))

    return JSONResponse(content={'data': jsonable_encoder(checked_out_books)})