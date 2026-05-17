from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Salon(Base, AuditMixin):
    __tablename__ = 'salones'

    salon = Column(String, nullable=False, unique=True)
    edad = Column(String, nullable=False)
    
    # Vínculo jerárquico con el área (Maternal, Infantil, Pre-juvenil)
    id_area = Column(Integer, ForeignKey('areas.id'), nullable=True)
    area = relationship("Area", backref="salones")

    distribuciones = relationship("Distribucion", back_populates="salon")

    def __repr__(self):
        return f"<Salón(id={self.id}, salon='{self.salon}, edad='{self.edad}', id_area={self.id_area})>"