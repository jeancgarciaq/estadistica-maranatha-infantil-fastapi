from models.aulas import Aula
from models.salones import Salon
from sqlalchemy.exc import SQLAlchemyError
from controllers.base_controller import BaseController
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AulasController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Aula, session=session)
        logger.info("Inicializando AulasController")
        if not session:
            logger.error("No se ha proporcionado una sesión de base de datos.")
            raise ValueError("Se requiere una sesión de base de datos para el controlador.")
        logger.info("AulasController inicializado con éxito.")

    def crear_aula(self, datos):
        """
        Crea un aula con los datos proporcionados.
        :param datos: Diccionario con los datos del aula.
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
                aula = Aula(**datos)
                db.add(aula)
                logger.info(f"Aula creada.")
            return True, "Aula creada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al crear aula")
        finally:
            db.close()

    def actualizar_aula(self, id, datos):
        """
        Actualiza un aula existente con los datos proporcionados.
        :param id: ID del aula a actualizar.
        :param datos: Diccionario con los datos actualizados del aula.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID del aula es obligatorio y debe ser un número entero."

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
                aula = db.query(Aula).filter(Aula.id == id).first()
                if aula:
                    for key, value in datos.items():
                        setattr(aula, key, value)
                    logger.info(f"Aula actualizada: ID {id}")
                    return True, "Aula actualizada exitosamente."
                else:
                    return False, "Aula no encontrada."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al actualizar aula")
        finally:
            db.close()

    def eliminar_aula(self, id):
        """
        Elimina un aula por su ID.
        :param id: ID del aula a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID del aula es obligatorio y debe ser un número entero."

        db = self.get_db_session()
        try:
            with db.begin():
                aula = db.query(Aula).filter(Aula.id == id).first()
                if aula:
                    db.delete(aula)
                    logger.info(f"Aula eliminada: ID {id}")
                    return True, "Aula eliminada exitosamente."
                else:
                    return False, "Aula no encontrada."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar aula")
        finally:
            db.close()

    def listar_aulas(self):
        """
        Lista todas las aulas.
        :return: Lista de objetos Aula.
        """
        db = self.get_db_session()
        try:
            aulas = db.query(Aula).all()
            logger.info(f"{len(aulas)} aulas obtenidas de la base de datos.")
            return aulas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar aulas: {e}")
            return []
        finally:
            db.close()

    def listar_salones(self):
        """
        Lista todos los salones disponibles.
        :return: Lista de objetos Salon.
        """
        db = self.get_db_session()
        try:
            salones = db.query(Salon).all()
            logger.info(f"{len(salones)} salones obtenidos para AulasController.")
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar salones en AulasController: {e}")
            return []
        finally:
            db.close()

    def buscar_aula(self, id=None, fecha=None):
        """
        Busca un aula por ID o fecha.
        :param id: ID del aula a buscar.
        :param fecha: Fecha del aula a buscar.
        :return: (Exito, Objeto, Mensaje)
        """
        if not id and not fecha:
            return False, None, "Debe proporcionar un ID o una fecha para buscar el aula."
        if id and not isinstance(id, int):
            return False, None, "El ID debe ser un número entero."
        if fecha and not isinstance(fecha, str):
            return False, None, "La fecha debe ser una cadena de texto."
        if isinstance(fecha, str):
            try:
                datetime.strptime(fecha, "%Y-%m-%d")
            except ValueError:
                return False, None, "El campo 'fecha' debe tener el formato 'YYYY-MM-DD'."

        aula = self.buscar_por_id_o_fecha(id=id, fecha=fecha, nombre_campo="fecha")
        if aula:
            return True, aula, "Aula encontrada exitosamente."
        else:
            if id:
                return False, None, f"No existe un aula con ID {id}."
            elif fecha:
                return False, None, f"No existe un aula con fecha '{fecha}'."
            return False, None, "Aula no encontrada."

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
