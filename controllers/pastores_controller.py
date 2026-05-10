from models.pastores import Pastor
from controllers.base_controller import BaseController

class PastoresController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Pastor, session=session)

    def listar_pastores(self):
        db = self.get_db_session()
        try:
            return self.query_activa(db).order_by(Pastor.nombre.asc()).all()
        finally:
            if not self.session: db.close()

    def crear_pastor(self, datos, user_context=None):
        if not datos.get('nombre') or not datos.get('iglesia'):
            return False, "Nombre e Iglesia son obligatorios."
            
        def operacion(db):
            pastor = Pastor(nombre=datos['nombre'], iglesia=datos['iglesia'])
            db.add(pastor)
            db.flush()
            self.registrar_evento_sync(db, 'pastores', pastor, 'upsert')
        return self.ejecutar_transaccion(operacion, "Pastor registrado exitosamente.", user_context=user_context)

    def actualizar_pastor(self, id, datos, user_context=None):
        def operacion(db):
            pastor = self.query_activa(db).filter(Pastor.id == id).first()
            if not pastor: raise ValueError("Pastor no encontrado.")
            pastor.nombre = datos.get('nombre', pastor.nombre)
            pastor.iglesia = datos.get('iglesia', pastor.iglesia)
            self.registrar_evento_sync(db, 'pastores', pastor, 'upsert')
        return self.ejecutar_transaccion(operacion, "Datos del pastor actualizados.", user_context=user_context)

    def eliminar_pastor(self, id, user_context=None):
        def operacion(db):
            pastor = self.query_activa(db).filter(Pastor.id == id).first()
            if not pastor: raise ValueError("Pastor no encontrado.")
            self.marcar_eliminado(pastor, db)
            self.registrar_evento_sync(db, 'pastores', pastor, 'delete')
        return self.ejecutar_transaccion(operacion, "Pastor eliminado del sistema.", user_context=user_context)