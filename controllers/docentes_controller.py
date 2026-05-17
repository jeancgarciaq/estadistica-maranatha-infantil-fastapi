from controllers.base_controller import BaseController
from models.docentes import Docente

class DocentesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Docente, session=session)

    def listar_docentes(self):
        db = self.session if self.session else self.get_db_session()
        try:
            query = self.query_activa(db)
            return query.all()
        finally:
            if not self.session:
                db.close()

    def crear_docente(self, datos, user_context=None):
        def operacion(db):
            nuevo = Docente(**datos)
            db.add(nuevo)
            return nuevo
        return self.ejecutar_transaccion(operacion, "Docente registrado exitosamente", user_context)