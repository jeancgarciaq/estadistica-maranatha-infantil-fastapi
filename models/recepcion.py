from sqlalchemy import Column, Integer, String, Date
from models.base import Base

class Recepcion(Base):
    __tablename__ = 'recepciones'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    fecha = Column(Date)

    def __repr__(self):
        return f"Recepcion(id={self.id}, nombre='{self.nombre}', fecha='{self.fecha}')"
