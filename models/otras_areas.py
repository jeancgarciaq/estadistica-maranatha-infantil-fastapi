from sqlalchemy import Column, Integer, Date
from models.base import Base, SyncMixin

class OtrasAreas(SyncMixin, Base):
    __tablename__ = 'otrasareas'

    id = Column(Integer, primary_key=True, index=True)
    alabanza = Column(Integer)
    fecha = Column(Date)
    protocolo = Column(Integer)
    semillitas = Column(Integer)
    sonido = Column(Integer)
    teatro = Column(Integer)
    tv = Column(Integer)
    ujier = Column(Integer)
    seguridad = Column(Integer)

    def __repr__(self):
        return f"OtrasAreas(id={self.id}, alabanza={self.alabanza}, protocolo={self.protocolo}, semillitas={self.semillitas}, sonido={self.sonido}, teatro={self.teatro}, tv={self.tv}, ujier={self.ujier}, seguridad={self.seguridad}, fecha='{self.fecha}')"
