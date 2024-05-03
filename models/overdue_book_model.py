from sqlalchemy import Column, ForeignKey, String, DateTime, text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base

import json


class OverdueBook(Base):
    """ Model that stores overdue books by patrons """
    __tablename__ = 'overdue_books'
    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    transaction_id = Column(UUID, ForeignKey('transactions.id'), unique=True)
    overdue_days = Column(Integer, nullable=False, index=True)
    
    transactions = relationship('Transaction', primaryjoin='Transaction.id == OverdueBook.transaction_id')

    def __init__(self, transaction_id, overdue_days):
        super().__init__()
        self.transaction_id = transaction_id
        self.overdue_days = overdue_days
    
    def to_json(self):
        return json.loads(json.dumps({
            'transaction_id': self.transaction_id,
            'overdue_days': self.overdue_days
        }))