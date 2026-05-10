# c:\xampp\htdocs\estadistica-maranatha-infantil-fastapi\controllers\capitanes_controller.py
from models.capitanes import Capitan
from controllers.base_controller import BaseController

class CapitanesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Capitan, session=session)

    def listar_capitanes(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).order_by(Capitan.nombre.asc()).all()
        finally:
            if not self.session: db.close()

    def crear_capitan(self, datos, user_context=None):
        def operacion(db):
            capitan = Capitan(**datos)
            db.add(capitan)
            db.flush()
            self.registrar_evento_sync(db, 'capitanes', capitan, 'upsert')
        return self.ejecutar_transaccion(operacion, "Capitán creado exitosamente.", user_context=user_context)

    def actualizar_capitan(self, id, datos, user_context=None):
        def operacion(db):
            capitan = self.query_activa(db).filter(Capitan.id == id).first()
            if not capitan: raise ValueError("Capitán no encontrado.")
            for key, value in datos.items(): setattr(capitan, key, value)
            self.registrar_evento_sync(db, 'capitanes', capitan, 'upsert')
        return self.ejecutar_transaccion(operacion, "Capitán actualizado.", user_context=user_context)

    def eliminar_capitan(self, id, user_context=None):
        def operacion(db):
            capitan = self.query_activa(db).filter(Capitan.id == id).first()
            self.marcar_eliminado(capitan, db)
            self.registrar_evento_sync(db, 'capitanes', capitan, 'delete')
        return self.ejecutar_transaccion(operacion, "Capitán eliminado.", user_context=user_context)
