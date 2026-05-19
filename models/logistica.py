from sqlalchemy import Column, String, Date, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.database import Base
from models.base_class import AuditMixin

class Logistica(Base, AuditMixin):
    __tablename__ = 'logisticas'

    fecha = Column(Date, nullable=False, index=True)
    observaciones = Column(Text, nullable=True)
    # Nota: Los capitanes y servidores ahora se consultan vía AsistenciaServidor

    def __repr__(self):
        return f"<Logistica(id={self.id}, fecha='{self.fecha}')>"