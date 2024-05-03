import models
import schemas
from controller.base import BaseController


class BookController(
    BaseController[models.Book, schemas.BookBase, schemas.BookUpdate, schemas.BookDelete]
):
    """ Book class controller """
    def __init__(self, model):
        super().__init__(model)


book = BookController(models.Book)