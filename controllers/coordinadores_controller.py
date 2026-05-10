# c:\xampp\htdocs\estadistica-maranatha-infantil-fastapi\controllers\coordinadores_controller.py
from models.coordinadores import Coordinador
from controllers.base_controller import BaseController

class CoordinadoresController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Coordinador, session=session)

    def listar_coordinadores(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).order_by(Coordinador.nombre.asc()).all()
        finally:
            if not self.session: db.close()

    def crear_coordinador(self, datos, user_context=None):
        def operacion(db):
            coordinador = Coordinador(**datos)
            db.add(coordinador)
            db.flush()
            self.registrar_evento_sync(db, 'coordinadores', coordinador, 'upsert')
        return self.ejecutar_transaccion(operacion, "Líder creado exitosamente.", user_context=user_context)

    def actualizar_coordinador(self, id, datos, user_context=None):
        def operacion(db):
            coordinador = self.query_activa(db).filter(Coordinador.id == id).first()
            if not coordinador: raise ValueError("Líder no encontrado.")
            for key, value in datos.items(): setattr(coordinador, key, value)
            self.registrar_evento_sync(db, 'coordinadores', coordinador, 'upsert')
        return self.ejecutar_transaccion(operacion, "Líder actualizado.", user_context=user_context)

    def eliminar_coordinador(self, id, user_context=None):
        def operacion(db):
            coordinador = self.query_activa(db).filter(Coordinador.id == id).first()
            self.marcar_eliminado(coordinador, db)
            self.registrar_evento_sync(db, 'coordinadores', coordinador, 'delete')
        return self.ejecutar_transaccion(operacion, "Coordinador eliminado.", user_context=user_context)
