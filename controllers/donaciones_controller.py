import logging
from models.donaciones import Donacion
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from controllers import BaseController

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DonacionesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Donacion, session=session)
        logger.info("Inicializando DonacionesController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        logger.info("DonacionesController inicializado con éxito.")

    def crear_donacion(self, datos):
        """
        Crea una nueva donación en la base de datos.
        :param datos: Diccionario con los datos de la donación.
        :return: (Exito, Mensaje)
        """
        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        db = self.get_db_session()
        try:
            # Convertir fecha de string a objeto date
            if 'fecha' in datos and isinstance(datos['fecha'], str):
                try:
                    datos['fecha'] = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            with db.begin():
                donacion = Donacion(**datos)
                db.add(donacion)
                logger.info(f"Donación creada.")
            return True, "Donación creada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al crear donación")
        finally:
            db.close()

    def actualizar_donacion(self, id, datos):
        """
        Actualiza una donación existente.
        :param id: ID de la donación a actualizar.
        :param datos: Diccionario con los datos actualizados.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la donación es obligatorio y debe ser un número entero."

        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        db = self.get_db_session()
        try:
            # Convertir fecha de string a objeto date
            if 'fecha' in datos and isinstance(datos['fecha'], str):
                try:
                    datos['fecha'] = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == id).first()
                if donacion:
                    for key, value in datos.items():
                        setattr(donacion, key, value)
                    logger.info(f"Donación actualizada: ID {id}")
                    return True, "Donación actualizada exitosamente."
                else:
                    return False, "Donación no encontrada."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al actualizar donación")
        finally:
            db.close()

    def eliminar_donacion(self, id):
        """
        Elimina una donación por su ID.
        :param id: ID de la donación a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la donación es obligatorio y debe ser un número entero."

        db = self.get_db_session()
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == id).first()
                if donacion:
                    db.delete(donacion)
                    logger.info(f"Donación eliminada: ID {id}")
                    return True, "Donación eliminada exitosamente."
                else:
                    return False, "Donación no encontrada."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar donación")
        finally:
            db.close()

    def listar_donaciones(self):
        """
        Obtiene la lista de donaciones desde la base de datos.
        :return: Lista de objetos Donacion.
        """
        db = self.get_db_session()
        try:
            donaciones = db.query(Donacion).all()
            logger.info(f"{len(donaciones)} donaciones obtenidas de la base de datos.")
            return donaciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar donaciones: {e}")
            return []
        finally:
            db.close()

    def obtener_donacion(self, id):
        """
        Obtiene una donación por su ID.
        :param id: ID de la donación.
        :return: Objeto Donacion o None.
        """
        db = self.get_db_session()
        try:
            return db.query(Donacion).filter(Donacion.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener donación: {e}")
            return None
        finally:
            db.close()

    def buscar_donacion(self, id=None, descripcion=None):
        """
        Busca una donación por ID o descripción.
        :param id: ID de la donación a buscar.
        :param descripcion: Descripción de la donación a buscar.
        :return: (Exito, Objeto, Mensaje)
        """
        if not id and not descripcion:
            return False, None, "Debe proporcionar un ID o una descripción para buscar la donación."
        if id and not isinstance(id, int):
            return False, None, "El ID debe ser un número entero."

        donacion = self.buscar_por_id_o_nombre(id=id, nombre=descripcion, nombre_campo="descripcion")
        if donacion:
            return True, donacion, "Donación encontrada exitosamente."
        else:
            if id:
                return False, None, f"No existe una donación con ID {id}."
            return False, None, f"No existe una donación con esa descripción."

    def validar_datos(self, datos):
        """
        Valida los datos proporcionados para crear o actualizar una donación.
        :param datos: Diccionario con los datos de la donación.
        :return: Lista de errores encontrados.
        """
        errores = []
        cantidad = datos.get("cantidad")
        if cantidad is None or not isinstance(cantidad, (int, float)):
            errores.append("El campo 'cantidad' debe ser un número.")
        if not isinstance(datos.get("descripcion"), str):
            errores.append("El campo 'descripcion' debe ser una cadena de texto.")
        if not isinstance(datos.get("unidad"), str):
            errores.append("El campo 'unidad' debe ser una cadena de texto.")
        if not isinstance(datos.get("fecha"), str):
            errores.append("El campo 'fecha' debe ser una cadena de texto con formato 'YYYY-MM-DD'.")
        else:
            try:
                datetime.strptime(datos["fecha"], '%Y-%m-%d')
            except ValueError:
                errores.append("El campo 'fecha' debe tener el formato 'YYYY-MM-DD'.")
        if not isinstance(datos.get("equipo"), str):
            errores.append("El campo 'equipo' debe ser una cadena de texto.")
        return errores