from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Area(Base, AuditMixin):
    """
    Modelo que representa un área en la base de datos.
    """
    __tablename__ = 'areas'

    area = Column(String(100), nullable=False, unique=True)  # Longitud máxima de 100 caracteres

    distribuciones = relationship("Distribucion", back_populates="area")

    def __repr__(self):
        return f"<Area(id={self.id}, area='{self.area}')>"
