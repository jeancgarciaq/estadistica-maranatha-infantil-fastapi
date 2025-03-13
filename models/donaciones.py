from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from models.database import Base
from models.donaciones_salones import donaciones_salones

class Donacion(Base):
    __tablename__ = 'donaciones'

    id = Column(Integer, primary_key=True, index=True)
    cantidad = Column(Integer)
    descripcion = Column(String)
    equipo = Column(String)
    fecha = Column(Date)
    sembrador = Column(String)
    salones = relationship('Salon', secondary=donaciones_salones, back_populates='donaciones')