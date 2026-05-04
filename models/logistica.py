from sqlalchemy import Column, String, Date, Integer

from models.database import Base
from models.base_class import AuditMixin

class Logistica(Base, AuditMixin):
    __tablename__ = 'logisticas'

    almacen = Column(Integer, nullable=False, default=0)
    capitan = Column(Integer, nullable=False, default=0)
    distribucion = Column(Integer, nullable=False, default=0)
    hidratacion = Column(Integer, nullable=False, default=0)
    pasillo = Column(Integer, nullable=False, default=0)
    secretaria = Column(Integer, nullable=False, default=0)
    fecha = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Logistica(id={self.id}, capitan='{self.capitan}', fecha='{self.fecha}')>"