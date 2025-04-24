import logging
from models.donaciones import Donacion
from models.salones import Salon
from models.distribucion import Distribucion
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from controllers import BaseController
from components.styled_popup import StyledPopup

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DistribucionesController(BaseController):
    def __init__(self, vista=None, session=None):
        """
        Constructor del controlador de distribuciones.
        :param vista: Vista asociada al controlador.
        :param session: Sesión de base de datos.
        """
        super().__init__(vista, Distribucion, session)
        self.session = session
        logger.info("Inicializando DistribucionesController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        self.vista = vista
        logger.info("DistribucionesController inicializado con éxito.")

    def crear_distribucion(self, datos):
        """
        Crea una nueva distribución en la base de datos.
        :param datos: Diccionario con los datos de la distribución.
        """
        # Validar que los datos sean un diccionario
        if not isinstance(datos, dict):
            StyledPopup.mostrar_popup("Error", "Los datos proporcionados no son válidos.", tipo="error")
            return

        # Validar los datos
        try:
            errores = self.validar_datos(datos)
        except Exception as e:
            logger.error(f"Error inesperado durante la validación de datos: {e}")
            StyledPopup.mostrar_popup("Error", "Ocurrió un error inesperado durante la validación de los datos.", tipo="error")
            return

        # Manejar errores de validación
        if errores:
            logger.warning(f"Errores de validación encontrados: {errores}")
            StyledPopup.mostrar_popup("Error", "\n".join(errores), tipo="error")
            return

        # Crear la distribución en la base de datos
        db = self.get_db_session()
        distribucion_creada = False
        try:
            with db.begin():
                distribucion = Distribucion(**datos)
                db.add(distribucion)
                logger.info(f"Distribución creada: {distribucion.id}")
                distribucion_creada = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear distribución: {e}")
            StyledPopup.mostrar_popup("Error", "Error al crear distribución. Inténtalo de nuevo.", tipo="error")
        finally:
            if db:
                db.close()
            if distribucion_creada:
                StyledPopup.mostrar_popup("Éxito", "Distribución creada exitosamente.", tipo="exito")
                logger.info("Conexión a la base de datos cerrada.")

    def listar_distribuciones(self):
        """
        Lista todas las distribuciones desde la base de datos.
        """
        db = self.get_db_session()
        try:
            distribuciones = db.query(Distribucion).options(
                joinedload(Distribucion.donacion),
                joinedload(Distribucion.salon)
            ).all()
            logger.info(f"{len(distribuciones)} distribuciones obtenidas de la base de datos.")
            if hasattr(self.vista, 'actualizar_lista_distribuciones'):
                self.vista.actualizar_lista_distribuciones(distribuciones)
            else:
                raise AttributeError("La vista no tiene el método 'actualizar_lista_distribuciones'.")
            return distribuciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar distribuciones: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al listar distribuciones: {e}. Inténtalo de nuevo.", tipo="error")
            return []
        finally:
            if db:
                db.close()
                logger.info("Conexión a la base de datos cerrada.")

    def actualizar_distribucion(self, id, datos):
        """
        Actualiza una distribución existente en la base de datos.
        :param id: ID de la distribución a actualizar.
        :param datos: Diccionario con los datos actualizados.
        """
        if not id or not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID de la distribución es obligatorio y debe ser un número entero.", tipo="error")
            return

        errores = self.validar_datos(datos)
        if errores:
            StyledPopup.mostrar_popup("Error", "\n".join(errores), tipo="error")
            return

        db = self.get_db_session()
        distribucion_actualizada = False
        try:
            with db.begin():
                distribucion = db.query(Distribucion).filter(Distribucion.id == id).first()
                if distribucion:
                    for key, value in datos.items():
                        setattr(distribucion, key, value)
                    logger.info(f"Distribución actualizada: {distribucion.id}")
                    distribucion_actualizada = True
                else:
                    StyledPopup.mostrar_popup("Error", "Distribución no encontrada.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar distribución: {e}")
            StyledPopup.mostrar_popup("Error", "Error al actualizar distribución. Inténtalo de nuevo.", tipo="error")
        finally:
            if db:
                db.close()
            if distribucion_actualizada:
                StyledPopup.mostrar_popup("Éxito", "Distribución actualizada exitosamente.", tipo="success")
                logger.info("Conexión a la base de datos cerrada.")

    def eliminar_distribucion(self, id):
        """
        Elimina una distribución de la base de datos.
        :param id: ID de la distribución a eliminar.
        """
        if not id or not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID de la distribución es obligatorio y debe ser un número entero.", tipo="error")
            return

        db = self.get_db_session()
        distribucion_eliminada = False
        try:
            with db.begin():
                distribucion = db.query(Distribucion).filter(Distribucion.id == id).first()
                if distribucion:
                    db.delete(distribucion)
                    distribucion_eliminada = True
                    logger.info(f"Distribución eliminada: {id}")
                else:
                    StyledPopup.mostrar_popup("Error", "Distribución no encontrada.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar distribución: {e}")
            StyledPopup.mostrar_popup("Error", "Error al eliminar distribución. Inténtalo de nuevo.", tipo="error")
        finally:
            if db:
                db.close()
            if distribucion_eliminada:
                StyledPopup.mostrar_popup("Éxito", "Distribución eliminada exitosamente.", tipo="success")
                logger.info("Conexión a la base de datos cerrada.")

    def validar_datos(self, datos):
        """
        Valida los datos proporcionados para crear o actualizar una distribución.
        :param datos: Diccionario con los datos de la distribución.
        :return: Lista de errores encontrados.
        """
        errores = []

        # Validar que los campos obligatorios no estén vacíos
        if not datos.get("donacion_id"):
            errores.append("El campo 'donacion_id' es obligatorio.")
        if not datos.get("salon_id"):
            errores.append("El campo 'salon_id' es obligatorio.")
        if not datos.get("cantidad"):
            errores.append("El campo 'cantidad' es obligatorio.")

        # Validar tipos de datos
        if not isinstance(datos.get("donacion_id"), int):
            errores.append("El campo 'donacion_id' debe ser un número entero.")
        if not isinstance(datos.get("salon_id"), int):
            errores.append("El campo 'salon_id' debe ser un número entero.")
        if not isinstance(datos.get("cantidad"), (int, float)):
            errores.append("El campo 'cantidad' debe ser un número.")

        # Validar que los valores sean positivos
        if datos.get("cantidad") <= 0:
            errores.append("El campo 'cantidad' debe ser un número positivo.")

        # Validar que los IDs existan en la base de datos
        db = self.get_db_session()
        if not db.query(Donacion).filter(Donacion.id == datos.get("donacion_id")).first():
            errores.append(f"No existe una donación con ID {datos.get('donacion_id')}.")
        if not db.query(Salon).filter(Salon.id == datos.get("salon_id")).first():
            errores.append(f"No existe un salón con ID {datos.get('salon_id')}.")

        # Validar duplicados
        if db.query(Distribucion).filter(
            Distribucion.donacion_id == datos.get("donacion_id"),
            Distribucion.salon_id == datos.get("salon_id")
        ).first():
            errores.append("Ya existe una distribución con la misma donación y salón.")

        # Validar límites máximos
        if datos.get("cantidad") > 1000:
            errores.append("El campo 'cantidad' no puede ser mayor a 1000.")

        return errores
    
    def buscar_distribucion(self, id=None, nombre=None):
        """
        Busca una distribución por ID o por nombre.
        :param id: ID de la distribución a buscar.
        :param nombre: Nombre de la distribución a buscar.
        :return: La distribución encontrada o None si no se encuentra.
        """
        # Validar que al menos uno de los campos esté lleno
        if not id and not nombre:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o un nombre para buscar la distribución.", tipo="error")
            return None

        # Validar que el ID sea un número entero si se proporciona
        if id and not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID debe ser un número entero.", tipo="error")
            return None

        try:
            # Usar el método buscar_por_id_o_nombre para buscar la distribución
            distribucion = self.buscar_por_id_o_nombre(id=id, nombre=nombre, nombre_campo="nombre")
            if distribucion:
                # Mostrar la información de la distribución en un popup
                StyledPopup.mostrar_popup(
                    "Información de la Distribución",
                    f"ID: {distribucion.id}\nDonación ID: {distribucion.donacion_id}\nSalón ID: {distribucion.salon_id}\nCantidad: {distribucion.cantidad}",
                    tipo="info"
                )
                return distribucion
            else:
                # Mostrar un mensaje de error si no se encuentra la distribución
                StyledPopup.mostrar_popup("Error", "No se encontró ninguna distribución con los criterios proporcionados.", tipo="error")
                return None
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar distribución: {e}")
            StyledPopup.mostrar_popup("Error", "Error al buscar distribución. Inténtalo de nuevo.", tipo="error")
            return None