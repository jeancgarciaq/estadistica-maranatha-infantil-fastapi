from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.modelo_base_datos import Base
from models.donacion_salon import donaciones_salones

class Salon(Base):
    __tablename__ = 'salones'

    id = Column(Integer, primary_key=True, index=True)
    salon = Column(String)
    edad = Column(String)
    donaciones = relationship('Donacion', secondary=donaciones_salones, back_populates='salones')