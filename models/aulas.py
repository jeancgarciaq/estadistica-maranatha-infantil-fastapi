from sqlalchemy import Column, Integer, String, ForeignKey, Date, and_
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class Aula(Base, AuditMixin):
    __tablename__ = 'aulas'

    condicion = Column(String, nullable=False)
    ninos = Column(Integer, nullable=False)
    ninas = Column(Integer, nullable=False)
    fecha = Column(Date, nullable=False)
    
    id_salon = Column(Integer, ForeignKey('salones.id'))
    salon = relationship("Salon", backref="aulas")

    # Relaciones con servidores (Jerarquización)
    id_maestra = Column(Integer, ForeignKey('docentes.id'), nullable=True)
    maestra_rel = relationship("Docente")

    id_auxiliar = Column(Integer, ForeignKey('auxiliares.id'), nullable=True)
    auxiliar_rel = relationship("Auxiliar")

    # Relación para múltiples colaboradores vinculados a esta sesión (1 o más)
    colaboradores_asistencias = relationship(
        "AsistenciaServidor",
        primaryjoin="and_(Aula.id == AsistenciaServidor.referencia_id, AsistenciaServidor.rol == 'Colaborador', AsistenciaServidor.categoria_contexto == 'aula')",
        foreign_keys="AsistenciaServidor.referencia_id",
        viewonly=True
    )

    def __repr__(self):
        return f"<Aula(id={self.id}, condicion='{self.condicion}', ninos={self.ninos}, ninas={self.ninas}, fecha='{self.fecha}', id_salon={self.id_salon}, id_maestra={self.id_maestra})>"