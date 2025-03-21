from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Salon(Base):
    __tablename__ = 'salones'

    id = Column(Integer, primary_key=True, index=True)
    salon = Column(String)
    edad = Column(String)
    
    distribuciones = relationship("Distribucion", back_populates="salon")