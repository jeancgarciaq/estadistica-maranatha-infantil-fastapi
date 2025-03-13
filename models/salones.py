from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.database import Base
from models.donaciones_salones import donaciones_salones

class Salon(Base):
    __tablename__ = 'salones'

    id = Column(Integer, primary_key=True, index=True)
    salon = Column(String)
    edad = Column(String)
    donaciones = relationship('Donacion', secondary=donaciones_salones, back_populates='salones')