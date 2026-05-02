from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import validates

from models.database import Base
from models.base_class import AuditMixin


class SyncQueue(Base, AuditMixin):
    __tablename__ = 'sync_queue'

    entity_name = Column(String(80), nullable=False, index=True)
    entity_sync_id = Column(String(36), nullable=False, index=True)
    operation = Column(String(20), nullable=False, default='upsert')
    payload_json = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default='pending')
    attempts = Column(Integer, nullable=False, default=0)
    last_error = Column(Text, nullable=True)
    processed_at = Column(DateTime, nullable=True)

    @validates('operation')
    def validate_operation(self, key, value):
        value = (value or '').strip().lower()
        if value not in {'upsert', 'delete'}:
            raise ValueError("operation must be 'upsert' or 'delete'")
        return value