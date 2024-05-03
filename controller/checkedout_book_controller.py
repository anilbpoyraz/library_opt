from controller.base import BaseController

import models
import schemas

class CheckoutBookController(
    BaseController[
        models.CheckedOutBook, schemas.CheckedOutBookBase,
        schemas.CheckedOutBookBase, schemas.CheckedOutBookBase
    ]
):
    def __init__(self, model):
        super().__init__(model)

checkedout_book = CheckoutBookController(models.CheckedOutBook)