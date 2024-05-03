from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import Any, List
import controller
import schemas
import models
from api import deps
from uuid import uuid4


router = APIRouter()


@router.post("/create", response_model=schemas.BookBase, summary="Create a new book", tags=["books"])
async def create_book(
    add: schemas.BookCreate,
    db: Session = Depends(deps.get_db),
    # current_user: models.Patron = Depends(deps.get_current_user)
) -> Any:
    """ Create a new book """
    data = controller.book.create(db, obj_in=add)
    return JSONResponse(content={'data': jsonable_encoder(data)})

@router.get("", response_model=schemas.BookBase)
async def read_book(
    book_id: str, 
    db: Session = Depends(deps.get_db)
) -> Any:
    """ Get a book by id """
    db_book = controller.book.get(db=db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.patch("/update", response_model=schemas.BookBase)
async def update_book(
    book_id: str, update_data: schemas.BookUpdate, db: Session = Depends(deps.get_db)
)-> Any:
    """ Update a book by id """
    db_book = controller.book.get(db=db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = controller.book.update(
        db=db,
        db_obj=db_book,
        obj_in=update_data.dict(exclude_unset=True)
    )
    
    return updated_book

@router.delete("/books/{book_id}", response_model=schemas.BookBase)
async def delete_book(
    book_id: str, db: Session = Depends(deps.get_db)
) -> Any:
    """ Delete a book by id """
    db_book = controller.book.get(db=db, id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return controller.book.remove(db=db, id=book_id)
