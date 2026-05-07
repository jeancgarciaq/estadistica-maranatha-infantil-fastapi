import logging
from datetime import datetime
from models.servidor import Servidor
from sqlalchemy.exc import SQLAlchemyError
from controllers import BaseController

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ServidorController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Servidor, session=session)
        logger.info("ServidorController inicializado.")

    def crear_servidor(self, datos, user_context=None):
        """
        Crea un nuevo registro de servidor en la base de datos.
        :param datos: Diccionario con los datos del servidor.
        :return: (Exito, Mensaje)
        """
        if not isinstance(datos, dict):
            return False, "Los datos proporcionados no son válidos."

        datos_normalizados = self._normalizar_datos(datos)

        def operacion(db):
            errores = self.validar_datos(datos_normalizados, db, is_new=True)
            if errores:
                raise ValueError("\n".join(errores))

            servidor = Servidor(**datos_normalizados)
            db.add(servidor)
            db.flush()
            self.registrar_evento_sync(db, 'servidores', servidor, 'upsert')
            logger.info("Servidor creado.")

        return self.ejecutar_transaccion(operacion, "Servidor creado exitosamente.", user_context=user_context)

    def listar_servidores(self):
        """
        Lista todos los registros de servidores desde la base de datos.
        :return: Lista de objetos Servidor.
        """
        db = self.get_db_session()
        try:
            servidores = self.query_activa(db).order_by(Servidor.nombre.asc()).all()
            logger.info(f"{len(servidores)} servidores obtenidos.")
            return servidores
        except SQLAlchemyError as e:
            logger.error(f"Error al listar servidores: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_servidor(self, id):
        """
        Obtiene un registro de servidor por su ID.
        :param id: ID del servidor.
        :return: Objeto Servidor o None.
        """
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Servidor.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener servidor: {e}")
            return None
        finally:
            if not self.session:
                db.close()

    def actualizar_servidor(self, id, datos, user_context=None):
        """
        Actualiza un registro de servidor existente.
        :param id: ID del servidor a actualizar.
        :param datos: Diccionario con los datos actualizados.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID del servidor es obligatorio y debe ser un número entero."

        datos_normalizados = self._normalizar_datos(datos)

        def operacion(db):
            servidor = db.query(Servidor).filter(Servidor.id == id, Servidor.is_deleted.is_(False)).first()
            if not servidor:
                raise ValueError("Servidor no encontrado.")

            # Combinar datos existentes con los nuevos para la validación
            datos_para_validar = {k: getattr(servidor, k) for k in servidor.__table__.columns.keys()}
            datos_para_validar.update(datos_normalizados)

            errores = self.validar_datos(datos_para_validar, db, is_new=False, current_id=id)
            if errores:
                raise ValueError("\n".join(errores))

            for key, value in datos_normalizados.items():
                setattr(servidor, key, value)
            
            self.registrar_evento_sync(db, 'servidores', servidor, 'upsert')
            logger.info(f"Servidor actualizado: ID {id}")

        return self.ejecutar_transaccion(operacion, "Servidor actualizado exitosamente.", user_context=user_context)

    def eliminar_servidor(self, id, user_context=None):
        """
        Elimina un registro de servidor por su ID.
        :param id: ID del servidor a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID del servidor es obligatorio y debe ser un número entero."

        def operacion(db):
            servidor = db.query(Servidor).filter(Servidor.id == id, Servidor.is_deleted.is_(False)).first()
            if not servidor:
                raise ValueError("Servidor no encontrado.")
            
            self.marcar_eliminado(servidor, db)
            self.registrar_evento_sync(db, 'servidores', servidor, 'delete')
            logger.info(f"Servidor eliminado: ID {id}")

        return self.ejecutar_transaccion(operacion, "Servidor eliminado exitosamente.", user_context=user_context)

    def _normalizar_datos(self, datos):
        """
        Normaliza los datos de entrada para facilitar validaciones.
        """
        datos_normalizados = dict(datos)
        for campo in ["nombre", "celular", "correo", "area_servicio", "capitan"]:
            if campo in datos_normalizados and isinstance(datos_normalizados[campo], str):
                datos_normalizados[campo] = datos_normalizados[campo].strip()
                if datos_normalizados[campo] == "":
                    datos_normalizados[campo] = None
        
        # Convertir campos numéricos que puedan venir como string vacío a None
        for campo in ["edad", "cedula", "numero_equipo"]:
            if campo in datos_normalizados and datos_normalizados[campo] == "":
                datos_normalizados[campo] = None

        return datos_normalizados

    def validar_datos(self, datos, db, is_new=True, current_id=None):
        """
        Valida los datos proporcionados para crear o actualizar un servidor.
        :param datos: Diccionario con los datos del servidor.
        :param db: Sesión de la base de datos.
        :param is_new: Booleano que indica si es una creación (True) o actualización (False).
        :param current_id: ID del servidor actual si es una actualización.
        :return: Lista de errores encontrados.
        """
        errores = []

        nombre = datos.get("nombre")
        if not nombre or not isinstance(nombre, str) or not nombre.strip():
            errores.append("El campo 'nombre' es obligatorio y debe ser una cadena de texto.")
        elif len(nombre) > 100:
            errores.append("El campo 'nombre' no puede superar los 100 caracteres.")

        edad = datos.get("edad")
        if edad is None:
            errores.append("El campo 'edad' es obligatorio.")
        elif not isinstance(edad, int) or edad <= 0:
            errores.append("El campo 'edad' debe ser un número entero positivo.")

        cedula = datos.get("cedula")
        if cedula is None:
            errores.append("El campo 'cedula' es obligatorio.")
        elif not isinstance(cedula, int) or cedula <= 0:
            errores.append("El campo 'cedula' debe ser un número entero positivo.")
        else:
            query = db.query(Servidor).filter(Servidor.cedula == cedula, Servidor.is_deleted.is_(False))
            if not is_new and current_id:
                query = query.filter(Servidor.id != current_id)
            if query.first():
                errores.append(f"Ya existe un servidor con la cédula {cedula}.")

        celular = datos.get("celular")
        if celular and (not isinstance(celular, str) or len(celular) > 20):
            errores.append("El campo 'celular' debe ser una cadena de texto de hasta 20 caracteres.")

        correo = datos.get("correo")
        if correo:
            if not isinstance(correo, str) or len(correo) > 100 or "@" not in correo:
                errores.append("El campo 'correo' debe ser una dirección de correo electrónico válida de hasta 100 caracteres.")
            else:
                query = db.query(Servidor).filter(Servidor.correo == correo, Servidor.is_deleted.is_(False))
                if not is_new and current_id:
                    query = query.filter(Servidor.id != current_id)
                if query.first():
                    errores.append(f"Ya existe un servidor con el correo electrónico {correo}.")

        numero_equipo = datos.get("numero_equipo")
        if numero_equipo is not None and (not isinstance(numero_equipo, int) or numero_equipo <= 0):
            errores.append("El campo 'numero de equipo' debe ser un número entero positivo.")

        area_servicio = datos.get("area_servicio")
        if area_servicio and (not isinstance(area_servicio, str) or len(area_servicio) > 100):
            errores.append("El campo 'area de servicio' debe ser una cadena de texto de hasta 100 caracteres.")

        capitan = datos.get("capitan")
        if capitan and (not isinstance(capitan, str) or len(capitan) > 100):
            errores.append("El campo 'capitan' debe ser una cadena de texto de hasta 100 caracteres.")

        return errores