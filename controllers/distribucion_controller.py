import logging
from models.donaciones import Donacion
from models.salones import Salon
from models.distribucion import Distribucion
from models.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DistribucionesController:

    def __init__(self, session):
        self.session = session

    def listar_donaciones(self):
        return self.session.query(Donacion).all()

    def obtener_salones(self):
        return self.session.query(Salon).all()

    def registrar_distribucion(self, donacion_descripcion, salones_distribucion):
        try:
            donacion = self.session.query(Donacion).filter_by(descripcion=donacion_descripcion).first()
            for salon_nombre, cantidad, unidad in salones_distribucion:
                salon = self.session.query(Salon).filter_by(nombre=salon_nombre).first()
                distribucion = Distribucion(donacion=donacion, salon=salon, cantidad=cantidad, unidad=unidad)
                self.session.add(distribucion)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def listar_distribuciones(self):
        return self.session.query(Distribucion).options(joinedload(Distribucion.donacion), joinedload(Distribucion.salon)).all()