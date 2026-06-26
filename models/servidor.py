from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, validates
from datetime import datetime, date
from models.database import Base
from models.base_class import AuditMixin

class Servidor(Base, AuditMixin):
    __tablename__ = 'servidores'

    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    cedula = Column(Integer, nullable=False, unique=True)
    celular = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=True, unique=True)
    numero_equipo = Column(Integer, nullable=True)
    sexo = Column(String(20), nullable=True)
    profesion = Column(String(100), nullable=True)
    estado_civil = Column(String(20), nullable=True)
    cantidad_hijos = Column(Integer, nullable=True, default=0)
    tiempo_servicio = Column(String(100), nullable=True)
    pertenece_evangelio_cambia = Column(String(5), nullable=True)
    sirve_otra_area = Column(String(5), nullable=True)
    otra_area_detalle = Column(String(100), nullable=True)
    bautizado = Column(String(5), nullable=True)
    asiste_discipulado = Column(String(5), nullable=True)
    usa_transporte = Column(String(5), nullable=True)

    id_capitan = Column(Integer, ForeignKey('capitanes.id'), nullable=True)
    capitan = relationship("Capitan", backref="servidores")

    @property
    def area(self):
        if self.capitan and self.capitan.coordinador:
            return self.capitan.coordinador.area
        return None

    def __repr__(self):
        return f"<Servidor(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"

    @validates('fecha_nacimiento')
    def validar_fecha_nacimiento(self, key, value):
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
