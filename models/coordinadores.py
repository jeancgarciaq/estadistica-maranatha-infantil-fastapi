from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Coordinador(Base, AuditMixin):
    """
    Modelo que representa un coordinador, quien reporta a un líder.
    """
    __tablename__ = 'coordinadores'

    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    cedula = Column(Integer, nullable=False, unique=True)
    celular = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)
    
    id_lider = Column(Integer, ForeignKey('lideres.id'), nullable=True)
    lider = relationship("Lider", backref="coordinadores")

    def __repr__(self):
        return f"<Coordinador(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"