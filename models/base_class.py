from sqlalchemy import Column, Integer, Boolean, DateTime, String
from datetime import datetime
import uuid

def generar_uuid():
    return str(uuid.uuid4())

class AuditMixin:
    """Campos comunes para todos los modelos."""
    # ID autoincremental (funciona tanto en SQLite como en PostgreSQL)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # UUID único para sincronización
    sync_id = Column(String(36), nullable=False, unique=True, default=generar_uuid)

    # Marca de borrado lógico y timestamps
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)