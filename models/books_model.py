from sqlalchemy import Column, String, DateTime, text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base

import json
import datetime

class Book(Base):
    __tablename__ = 'books'

    id = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    created_at = Column(DateTime, index=True, default=datetime.datetime.now)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)
    placement = Column(String, index=True, nullable=False)
    is_available = Column(Boolean, index=True, nullable=False, server_default='t')

    def __init__(self, title, author, category, placement, is_available):
        super().__init__()
        self.title = title
        self.author = author
        self.category = category
        self.placement = placement
        self.is_available = is_available

    
    def to_json(self):
        return json.loads(json.dumps({
            'id': self.id,
            'created_at': self.created_at,
            'title': self.title,
            'author': self.author,
            'category': self.category,
            'placement': self.placement,
            'is_availbale': self.is_available
        }))

