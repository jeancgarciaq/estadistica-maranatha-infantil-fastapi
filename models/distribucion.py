from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Distribucion(Base):
    __tablename__ = 'distribuciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    donacion_id = Column(Integer, ForeignKey('donaciones.id'), nullable=False)
    salon_id = Column(Integer, ForeignKey('salones.id'), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    fecha = Column(Date, nullable=False)

    # Relaciones
    donacion = relationship("Donacion", back_populates="distribuciones")
    salon = relationship("Salon", back_populates="distribuciones")

    def __repr__(self):
        return f"<Distribucion(id={self.id}, donacion_id={self.donacion_id}, salon_id={self.salon_id}, cantidad={self.cantidad}, fecha='{self.fecha}')>"