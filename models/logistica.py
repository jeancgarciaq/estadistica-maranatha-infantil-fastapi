from sqlalchemy import Column, Integer, Date
from models.base import Base

class Logistica(Base):
    __tablename__ = 'logisticas'

    id = Column(Integer, primary_key=True, index=True)
    almacen = Column(Integer)
    capitan = Column(Integer)
    distribucion = Column(Integer)
    hidratacion = Column(Integer)
    pasillo = Column(Integer)
    secretaria = Column(Integer)
    fecha = Column(Date)
