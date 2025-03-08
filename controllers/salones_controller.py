from models.salon import Salon
from models.database import get_db
from sqlalchemy.orm import Session

class ControladorSalon:
    def __init__(self, vista):
        self.vista = vista

    def crear_salon(self, salon, edad):
        db: Session = next(get_db())
        nuevo_salon = Salon(salon=salon, edad=edad)
        db.add(nuevo_salon)
        db.commit()
        db.refresh(nuevo_salon)
        self.listar_salones()

    def actualizar_salon(self, id, salon, edad):
        db: Session = next(get_db())
        salon_actualizar = db.query(Salon).filter(Salon.id == id).first()
        if salon_actualizar:
            salon_actualizar.salon = salon
            salon_actualizar.edad = edad
            db.commit()
            self.listar_salones()

    def eliminar_salon(self, id):
        db: Session = next(get_db())
        salon_eliminar = db.query(Salon).filter(Salon.id == id).first()
        if salon_eliminar:
            db.delete(salon_eliminar)
            db.commit()
            self.listar_salones()

    def listar_salones(self):
        db: Session = next(get_db())
        salones = db.query(Salon).all()
        self.vista.actualizar_lista_salones(salones)

    def obtener_salon(self, id):
        db: Session = next(get_db())
        return db.query(Salon).filter(Salon.id == id).first()