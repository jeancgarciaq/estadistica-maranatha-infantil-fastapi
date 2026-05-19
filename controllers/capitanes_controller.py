# c:\xampp\htdocs\estadistica-maranatha-infantil-fastapi\controllers\capitanes_controller.py
from models.capitanes import Capitan
from models.coordinadores import Coordinador
from controllers.base_controller import BaseController
from sqlalchemy.orm import selectinload

class CapitanesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Capitan, session=session)

    def listar_capitanes(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).options(selectinload(Capitan.coordinador).selectinload(Coordinador.area)).order_by(Capitan.nombre.asc()).all()
        finally:
            if not self.session: db.close()

    def crear_capitan(self, datos, user_context=None):
        def operacion(db):
            # El área se hereda del coordinador, no se guarda en el capitán
            datos.pop('id_area', None)
            capitan = Capitan(**datos)
            db.add(capitan)
        return self.ejecutar_transaccion(operacion, "Capitán registrado exitosamente.", user_context=user_context)

    def actualizar_capitan(self, id, datos, user_context=None):
        def operacion(db):
            capitan = self.query_activa(db).filter(Capitan.id == id).first()
            if not capitan: raise ValueError("Capitán no encontrado.")
            
            # Limpiamos datos redundantes para evitar errores de modelo
            datos.pop('id_area', None)
            datos.pop('id', None)
            for key, value in datos.items(): 
                setattr(capitan, key, value)
        return self.ejecutar_transaccion(operacion, "Capitán actualizado.", user_context=user_context)

    def eliminar_capitan(self, id, user_context=None):
        def operacion(db):
            capitan = self.query_activa(db).filter(Capitan.id == id).first()
            self.marcar_eliminado(capitan, db)
        return self.ejecutar_transaccion(operacion, "Capitán eliminado.", user_context=user_context)
