import logging
from datetime import datetime
from models.donaciones import Donacion
from models.salones import Salon
from models.distribucion import Distribucion
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from controllers import BaseController

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DistribucionesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Distribucion, session=session)
        logger.info("Inicializando DistribucionesController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        logger.info("DistribucionesController inicializado con éxito.")

    def crear_distribucion(self, datos):
        """
        Crea una nueva distribución en la base de datos.
        :param datos: Diccionario con los datos de la distribución.
        :return: (Exito, Mensaje)
        """
        if not isinstance(datos, dict):
            return False, "Los datos proporcionados no son válidos."

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
                distribucion = Distribucion(**datos)
                db.add(distribucion)
                logger.info(f"Distribución creada.")
            return True, "Distribución creada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al crear distribución")
        finally:
            db.close()

    def listar_distribuciones(self):
        """
        Lista todas las distribuciones desde la base de datos.
        :return: Lista de objetos Distribucion.
        """
        db = self.get_db_session()
        try:
            distribuciones = db.query(Distribucion).options(
                joinedload(Distribucion.donacion),
                joinedload(Distribucion.salon)
            ).all()
            logger.info(f"{len(distribuciones)} distribuciones obtenidas.")
            return distribuciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar distribuciones: {e}")
            return []
        finally:
            db.close()

    def actualizar_distribucion(self, id, datos):
        """
        Actualiza una distribución existente.
        :param id: ID de la distribución a actualizar.
        :param datos: Diccionario con los datos actualizados.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la distribución es obligatorio y debe ser un número entero."

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
                distribucion = db.query(Distribucion).filter(Distribucion.id == id).first()
                if distribucion:
                    for key, value in datos.items():
                        setattr(distribucion, key, value)
                    logger.info(f"Distribución actualizada: ID {id}")
                    return True, "Distribución actualizada exitosamente."
                else:
                    return False, "Distribución no encontrada."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al actualizar distribución")
        finally:
            db.close()

    def eliminar_distribucion(self, id):
        """
        Elimina una distribución de la base de datos.
        :param id: ID de la distribución a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la distribución es obligatorio y debe ser un número entero."

        db = self.get_db_session()
        try:
            with db.begin():
                distribucion = db.query(Distribucion).filter(Distribucion.id == id).first()
                if distribucion:
                    db.delete(distribucion)
                    logger.info(f"Distribución eliminada: ID {id}")
                    return True, "Distribución eliminada exitosamente."
                else:
                    return False, "Distribución no encontrada."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar distribución")
        finally:
            db.close()

    def obtener_distribucion(self, id):
        """
        Obtiene una distribución por su ID.
        :param id: ID de la distribución.
        :return: Objeto Distribucion o None.
        """
        db = self.get_db_session()
        try:
            return db.query(Distribucion).filter(Distribucion.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener distribución: {e}")
            return None
        finally:
            db.close()

    def buscar_distribucion(self, id=None):
        """
        Busca una distribución por ID.
        :param id: ID de la distribución a buscar.
        :return: (Exito, Objeto, Mensaje)
        """
        if not id:
            return False, None, "Debe proporcionar un ID para buscar la distribución."
        if not isinstance(id, int):
            return False, None, "El ID debe ser un número entero."

        distribucion = self.buscar_por_id_o_nombre(id=id, nombre_campo="id")
        if distribucion:
            return True, distribucion, "Distribución encontrada exitosamente."
        else:
            return False, None, f"No existe una distribución con ID {id}."

    def validar_datos(self, datos):
        """
        Valida los datos para crear o actualizar una distribución.
        :return: Lista de errores encontrados.
        """
        errores = []
        if not datos.get("donacion_id"):
            errores.append("El campo 'donacion_id' es obligatorio.")
        elif not isinstance(datos.get("donacion_id"), int):
            errores.append("El campo 'donacion_id' debe ser un número entero.")

        if not datos.get("salon_id"):
            errores.append("El campo 'salon_id' es obligatorio.")
        elif not isinstance(datos.get("salon_id"), int):
            errores.append("El campo 'salon_id' debe ser un número entero.")

        cantidad = datos.get("cantidad")
        if not cantidad:
            errores.append("El campo 'cantidad' es obligatorio.")
        elif not isinstance(cantidad, (int, float)):
            errores.append("El campo 'cantidad' debe ser un número.")
        elif cantidad <= 0:
            errores.append("El campo 'cantidad' debe ser un número positivo.")
        elif cantidad > 1000:
            errores.append("El campo 'cantidad' no puede ser mayor a 1000.")

        if not isinstance(datos.get("fecha"), str):
            errores.append("El campo 'fecha' debe ser una cadena de texto con formato 'YYYY-MM-DD'.")
        else:
            try:
                datetime.strptime(datos["fecha"], '%Y-%m-%d')
            except ValueError:
                errores.append("El campo 'fecha' debe tener el formato 'YYYY-MM-DD'.")

        return errores