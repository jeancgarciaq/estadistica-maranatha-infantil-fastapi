# c:\xampp\htdocs\estadistica-maranatha-infantil-fastapi\controllers\lideres_controller.py
from models.lideres import Lider
from controllers.base_controller import BaseController

class LideresController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Lider, session=session)

    def listar_lideres(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).order_by(Lider.nombre.asc()).all()
        finally:
            if not self.session: db.close()

    def crear_lider(self, datos, user_context=None):
        def operacion(db):
            lider = Lider(**datos)
            db.add(lider)
            db.flush()
            self.registrar_evento_sync(db, 'lideres', lider, 'upsert')
        return self.ejecutar_transaccion(operacion, "Líder creado exitosamente.", user_context=user_context)

    def actualizar_lider(self, id, datos, user_context=None):
        def operacion(db):
            lider = self.query_activa(db).filter(Lider.id == id).first()
            if not lider: raise ValueError("Líder no encontrado.")
            for key, value in datos.items(): setattr(lider, key, value)
            self.registrar_evento_sync(db, 'lideres', lider, 'upsert')
        return self.ejecutar_transaccion(operacion, "Líder actualizado.", user_context=user_context)

    def eliminar_lider(self, id, user_context=None):
        def operacion(db):
            lider = self.query_activa(db).filter(Lider.id == id).first()
            self.marcar_eliminado(lider, db)
            self.registrar_evento_sync(db, 'lideres', lider, 'delete')
        return self.ejecutar_transaccion(operacion, "Líder eliminado.", user_context=user_context)
