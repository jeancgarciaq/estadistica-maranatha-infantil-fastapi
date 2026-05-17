from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import validates
from models.database import Base
from datetime import datetime
from models.base_class import AuditMixin

class Ensenanza(Base, AuditMixin):
    __tablename__ = 'ensenanzas'

    capitan = Column(String)
    subcapitan = Column(Integer)
    fecha = Column(Date)

    def __repr__(self):
        return f"Ensenanza(id={self.id}, capitan='{self.capitan}', subcapitan={self.subcapitan}, fecha='{self.fecha}')"

    @validates('fecha')
    def validar_fecha(self, key, value):
        """Maneja fechas en formato string provenientes de formularios."""
        if value and isinstance(value, str):
            try:
                return datetime.strptime(value.split('T')[0], '%Y-%m-%d').date()
            except ValueError:
                return None
        return value
