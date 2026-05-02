from sqlalchemy import Column, Integer, Date
from models.database import Base
from models.base_class import AuditMixin

class OtrasAreas(Base, AuditMixin):
    __tablename__ = 'otrasareas'

    alabanza = Column(Integer)
    protocolo = Column(Integer)
    semillitas = Column(Integer)
    sonido = Column(Integer)
    teatro = Column(Integer)
    tv = Column(Integer)
    ujier = Column(Integer)
    seguridad = Column(Integer)
    fecha = Column(Date)

    def __repr__(self):
        return f"OtrasAreas(id={self.id}, alabanza={self.alabanza}, protocolo={self.protocolo}, semillitas={self.semillitas}, sonido={self.sonido}, teatro={self.teatro}, tv={self.tv}, ujier={self.ujier}, seguridad={self.seguridad}, fecha='{self.fecha}')"
