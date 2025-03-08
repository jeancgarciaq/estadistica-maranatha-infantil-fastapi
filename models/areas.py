from sqlalchemy import Column, Integer, String
from models.database import Base

class Area(Base):
    __tablename__ = 'areas'

    id = Column(Integer, primary_key=True, index=True)
    area = Column(String)