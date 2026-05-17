from controllers.base_controller import BaseController
from models.auxiliares import Auxiliar

class AuxiliaresController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Auxiliar, session=session)

    def listar_auxiliares(self):
        db = self.session if self.session else self.get_db_session()
        try:
            query = self.query_activa(db)
            return query.all()
        finally:
            if not self.session:
                db.close()

    def crear_auxiliar(self, datos, user_context=None):
        def operacion(db):
            nuevo = Auxiliar(**datos)
            db.add(nuevo)
            return nuevo
        return self.ejecutar_transaccion(operacion, "Auxiliar registrado exitosamente", user_context)
