from sqlalchemy import Column, Integer, String
from models.database import Base

class Recepcion(Base):
    __tablename__ = 'recepciones'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)