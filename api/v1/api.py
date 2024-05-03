from fastapi import APIRouter

from api.v1.endpoints import book_api, login_api, patron_api, transaction_api, checkout_book_api, overdue_book_api

api_router = APIRouter()
api_router.include_router(login_api.router, tags=["login"])
api_router.include_router(patron_api.router, prefix='/patron', tags=["patrons"])
api_router.include_router(book_api.router, prefix='/books', tags=["books"])
api_router.include_router(transaction_api.router, prefix='/transaction', tags=["transactions"])
api_router.include_router(checkout_book_api.router, prefix='/checkoutbooks', tags=["checkedout_books"])
api_router.include_router(overdue_book_api.router, prefix='/overduebooks', tags=["overdue_books"])
