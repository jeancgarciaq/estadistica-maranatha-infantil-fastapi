from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime, date
from models.database import Base
from models.base_class import AuditMixin

class Servidor(Base, AuditMixin):
    """
    Modelo que representa un servidor (persona de servicio) en la base de datos.
    """
    __tablename__ = 'servidores'

    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    cedula = Column(Integer, nullable=False, unique=True)
    celular = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)
    numero_equipo = Column(Integer, nullable=True)

    id_area = Column(Integer, ForeignKey('areas.id'), nullable=True)
    area = relationship("Area", backref="servidores")

    id_capitan = Column(Integer, ForeignKey('capitanes.id'), nullable=True)
    capitan = relationship("Capitan", backref="servidores")

    def __repr__(self):
        return f"<Servidor(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"

    @validates('fecha_nacimiento')
    def validar_fecha_nacimiento(self, key, value):
        """Calcula la edad automáticamente cuando se asigna la fecha de nacimiento."""
        if value:
            # Si viene como string desde el formulario, convertirlo a objeto date
            if isinstance(value, str):
                try:
                    fecha_dt = datetime.strptime(value, '%Y-%m-%d').date()
                except ValueError:
                    return value # Dejar que el validador del controlador maneje el error de formato
            else:
                fecha_dt = value
            
            # Cálculo de edad
            today = date.today()
            self.edad = today.year - fecha_dt.year - ((today.month, today.day) < (fecha_dt.month, fecha_dt.day))
        return value