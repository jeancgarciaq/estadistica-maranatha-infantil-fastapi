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
        return self.ejecutar_transaccion(operacion, "Coordinador creado exitosamente.", user_context=user_context)

    def actualizar_coordinador(self, id, datos, user_context=None):
        if not id or not isinstance(id, int):
            return False, "El ID del coordinador es obligatorio y debe ser un número entero."

        errores = self._validar_datos_coordinador(datos)
        if errores:
            return False, "\n".join(errores)

        def operacion(db):
            coordinador = self.query_activa(db).filter(Coordinador.id == id).first()
            if not coordinador: raise ValueError("Coordinador no encontrado.")
            for key, value in datos.items(): setattr(coordinador, key, value)
        return self.ejecutar_transaccion(operacion, "Coordinador actualizado.", user_context=user_context)

    def eliminar_coordinador(self, id, user_context=None):
        def operacion(db):
            coordinador = self.query_activa(db).filter(Coordinador.id == id).first()
            self.marcar_eliminado(coordinador, db)
        return self.ejecutar_transaccion(operacion, "Coordinador eliminado.", user_context=user_context)

    def _validar_datos_coordinador(self, datos):
        errores = []
        if not datos.get('nombre'):
            errores.append("El nombre del coordinador es obligatorio.")
        # Aquí podrías añadir más validaciones para id_lider, id_area, etc.
        return errores
