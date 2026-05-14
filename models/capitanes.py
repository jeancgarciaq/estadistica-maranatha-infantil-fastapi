from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime, date
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

    @validates('fecha_nacimiento')
    def validar_fecha_nacimiento(self, key, value):
        """Calcula la edad automáticamente cuando se asigna la fecha de nacimiento."""
        if value:
            if isinstance(value, str):
                try:
                    fecha_dt = datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError:
                    return value
            else:
                fecha_dt = value
            
            today = date.today()
            self.edad = today.year - fecha_dt.year - ((today.month, today.day) < (fecha_dt.month, fecha_dt.day))
        return value