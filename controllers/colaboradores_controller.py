from controllers.base_controller import BaseController
from models.colaboradores import Colaborador

class ColaboradoresController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Colaborador, session=session)

    def listar_colaboradores(self):
        db = self.session if self.session else self.get_db_session()
        try:
            query = self.query_activa(db)
            return query.all()
        finally:
            if not self.session:
                db.close()

    def crear_colaborador(self, datos, user_context=None):
        def operacion(db):
            nuevo = Colaborador(**datos)
            db.add(nuevo)
            return nuevo
        return self.ejecutar_transaccion(operacion, "Colaborador registrado exitosamente", user_context)
