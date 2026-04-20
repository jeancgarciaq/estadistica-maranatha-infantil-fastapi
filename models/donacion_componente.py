from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from models.base import Base

class DonacionComponente(Base):
    """
    Modelo que registra el uso de una donación como materia prima para otra donación compuesta.
    """
    __tablename__ = 'donaciones_componentes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    donacion_compuesta_id = Column(Integer, ForeignKey('donaciones.id'), nullable=False)
    donacion_materia_id = Column(Integer, ForeignKey('donaciones.id'), nullable=False)
    cantidad_usada = Column(Float, nullable=False)

    # Relaciones
    donacion_compuesta = relationship("Donacion", back_populates="componentes", foreign_keys=[donacion_compuesta_id])
    materia_prima = relationship("Donacion", back_populates="usada_en", foreign_keys=[donacion_materia_id])

    def __repr__(self):
        return f"<DonacionComponente(id={self.id}, compuesta_id={self.donacion_compuesta_id}, materia_id={self.donacion_materia_id}, cantidad={self.cantidad_usada})>"
