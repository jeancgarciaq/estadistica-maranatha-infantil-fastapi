from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class Area(Base):
    """
    Modelo que representa un área en la base de datos.

    Atributos:
        id (int): Identificador único del área.
        area (str): Nombre del área.
    """
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True, index=True)
    area = Column(String(100), nullable=False, unique=True)  # Longitud máxima de 100 caracteres

    # Relación con otras tablas (si aplica)
    # salones = relationship("Salon", back_populates="area")

    def __repr__(self):
        return f"<Area(id={self.id}, area='{self.area}')>"
