from pydantic import BaseModel


class OverdueBookBase(BaseModel):
    """ Base model for OverdueBook table """
    transaction_id: str