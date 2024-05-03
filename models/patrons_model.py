from sqlalchemy import Column, ForeignKey, String, DateTime, text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID

from db.base_class import Base

import json
import datetime

class Patron(Base):
    __tablename__ = 'patrons'

    id = Column(UUID, primary_key=True, unique=True, server_default=text("uuid_generate_v4()"))
    created_at = Column(DateTime, index=True, default=datetime.datetime.now)
    first_name = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    overdue_count = Column(Integer, nullable=True, server_default='0')
    is_active = Column(Boolean, index=True, server_default='t')
    password = Column(String, index=True, nullable=False)

    def __init__(self, first_name, last_name, email, password):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
    
    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }))
