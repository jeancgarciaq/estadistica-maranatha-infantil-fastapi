from sqlalchemy import Column, String, Date, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.database import Base
from models.base_class import AuditMixin

class Logistica(Base, AuditMixin):
    __tablename__ = 'logisticas'

    fecha = Column(Date, nullable=False, index=True)
    id_capitan = Column(Integer, ForeignKey('servidores.id'), nullable=True)
    observaciones = Column(Text, nullable=True)

    # Campos de resumen (se calculan para compatibilidad con reportes)
    almacen = Column(Integer, default=0)
    distribucion = Column(Integer, default=0)
    hidratacion = Column(Integer, default=0)
    pasillo = Column(Integer, default=0)
    secretaria = Column(Integer, default=0)
    capitan = Column(Integer, default=0) # Conteo para reportes

    capitan_encargado = relationship("Servidor", foreign_keys=[id_capitan])

    def __repr__(self):
        return f"<Logistica(id={self.id}, fecha='{self.fecha}')>"