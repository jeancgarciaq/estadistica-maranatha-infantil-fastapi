from models.aulas import Aula
from models.salones import Salon
from sqlalchemy.exc import SQLAlchemyError
from components.styled_popup import StyledPopup
from controllers.base_controller import BaseController
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AulasController(BaseController):
    def __init__(self, vista=None, session=None):
        super().__init__(vista, Aula, session)
        self.session = session
        logger.info("Inicializando AulasController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        self.vista = vista
        logger.info("AulasController inicializado con éxito.")

    def crear_aula(self, datos):
        """
        Crea un aula con los datos proporcionados.
        :param datos: Diccionario con los datos del aula.
        """
        # Validar los datos
        errores = self.validar_datos(datos)
        if errores:
            StyledPopup.mostrar_popup("Error", "\n".join(errores), tipo="error")
            return

        db = self.get_db_session()
        aula_creada = False
        try:
            with db.begin():
                aula = Aula(**datos)
                db.add(aula)
                logger.info(f"Aula creada: {aula.id}")
                aula_creada = True
        except SQLAlchemyError as e:
            logger.error(f"Error al crear aula: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al crear aula: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            if aula_creada:
                StyledPopup.mostrar_popup("Éxito", "Aula creada exitosamente.", tipo="success")

    def actualizar_aula(self, id, datos):
        """
        Actualiza un aula existente con los datos proporcionados.
        :param id: ID del aula a actualizar.
        :param datos: Diccionario con los datos actualizados del aula.
        """
        if not id or not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID del aula es obligatorio y debe ser un número entero.", tipo="error")
            return

        errores = self.validar_datos(datos)
        if errores:
            StyledPopup.mostrar_popup("Error", "\n".join(errores), tipo="error")
            return

        db = self.get_db_session()
        aula_actualizada = False
        try:
            with db.begin():
                aula = db.query(Aula).filter(Aula.id == id).first()
                if aula:
                    for key, value in datos.items():
                        setattr(aula, key, value)
                    logger.info(f"Aula actualizada: {aula.id}")
                    aula_actualizada = True
                else:
                    StyledPopup.mostrar_popup("Error", "Aula no encontrada.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar aula: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al actualizar aula: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            if aula_actualizada:
                StyledPopup.mostrar_popup("Éxito", "Aula actualizada exitosamente.", tipo="success")

    def eliminar_aula(self, id):
        """
        Elimina un aula por su ID.
        :param id: ID del aula a eliminar.
        """
        if not id or not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID del aula es obligatorio y debe ser un número entero.", tipo="error")
            return

        db = self.get_db_session()
        aula_eliminada = False
        try:
            with db.begin():
                aula = db.query(Aula).filter(Aula.id == id).first()
                if aula:
                    db.delete(aula)
                    logger.info(f"Aula eliminada: {aula.id}")
                    aula_eliminada = True
                else:
                    StyledPopup.mostrar_popup("Error", "Aula no encontrada.", tipo="error")
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar aula: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al eliminar aula: {e}. Inténtalo de nuevo.", tipo="error")
        finally:
            db.close()
            if aula_eliminada:
                StyledPopup.mostrar_popup("Éxito", "Aula eliminada exitosamente.", tipo="success")

    def listar_aulas(self, vista):
        """
        Lista todas las aulas.
        """
        db = self.get_db_session()
        try:
            aulas = db.query(Aula).all()
            logger.info(f"{len(aulas)} aulas obtenidas de la base de datos.")
            if hasattr(vista, 'actualizar_lista_aulas'):
                vista.actualizar_lista_aulas(aulas)
            else:
                raise AttributeError("La vista no tiene un método 'actualizar_lista_aulas'.")
            return aulas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar aulas: {e}")
            StyledPopup.mostrar_popup("Error", f"Error al listar aulas: {e}. Inténtalo de nuevo.", tipo="error")
            return []
        finally:
            db.close()
            logger.info("Cierre de la sesión")
    
    def listar_aulas_button_handler(self):
        """El manejador del botón Listar en la vista aulas."""
        self.listar_aulas(self.vista)

    def buscar_aula(self, id=None, fecha=None):
        """
        Busca un aula por ID o fecha y muestra la información en un popup.
        :param id: ID del aula a buscar.
        :param fecha: Fecha del aula a buscar.
        """
        # Validar que al menos uno de los campos esté lleno
        if not id and not fecha:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o una fecha para buscar el aula.", tipo="error")
            return
        if id and not isinstance(id, int):
            StyledPopup.mostrar_popup("Error", "El ID debe ser un número entero.", tipo="error")
            return
        if fecha and not isinstance(fecha, str):
            StyledPopup.mostrar_popup("Error", "El nombre debe ser una cadena de texto.", tipo="error")
            return
        if isinstance(fecha, str):
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                StyledPopup.mostrar_popup("Error", "El campo 'fecha' debe tener el formato 'YYYY-MM-DD'.", type="error")
            
        #Buscar Aula
        aula = self.buscar_por_id_o_fecha(id=id, fecha=fecha, nombre_campo="fecha")
        if aula:
            # Mostrar la información del área en un popup
            StyledPopup.mostrar_popup(
                "Información del Aula",
                f"ID: {aula.id}\nFecha: {aula.fecha}",
                tipo="info"
            )
        else:
            # Mostrar un mensaje de error si no se encuentra el área
            if id:
                StyledPopup.mostrar_popup("Error", f"No existe un área con ID {id}.", tipo="error")
            elif fecha:
                StyledPopup.mostrar_popup("Error", f"No existe un área con fecha '{fecha}'.", tipo="error")

    def validar_datos(self, datos):
        """
        Valida los datos proporcionados para crear o actualizar un aula.
        :param datos: Diccionario con los datos del aula.
        :return: Lista de errores encontrados.
        """
        errores = []
        if not isinstance(datos.get("auxiliar"), int):
            errores.append("El campo 'auxiliar' debe ser un número entero.")
        if not isinstance(datos.get("capitan"), int):
            errores.append("El campo 'capitan' debe ser un número entero.")
        if not isinstance(datos.get("colaborador"), int):
            errores.append("El campo 'colaborador' debe ser un número entero.")
        if not isinstance(datos.get("condicion"), str):
            errores.append("El campo 'condicion' debe ser una cadena de texto.")
        if not isinstance(datos.get("edad"), str):
            errores.append("El campo 'edad' debe ser una cadena de texto.")
        if not isinstance(datos.get("maestra"), int):
            errores.append("El campo 'maestra' debe ser un número entero.")
        if not isinstance(datos.get("ninos"), int):
            errores.append("El campo 'ninos' debe ser un número entero.")
        if not isinstance(datos.get("ninas"), int):
            errores.append("El campo 'ninas' debe ser un número entero.")
        if not isinstance(datos.get("subcapitan"), int):
            errores.append("El campo 'subcapitan' debe ser un número entero.")
        if not isinstance(datos.get("fecha"), str):
            errores.append("El campo 'fecha' debe ser una cadena de texto con formato 'YYYY-MM-DD'.")
        else:
            try:
                datetime.strptime(datos["fecha"], '%Y-%m-%d')
            except ValueError:
                errores.append("El campo 'fecha' debe tener el formato 'YYYY-MM-DD'.")
        if not isinstance(datos.get("id_salon"), int):
            errores.append("El campo 'id_salon' debe ser un número entero.")
        return errores

