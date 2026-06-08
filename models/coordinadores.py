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
    
    # Nuevos campos solicitados
    sexo = Column(String(20), nullable=True)  # masculino, femenino
    profesion = Column(String(100), nullable=True)
    estado_civil = Column(String(20), nullable=True)  # soltero, casado, divorciado, viudo, concubinato
    cantidad_hijos = Column(Integer, nullable=True, default=0)
    numero_equipo = Column(Integer, nullable=True)  # Equipo
    tiempo_servicio = Column(String(100), nullable=True)
    pertenece_evangelio_cambia = Column(String(5), nullable=True)  # si, no
    sirve_otra_area = Column(String(5), nullable=True)  # si, no
    otra_area_detalle = Column(String(100), nullable=True)
    bautizado = Column(String(5), nullable=True)  # si, no
    asiste_discipulado = Column(String(5), nullable=True)  # si, no
    usa_transporte = Column(String(5), nullable=True)  # si, no
    
    id_lider = Column(Integer, ForeignKey('lideres.id'), nullable=True)
    lider = relationship("Lider", backref="coordinadores")

    id_area = Column(Integer, ForeignKey('areas.id'), nullable=True)
    area = relationship("Area", back_populates="coordinadores")

    def __repr__(self):
        return f"<Coordinador(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"

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