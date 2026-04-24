from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Logistica(Base):
    __tablename__ = 'logisticas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    almacen = Column(String(100), nullable=False)
    capitan = Column(String(100), nullable=False)
    distribucion = Column(String(255), nullable=True)
    hidratacion = Column(String(255), nullable=True)
    pasillo = Column(String(255), nullable=True)
    secretaria = Column(String(255), nullable=True)
    fecha = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Logistica(id={self.id}, capitan='{self.capitan}', fecha='{self.fecha}')>"