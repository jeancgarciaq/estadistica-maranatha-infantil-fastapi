from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Capitan(Base, AuditMixin):
    """
    Modelo que representa un capitán, quien reporta a un coordinador.
    """
    __tablename__ = 'capitanes'

    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    cedula = Column(Integer, nullable=False, unique=True)
    celular = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)
    
    id_coordinador = Column(Integer, ForeignKey('coordinadores.id'), nullable=True)
    coordinador = relationship("Coordinador", backref="capitanes")

    def __repr__(self):
        return f"<Capitan(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"