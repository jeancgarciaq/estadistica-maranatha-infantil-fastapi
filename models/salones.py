from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Salon(Base, AuditMixin):
    __tablename__ = 'salones'

    salon = Column(String, nullable=False, unique=True)
    edad = Column(String, nullable=False)
    
    distribuciones = relationship("Distribucion", back_populates="salon")

    def __repr__(self):
        return f"<Salón(id={self.id}, salon='{self.salon}, edad='{self.edad}')>"