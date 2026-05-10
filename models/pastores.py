from sqlalchemy import Column, Integer, String
from models.database import Base
from models.base_class import AuditMixin

class Pastor(Base, AuditMixin):
    """
    Modelo que representa un pastor, autoridad máxima de los líderes.
    """
    __tablename__ = 'pastores'

    nombre = Column(String(100), nullable=False)
    iglesia = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Pastor(id={self.id}, nombre='{self.nombre}', iglesia='{self.iglesia}')>"