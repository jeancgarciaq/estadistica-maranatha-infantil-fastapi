from sqlalchemy import Column, Integer, Boolean, DateTime, String
from datetime import datetime
import uuid

class AuditMixin:
    """Campos comunes para todos los modelos."""
    # ID autoincremental para rendimiento local en SQLite
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # UUID global para evitar colisiones en la sincronización con Firebase
    sync_id = Column(String(36), unique=True, nullable=False, index=True, default=lambda: str(uuid.uuid4()))
    
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Sincronización (opcional para traza local)
    last_sync = Column(DateTime, nullable=True)