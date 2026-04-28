from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from models.base import Base, SyncMixin


class AlimentoPreparadoComponente(SyncMixin, Base):
    __tablename__ = 'alimentos_preparados_componentes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    alimento_preparado_id = Column(Integer, ForeignKey('alimentos_preparados.id'), nullable=False)
    donacion_materia_id = Column(Integer, ForeignKey('donaciones.id'), nullable=False)
    cantidad_usada = Column(Float, nullable=False)

    alimento_preparado = relationship('AlimentoPreparado', back_populates='componentes')
    materia_prima = relationship('Donacion')

    def __repr__(self):
        return (
            f"<AlimentoPreparadoComponente(id={self.id}, preparado_id={self.alimento_preparado_id}, "
            f"donacion_materia_id={self.donacion_materia_id}, cantidad_usada={self.cantidad_usada})>"
        )
