from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from sqlalchemy.orm import relationship
from models.base import Base

class Donacion(Base):
    """
    Modelo que representa una donación en la base de datos.

    Atributos:
        id (int): Identificador único de la donación.
        descripcion (str): Descripción de la donación.
        cantidad (float): Cantidad de la donación.
        unidad (str): Unidad de medida de la donación.
        equipo (str): Equipo asociado con la donación.
        fecha (date): Fecha en la que se realizó la donación.
        es_compuesta (bool): Indica si la donación es resultado de una mezcla/composición.
    """
    __tablename__ = 'donaciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(255), nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String(50), nullable=False)
    equipo = Column(String(100))
    fecha = Column(Date, nullable=False)
    es_compuesta = Column(Boolean, default=False)

    distribuciones = relationship("Distribucion", back_populates="donacion")


    def __repr__(self):
        return f"<Donacion(id={self.id}, donacion='{self.descripcion}, cantidad={self.cantidad}, unidad={self.unidad}, equipo={self.equipo}, fecha={self.fecha}')>"