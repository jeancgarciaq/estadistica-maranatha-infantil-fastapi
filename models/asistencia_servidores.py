from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base
from models.base_class import AuditMixin

class AsistenciaServidor(Base, AuditMixin):
    """
    Tabla pivote centralizada para registrar la asistencia individual de servidores
    en cualquier área o contexto del sistema.
    """
    __tablename__ = 'asistencia_servidores'

    id_servidor = Column(Integer, ForeignKey('servidores.id'), nullable=False)
    fecha = Column(Date, nullable=False, index=True)
    
    # Rol desempeñado en esa fecha específica (ej: 'Maestra', 'Auxiliar', 'Logística')
    rol = Column(String(50), nullable=False)
    
    # Define el contexto (ej: 'aula', 'logistica', 'otras_areas')
    categoria_contexto = Column(String(50), nullable=False, index=True)
    
    # ID del registro en la tabla correspondiente (ej: id de la tabla 'aulas')
    referencia_id = Column(Integer, nullable=True)

    servidor = relationship("Servidor", backref="asistencias")

    def __repr__(self):
        return f"<AsistenciaServidor(id={self.id}, servidor='{self.id_servidor}', fecha='{self.fecha}', rol='{self.rol}')>"