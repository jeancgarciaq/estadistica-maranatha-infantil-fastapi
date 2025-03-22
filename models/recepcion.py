from sqlalchemy import Column, Integer, String, Date
from models.base import Base

class Recepcion(Base):
    __tablename__ = 'recepciones'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    fecha = Column(Date)
