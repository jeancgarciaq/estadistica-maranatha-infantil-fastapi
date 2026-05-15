from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime, date
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

    @validates('fecha_nacimiento')
    def validar_fecha_nacimiento(self, key, value):
        """Calcula la edad automáticamente cuando se asigna la fecha de nacimiento."""
        if value and value != "":
            if isinstance(value, str):
                try:
                    fecha_dt = datetime.strptime(value.split('T')[0], '%Y-%m-%d').date()
                except ValueError:
                    return None
            else:
                fecha_dt = value
            
            if isinstance(fecha_dt, (date, datetime)):
                today = date.today()
                self.edad = today.year - fecha_dt.year - ((today.month, today.day) < (fecha_dt.month, fecha_dt.day))
            return fecha_dt
        return None