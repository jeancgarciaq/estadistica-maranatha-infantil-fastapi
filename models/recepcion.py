from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from models.base import Base, SyncMixin

class Recepcion(SyncMixin, Base):
    __tablename__ = 'recepciones'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    fecha = Column(Date)

    distribuciones = relationship("Distribucion", back_populates="recepcion")

    def __repr__(self):
        return f"Recepcion(id={self.id}, nombre='{self.nombre}', fecha='{self.fecha}')"
