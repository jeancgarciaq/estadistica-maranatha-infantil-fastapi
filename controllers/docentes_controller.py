from controllers.base_controller import BaseController
from models.docentes import Docente
from models.capitanes import Capitan
from models.coordinadores import Coordinador
from sqlalchemy.orm import selectinload

class DocentesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Docente, session=session)

    def listar_docentes(self):
        db = self.session if self.session else self.get_db_session()
        try:
            query = self.query_activa(db).options(selectinload(Docente.capitan).selectinload(Capitan.coordinador).selectinload(Coordinador.area))
            return query.all()
        finally:
            if not self.session:
                db.close()

    def crear_docente(self, datos, user_context=None):
        def operacion(db):
            # Eliminamos id_area si viene del formulario; el docente hereda el área vía Capitán -> Coordinador
            datos.pop('id_area', None)
            nuevo = Docente(**datos)
            db.add(nuevo)
            return nuevo
        return self.ejecutar_transaccion(operacion, "Docente registrado exitosamente", user_context)

    def actualizar_docente(self, id, datos, user_context=None):
        def operacion(db):
            docente = self.query_activa(db).filter(Docente.id == id).first()
            if not docente: raise ValueError("Docente no encontrado.")
            datos.pop('id_area', None)
            for key, value in datos.items(): setattr(docente, key, value)
        return self.ejecutar_transaccion(operacion, "Docente actualizado.", user_context)

    def eliminar_docente(self, id, user_context=None):
        def operacion(db):
            docente = self.query_activa(db).filter(Docente.id == id).first()
            if not docente: raise ValueError("Docente no encontrado.")
            self.marcar_eliminado(docente, db)
        return self.ejecutar_transaccion(operacion, "Docente eliminado.", user_context)
