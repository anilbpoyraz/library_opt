from controller.base import BaseController

import models
import schemas


class TransactionController(
    BaseController[
        models.Transaction, schemas.TransactionBase, 
        schemas.TransactionUpdate, schemas.TransactionBase]
):
    def __init__(self, model):
        super().__init__(model)

transaction = TransactionController(models.Transaction)