import logging
from models.donaciones import Donacion
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from kivy.lang import Builder
from components.styled_popup import StyledPopup
from controllers import BaseController

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DonacionesController(BaseController):
    def __init__(self, vista=None, session=None):
        super().__init__(vista, Donacion, session)
        self.session = session
        logger.info("Inicializando DonacionesController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        self.vista = vista
        logger.info("DonacionesController inicializado con éxito.")

    def crear_donacion(self, datos):
        """Crea una nueva donación en la base de datos."""
        # Validar los datos
        errores = self.validar_datos(datos)
        if errores:
            StyledPopup.mostrar_popup("Error", "\n".join(errores), tipo="error")
            return

        db = self.get_db_session()
        donacion_creada = False
        try:
            with db.begin():
                donacion = Donacion(**datos)
                db.add(donacion)
                logger.info(f"Donación creada: {donacion.id}")
                donacion_creada = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear donación: {e}")
            StyledPopup.mostrar_popup("Error", "Error al crear donación. Inténtalo de nuevo.", tipo="error")
        finally:
            if db:
                db.close()
            if donacion_creada:
                StyledPopup.mostrar_popup("Éxito", "Donación creada exitosamente.", tipo="exito")
                logger.info("Conexión a la base de datos cerrada.")

    def actualizar_donacion(self, id, datos):
        # Validar los datos
        if not id or not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID de la donación es obligatorio y debe ser un número entero.", tipo="error")
            return

        errores = self.validar_datos(datos)
        if errores:
            StyledPopup.mostrar_popup("Error", "\n".join(errores), tipo="error")
            return
            
        db = self.get_db_session()
        donacion_actualizada = False
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == id).first()
                if donacion:
                    for key, value in datos.items():
                        setattr(donacion, key, value)
                    logger.info(f"Donación actualizada: {donacion.id}")
                    aula_actualizada = True
                else:
                    StyledPopup.mostrar_popup("Error", "Aula no encontrada.", tipo="error")
        except ValueError:
            self.vista.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar donación: {e}")
            self.vista.mostrar_error("Error al actualizar donación. Inténtalo de nuevo.")
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")
            if donacion_actualizada:
                self.vista.mostrar_exito("Donación actualizada exitosamente.")

    def eliminar_donacion(self, id):
        # Validación de datos
        if not id or not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID de la donación es obligatorio y debe ser un número entero.", tipo="error")
            return

        db = self.get_db_session()
        donacion_eliminada = False
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == id).first()
                if donacion:
                    db.delete(donacion)
                    donacion_eliminada = True
                    logger.info(f"Donación eliminada: {id}")
                else:
                    StyledPopup.mostrar_popup("Error", "Donación no encontrada.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar donación: {e}")
            StyledPopup.mostrar_popup("Error", "Error al eliminar donación. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")
            if donacion_eliminada:
                StyledPopup.mostrar_popup("Éxito", "Donación eliminada exitosamente.", tipo="exito")

    def listar_donaciones(self, vista):
        """Obtiene la lista de donaciones desde la base de datos."""
        db = self.get_db_session()
        try:
            donaciones = db.query(Donacion).all()
            logger.info(f"{len(donaciones)} donaciones obtenidas de la base de datos.")
            if hasattr(vista, 'actualizar_lista_donaciones'):
                vista.actualizar_lista_donaciones(donaciones)
            else:
                raise AttributeError("La vista no tiene el método 'actualizar_lista_donaciones'.")
            return donaciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar donaciones: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al listar donaciones: {e}. Inténtalo de nuevo.", tipo="error")
            return []
        finally:
            if db:
                db.close()
                logger.info("Conexión a la base de datos cerrada.")
    
    def listar_donaciones_button_handler(self):
        """Método para manejar el evento de listar donaciones."""
        self.listar_donaciones(self.vista)
    
    #Buscar Donación
    def buscar_donacion(self, id=None, descripcion=None):
        # Validar que al menos uno de los campos esté lleno
        if not id:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o una descripción para buscar la donación.", tipo="error")
            return
        if id and not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID debe ser un número entero.", tipo="error")
            return
        

        donacion = self.buscar_por_id_o_nombre(id=id, nombre=descripcion, nombre_campo="descripcion")
        if donacion:
            # Mostrar la información de la donación en un popup
            StyledPopup.mostrar_popup(
                "Información de la Donacion",
                f"ID: {donacion.id}\nDescripción: {donacion.descripcion}\nFecha: {donacion.fecha}",
                tipo="info"
            )
        else:
            # Mostrar un mensaje de error si no se encuentra la donación
            if id:
                StyledPopup.mostrar_popup("Error", f"No existe una donación con ID {id}.", tipo="error")
    
    def validar_datos(self, datos):
        """
        Valida los datos proporcionados para crear o actualizar un aula.
        :param datos: Diccionario con los datos del aula.
        :return: Lista de errores encontrados.
        """
        errores = []
        if not isinstance(datos.get("cantidad"), float):
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
            errores.append("El campo 'equipo' debe ser un número entero.")
        return errores