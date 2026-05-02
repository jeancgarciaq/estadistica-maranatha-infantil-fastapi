from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Distribucion(Base, AuditMixin):
    __tablename__ = 'distribuciones'

    donacion_id = Column(Integer, ForeignKey('donaciones.id'), nullable=True)
    alimento_preparado_id = Column(Integer, ForeignKey('alimentos_preparados.id'), nullable=True)
    salon_id = Column(Integer, ForeignKey('salones.id'), nullable=True)
    area_id = Column(Integer, ForeignKey('areas.id'), nullable=True)
    recepcion_id = Column(Integer, ForeignKey('recepciones.id'), nullable=True)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    fecha = Column(Date, nullable=False)

    # Relaciones
    donacion = relationship("Donacion", back_populates="distribuciones")
    alimento_preparado = relationship("AlimentoPreparado", back_populates="distribuciones")
    salon = relationship("Salon", back_populates="distribuciones")
    area = relationship("Area", back_populates="distribuciones")
    recepcion = relationship("Recepcion", back_populates="distribuciones")

    def __repr__(self):
        return (
            f"<Distribucion(id={self.id}, donacion_id={self.donacion_id}, alimento_preparado_id={self.alimento_preparado_id}, "
            f"salon_id={self.salon_id}, area_id={self.area_id}, recepcion_id={self.recepcion_id}, "
            f"cantidad={self.cantidad}, fecha='{self.fecha}')>"
        )