from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session
from typing import Any
from api import deps

import controller
import models
import schemas

import datetime



router = APIRouter()


@router.post("/create", response_model=schemas.TransactionBase)
async def create_transaction(
    transaction_data: schemas.TransactionBase = Body(),
    db: Session = Depends(deps.get_db),
    # current_user: models.Transaction = Depends(deps.get_current_user),
) -> Any:
    """ Create a transaction """
    db_book = controller.book.get(db=db, id=transaction_data.book_id)
    db_patron = controller.patron.get(db=db, id=transaction_data.patron_id)
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_patron is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_book_status = {
        'is_available': False
    }
    controller.book.update(
        db=db, db_obj=db_book, 
        obj_in=update_book_status
    )    
    data = controller.transaction.create(db, obj_in=transaction_data)

    return JSONResponse(content={'data': jsonable_encoder(data)})

@router.post("/transaction-status", response_model=schemas.TransactionBase)
async def update_transaction(
    transaction_id: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """ Update transaction is_active key """
    db_transaction = controller.transaction.get(db=db, id=transaction_id)

    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transactin not found")
    
    transaction_status = {
        'is_active': False,
        'user_return_date': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    }
    
    updated_transaction = controller.transaction.update(
        db=db, db_obj=db_transaction, 
        obj_in=transaction_status
    )

    if datetime.datetime.now() > db_transaction.return_date:
        overdue_days = (datetime.datetime.now() - db_transaction.return_date).days
        overdue_book_data = {
            'transaction_id': transaction_id,
            'overdue_days': overdue_days,
        }
        controller.overdue_book.create(db=db, obj_in=overdue_book_data)
        is_return_on_time = False
        pass
    else:
        is_return_on_time = True

    db_book = controller.book.get(db=db, id=str(db_transaction.book_id))
    update_book_status = {
        'is_available': True,
    }
    controller.book.update(
        db=db, db_obj=db_book, 
        obj_in=update_book_status
    )
    checkout_book_data = {
        'transaction_id': transaction_id,
        'is_return_on_time' : is_return_on_time,
    }
    controller.checkedout_book.create(db=db, obj_in=checkout_book_data)

    return JSONResponse(content={'data': jsonable_encoder(updated_transaction)})