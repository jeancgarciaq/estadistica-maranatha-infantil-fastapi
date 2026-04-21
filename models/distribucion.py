from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.base import Base

class Distribucion(Base):
    __tablename__ = 'distribuciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    donacion_id = Column(Integer, ForeignKey('donaciones.id'), nullable=False)
    salon_id = Column(Integer, ForeignKey('salones.id'), nullable=True)
    area_id = Column(Integer, ForeignKey('areas.id'), nullable=True)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    fecha = Column(Date, nullable=False)

    # Relaciones
    donacion = relationship("Donacion", back_populates="distribuciones")
    salon = relationship("Salon", back_populates="distribuciones")
    area = relationship("Area", back_populates="distribuciones")

    def __repr__(self):
        return (
            f"<Distribucion(id={self.id}, donacion_id={self.donacion_id}, "
            f"salon_id={self.salon_id}, area_id={self.area_id}, "
            f"cantidad={self.cantidad}, fecha='{self.fecha}')>"
        )