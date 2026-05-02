from models.aulas import Aula
from models.salones import Salon
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from controllers.base_controller import BaseController
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AulasController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Aula, session=session)
        logger.info("AulasController inicializado.")

    def crear_aula(self, datos, user_context=None):
        """
        Crea un aula con los datos proporcionados.
        :param datos: Diccionario con los datos del aula.
        :return: (Exito, Mensaje)
        """
        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        fecha = self.validar_y_convertir_fecha(datos.get('fecha'))
        if not fecha:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        datos['fecha'] = fecha

        def operacion(db):
            aula = Aula(**datos)
            db.add(aula)
            db.flush()
            self.registrar_evento_sync(db, 'aulas', aula, 'upsert')
            logger.info("Aula creada.")

        return self.ejecutar_transaccion(operacion, "Aula creada exitosamente.", user_context=user_context)

    def actualizar_aula(self, id, datos, user_context=None):
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

        fecha = self.validar_y_convertir_fecha(datos.get('fecha'))
        if not fecha:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        datos['fecha'] = fecha

        def operacion(db):
            aula = db.query(Aula).filter(Aula.id == id, Aula.is_deleted.is_(False)).first()
            if not aula:
                raise ValueError("Aula no encontrada.")
            
            for key, value in datos.items():
                setattr(aula, key, value)
            
            self.registrar_evento_sync(db, 'aulas', aula, 'upsert')
            logger.info(f"Aula actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Aula actualizada exitosamente.", user_context=user_context)

    def eliminar_aula(self, id, user_context=None):
        """
        Elimina un aula por su ID.
        :param id: ID del aula a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID del aula es obligatorio y debe ser un número entero."

        def operacion(db):
            aula = db.query(Aula).filter(Aula.id == id, Aula.is_deleted.is_(False)).first()
            if not aula:
                raise ValueError("Aula no encontrada.")
            
            self.marcar_eliminado(aula, db)
            self.registrar_evento_sync(db, 'aulas', aula, 'delete')
            logger.info(f"Aula eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Aula eliminada exitosamente.", user_context=user_context)

    def listar_aulas(self):
        """
        Lista todas las aulas.
        :return: Lista de objetos Aula.
        """
        return self.listar_aulas_por_fecha()

    def listar_aulas_por_fecha(self, fecha=None):
        """
        Lista las aulas filtrando por fecha cuando se proporciona.
        :param fecha: Fecha en formato YYYY-MM-DD o datetime.date.
        :return: Lista de objetos Aula.
        """
        db = self.get_db_session()
        try:
            query = self.query_activa(db).options(selectinload(Aula.salon))
            if fecha:
                fecha_dt = self.validar_y_convertir_fecha(fecha)
                if fecha_dt:
                    query = query.filter(Aula.fecha == fecha_dt)

            aulas = query.all()
            logger.info(f"{len(aulas)} aulas obtenidas de la base de datos.")
            return aulas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar aulas: {e}")
            return []
        except ValueError as e:
            logger.error(f"Formato de fecha inválido al listar aulas: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def listar_salones(self):
        """
        Lista todos los salones disponibles.
        :return: Lista de objetos Salon.
        """
        db = self.get_db_session()
        try:
            salones = db.query(Salon).filter(Salon.is_deleted.is_(False)).all()
            logger.info(f"{len(salones)} salones obtenidos para AulasController.")
            return salones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar salones en AulasController: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_aula(self, id):
        """
        Obtiene un aula por su ID.
        :param id: ID del aula.
        :return: Objeto Aula o None.
        """
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Aula.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener aula: {e}")
            return None
        finally:
            if not self.session:
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
