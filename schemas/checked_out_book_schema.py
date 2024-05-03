from pydantic import BaseModel


class CheckedOutBookBase(BaseModel):
    """ Base model for OverdueBook table """
    transaction_id: str
    is_return_on_time: bool