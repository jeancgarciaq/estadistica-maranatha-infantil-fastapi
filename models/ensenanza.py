from sqlalchemy import Column, Integer, String, Date
from models.base import Base, SyncMixin

class Ensenanza(SyncMixin, Base):
    __tablename__ = 'ensenanzas'

    id = Column(Integer, primary_key=True, index=True)
    capitan = Column(String)
    subcapitan = Column(Integer)
    fecha = Column(Date)

    def __repr__(self):
        return f"Ensenanza(id={self.id}, capitan='{self.capitan}', subcapitan={self.subcapitan}, fecha='{self.fecha}')"
