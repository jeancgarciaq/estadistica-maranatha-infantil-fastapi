from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from models.database import Base

class Donacion(Base):
    __tablename__ = 'donaciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    cantidad = Column(Float)
    unidad = Column(String)
    fecha = Column(Date)
    equipo = Column(String)
    salones = relationship("Salon", secondary="donaciones_salones", back_populates="donaciones")