from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class Distribucion(Base):
    __tablename__ = 'distribuciones'

    id = Column(Integer, primary_key=True)
    donacion_id = Column(Integer, ForeignKey('donaciones.id'))
    salon_id = Column(Integer, ForeignKey('salones.id'))
    cantidad = Column(Float)
    unidad = Column(String)

    donaciones = relationship("Donacion", back_populates="distribuciones")
    salones = relationship("Salon", back_populates="distribuciones")