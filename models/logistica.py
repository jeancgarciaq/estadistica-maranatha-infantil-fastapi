from sqlalchemy import Column, String, Date

from models.database import Base
from models.base_class import AuditMixin

class Logistica(Base, AuditMixin):
    __tablename__ = 'logisticas'

    almacen = Column(String(100), nullable=False)
    capitan = Column(String(100), nullable=False)
    distribucion = Column(String(255), nullable=True)
    hidratacion = Column(String(255), nullable=True)
    pasillo = Column(String(255), nullable=True)
    secretaria = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Logistica(id={self.id}, capitan='{self.capitan}', fecha='{self.fecha}')>"