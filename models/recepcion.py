from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Recepcion(Base, AuditMixin):
    __tablename__ = 'recepciones'

    nombre = Column(String)
    fecha = Column(Date)

    distribuciones = relationship("Distribucion", back_populates="recepcion")

    def __repr__(self):
        return f"Recepcion(id={self.id}, nombre='{self.nombre}', fecha='{self.fecha}')"
