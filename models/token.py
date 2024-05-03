from sqlalchemy import Boolean, Column, ForeignKey, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from db.base_class import Base

import json


class Tokens(Base):
    __tablename__ = 'tokens'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    token = Column(String, unique=False, nullable=False, index=True)
    is_active = Column(Boolean, nullable=False, server_default='t', index=True)
    patron_id = Column(ForeignKey('patrons.id'), nullable=False, index=True)

    patrons = relationship('Patron', primaryjoin='Patron.id == Tokens.patron_id')

    def __init__(self, token, is_active, patron_id):
        super().__init__()
        self.token = token
        self.patron_id = patron_id
        self.is_active = is_active
    
    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'token': self.token,
            'patron_id': self.patron_id,
            'patron_name': self.patrons.first_name + ' ' + self.patrons.last_name
        }))