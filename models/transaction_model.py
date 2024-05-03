from sqlalchemy import Column, ForeignKey, String, DateTime, text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base

import json
import datetime


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    book_id = Column(UUID, ForeignKey('books.id'))
    patron_id = Column(UUID, ForeignKey('patrons.id'))
    checkout_date = Column(DateTime, default=datetime.datetime.now)
    return_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, index=True, server_default='t', nullable=False)
    user_return_date = Column(DateTime, nullable=True)
    books = relationship('Book', primaryjoin='Book.id == Transaction.book_id')
    patrons = relationship('Patron', primaryjoin='Patron.id == Transaction.patron_id')

    def __init__(self, book_id, patron_id, checkout_date, return_date, user_return_date, is_active):
        super().__init__()
        self.book_id = book_id
        self.patron_id = patron_id
        self.checkout_date = checkout_date
        self.return_date = return_date
        self.is_active = is_active
        self.user_return_date = user_return_date

    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'book_id': self.book_id,
            'patron_id': self.patron_id,
            'checkout_date': self.checkout_date,
            'return_date': self.return_date,
            'is_active': self.is_active,
        }))
