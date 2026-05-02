from sqlalchemy import Column, Integer, String, Date
from models.database import Base
from models.base_class import AuditMixin

class Ensenanza(Base, AuditMixin):
    __tablename__ = 'ensenanzas'

    capitan = Column(String)
    subcapitan = Column(Integer)
    fecha = Column(Date)

    def __repr__(self):
        return f"Ensenanza(id={self.id}, capitan='{self.capitan}', subcapitan={self.subcapitan}, fecha='{self.fecha}')"
