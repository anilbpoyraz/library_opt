from sqlalchemy import Column, ForeignKey, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base

import json


class CheckedOutBook(Base):
    """ Model that checked out books """
    __tablename__ = 'checked_out_books'
    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    transaction_id = Column(UUID, ForeignKey('transactions.id'), unique=True)
    is_return_on_time = Column(Boolean, index=True, nullable=True)
    
    transactions = relationship('Transaction', primaryjoin='Transaction.id == CheckedOutBook.transaction_id')

    def __init__(self, transaction_id, is_return_on_time):
        super().__init__()
        self.transaction_id = transaction_id
        self.is_return_on_time = is_return_on_time
    
    def to_json(self):
        return json.loads(json.dumps({
            'transaction_id': self.transaction_id
        }))
