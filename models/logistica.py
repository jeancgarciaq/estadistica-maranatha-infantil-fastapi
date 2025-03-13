from sqlalchemy import Column, Integer, Date
from models.database import Base

class Logistica(Base):
    __tablename__ = 'logisticas'

    id = Column(Integer, primary_key=True, index=True)
    almacen = Column(Integer)
    capitan = Column(Integer)
    distribucion = Column(Integer)
    fecha = Column(Date)
    hidratacion = Column(Integer)
    pasillo = Column(Integer)
    secretaria = Column(Integer)