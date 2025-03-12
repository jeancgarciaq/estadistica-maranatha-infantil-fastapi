from sqlalchemy import Column, Integer, String, Date
from models.database import Base

class Ensenanza(Base):
    __tablename__ = 'ensenanzas'

    id = Column(Integer, primary_key=True, index=True)
    capitan = Column(String)
    fecha = Column(Date)
    subcapitan = Column(Integer)