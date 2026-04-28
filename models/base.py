from datetime import datetime
import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class SyncMixin:
	"""Campos compartidos para sincronización entre dispositivos."""

	sync_id = Column(String(36), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
	created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
	updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
	is_deleted = Column(Boolean, nullable=False, default=False)