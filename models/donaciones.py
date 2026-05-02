from sqlalchemy import Column, String, Float, Date
from models.database import Base
from models.base_class import AuditMixin

class Donacion(Base, AuditMixin):
    __tablename__ = "donaciones"

    descripcion = Column(String(255), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    equipo = Column(String(100), nullable=True)
    fecha = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Donacion(id={self.id}, descripcion='{self.descripcion}')>"