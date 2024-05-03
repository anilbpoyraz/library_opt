from controller.base import BaseController

import models
import schemas


class OverdueBookController(
    BaseController[
        models.OverdueBook, schemas.OverdueBookBase,
        schemas.OverdueBookBase, schemas.OverdueBookBase
    ]
):
    def __init__(self, model):
        super().__init__(model)


overdue_book = OverdueBookController(models.OverdueBook)