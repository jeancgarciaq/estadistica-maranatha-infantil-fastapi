from sqlalchemy import Table, Column, Integer, ForeignKey
from models.database import Base

donaciones_salones = Table(
    'donaciones_salones', Base.metadata,
    Column('donacion_id', Integer, ForeignKey('donaciones.id'), primary_key=True),
    Column('salon_id', Integer, ForeignKey('salones.id'), primary_key=True)
)