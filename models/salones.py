from sqlalchemy import Column, Integer, String
from models.database import Base

class Salon(Base):
    __tablename__ = 'salones'

    id = Column(Integer, primary_key=True, index=True)
    salon = Column(String)
    edad = Column(String)