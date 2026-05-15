from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime, date
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

    id_area = Column(Integer, ForeignKey('areas.id'), nullable=True)
    area = relationship("Area", back_populates="coordinadores")

    def __repr__(self):
        return f"<Coordinador(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"

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