from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from models.base import Base


class AlimentoPreparado(Base):
    __tablename__ = 'alimentos_preparados'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    equipo = Column(String(100), nullable=False)
    fecha = Column(Date, nullable=False)

    componentes = relationship(
        'AlimentoPreparadoComponente',
        back_populates='alimento_preparado',
        cascade='all, delete-orphan'
    )
    distribuciones = relationship('Distribucion', back_populates='alimento_preparado')

    def __repr__(self):
        return (
            f"<AlimentoPreparado(id={self.id}, descripcion='{self.descripcion}', "
            f"cantidad={self.cantidad}, unidad='{self.unidad}', equipo='{self.equipo}', fecha='{self.fecha}')>"
        )
