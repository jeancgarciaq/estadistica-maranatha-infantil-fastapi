from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.database import Base

class Aula(Base):
    __tablename__ = 'aulas'

    id = Column(Integer, primary_key=True, index=True)
    auxiliar = Column(Integer)
    capitan = Column(Integer)
    colaborador = Column(Integer)
    condicion = Column(String)
    edad = Column(String)
    maestra = Column(Integer)
    ninos = Column(Integer)
    ninas = Column(Integer)
    subcapitan = Column(Integer)
    fecha = Column(Date)
    
    id_salon = Column(Integer, ForeignKey('salones.id'))
    salon = relationship("Salon", backref="aulas")