from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Aula(Base, AuditMixin):
    __tablename__ = 'aulas'

    auxiliar = Column(Integer, nullable=False)
    capitan = Column(Integer, nullable=False)
    colaborador = Column(Integer, nullable=False)
    condicion = Column(String, nullable=False)
    maestra = Column(Integer, nullable=False)
    ninos = Column(Integer, nullable=False)
    ninas = Column(Integer, nullable=False)
    subcapitan = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    
    id_salon = Column(Integer, ForeignKey('salones.id'))
    salon = relationship("Salon", backref="aulas")

    def __repr__(self):
        return f"<Aula(id={self.id}, auxiliar={self.auxiliar}, capitan={self.capitan}, colaborador={self.colaborador}, condicion='{self.condicion}', maestra={self.maestra}, ninos={self.ninos}, ninas={self.ninas}, subcapitan={self.subcapitan}, fecha='{self.fecha}', id_salon={self.id_salon})>"