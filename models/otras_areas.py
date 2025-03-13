from sqlalchemy import Column, Integer, Date
from models.database import Base

class OtrasAreas(Base):
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