from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Lider(Base, AuditMixin):
    """
    Modelo que representa un líder de nivel superior en la estructura organizacional.
    """
    __tablename__ = 'lideres'

    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    cedula = Column(Integer, nullable=False, unique=True)
    celular = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)

    id_pastor = Column(Integer, ForeignKey('pastores.id'), nullable=True)
    pastor = relationship("Pastor", backref="lideres")

    def __repr__(self):
        return f"<Lider(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"