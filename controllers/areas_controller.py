from models.areas import Area
from models.database import get_db
from sqlalchemy.orm import Session

class ControladorArea:
    def __init__(self, vista):
        self.vista = vista

    def crear_area(self, nombre):
        db: Session = next(get_db())
        area = Area(nombre=nombre)
        db.add(area)
        db.commit()
        db.refresh(area) # Actualiza el objeto area con los datos de la base de datos
        self.listar_areas()

    def actualizar_area(self, id, nombre):
        db: Session = next(get_db())
        area = db.query(Area).filter(Area.id == id).first()
        if area:
            area.nombre = nombre
            db.commit()
            self.listar_areas()

    def eliminar_area(self, id):
        db: Session = next(get_db())
        area = db.query(Area).filter(Area.id == id).first()
        if area:
            db.delete(area)
            db.commit()
            self.listar_areas()

    def listar_areas(self):
        db: Session = next(get_db())
        areas = db.query(Area).all()
        self.vista.actualizar_lista_areas(areas)

    def obtener_area(self, id):
        db: Session = next(get_db())
        area = db.query(Area).filter(Area.id == id).first()
        return area