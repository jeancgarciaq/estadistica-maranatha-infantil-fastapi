from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Salon(Base):
    __tablename__ = 'salones'

    id = Column(Integer, primary_key=True, index=True)
    salon = Column(String, nullable=False, unique=True)
    edad = Column(String, nullable=False)
    
    distribuciones = relationship("Distribucion", back_populates="salon")

    def __repr__(self):
        return f"<Salón(id={self.id}, salon='{self.salon}, edad='{self.edad}')>"