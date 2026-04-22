import logging
from datetime import datetime
from models.donaciones import Donacion
from models.alimento_preparado import AlimentoPreparado
from models.salones import Salon
from models.areas import Area
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

        db = self.get_db_session()
        try:
            datos_normalizados = self._normalizar_datos(datos)
            errores = self.validar_datos(datos_normalizados, db)
            if errores:
                return False, "\n".join(errores)

            # Convertir fecha de string a objeto date
            if 'fecha' in datos_normalizados and isinstance(datos_normalizados['fecha'], str):
                try:
                    datos_normalizados['fecha'] = datetime.strptime(datos_normalizados['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            distribucion = Distribucion(**datos_normalizados)
            db.add(distribucion)
            db.commit()
            logger.info("Distribución creada.")
            return True, "Distribución creada exitosamente."
        except SQLAlchemyError as e:
            db.rollback()
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
                joinedload(Distribucion.alimento_preparado),
                joinedload(Distribucion.salon),
                joinedload(Distribucion.area)
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

        db = self.get_db_session()
        try:
            datos_normalizados = self._normalizar_datos(datos)
            distribucion = db.query(Distribucion).filter(Distribucion.id == id).first()
            if not distribucion:
                return False, "Distribución no encontrada."

            datos_validar = {
                "donacion_id": datos_normalizados.get("donacion_id", distribucion.donacion_id),
                "alimento_preparado_id": datos_normalizados.get("alimento_preparado_id", distribucion.alimento_preparado_id),
                "salon_id": datos_normalizados.get("salon_id", distribucion.salon_id),
                "area_id": datos_normalizados.get("area_id", distribucion.area_id),
                "cantidad": datos_normalizados.get("cantidad", distribucion.cantidad),
                "unidad": datos_normalizados.get("unidad", distribucion.unidad),
                "fecha": datos_normalizados.get("fecha", distribucion.fecha),
            }

            errores = self.validar_datos(datos_validar, db)
            if errores:
                return False, "\n".join(errores)

            # Convertir fecha de string a objeto date
            if 'fecha' in datos_normalizados and isinstance(datos_normalizados['fecha'], str):
                try:
                    datos_normalizados['fecha'] = datetime.strptime(datos_normalizados['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            for key, value in datos_normalizados.items():
                setattr(distribucion, key, value)
            db.commit()
            logger.info(f"Distribución actualizada: ID {id}")
            return True, "Distribución actualizada exitosamente."
        except SQLAlchemyError as e:
            db.rollback()
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
            distribucion = db.query(Distribucion).filter(Distribucion.id == id).first()
            if distribucion:
                db.delete(distribucion)
                db.commit()
                logger.info(f"Distribución eliminada: ID {id}")
                return True, "Distribución eliminada exitosamente."
            else:
                return False, "Distribución no encontrada."
        except SQLAlchemyError as e:
            db.rollback()
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
            return db.query(Distribucion).options(
                joinedload(Distribucion.donacion),
                joinedload(Distribucion.alimento_preparado),
                joinedload(Distribucion.salon),
                joinedload(Distribucion.area)
            ).filter(Distribucion.id == id).first()
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

    def _normalizar_datos(self, datos):
        """
        Normaliza los datos de entrada para facilitar validaciones.
        """
        datos_normalizados = dict(datos)

        for campo in ("donacion_id", "alimento_preparado_id", "salon_id", "area_id", "unidad"):
            if campo in datos_normalizados and isinstance(datos_normalizados[campo], str):
                datos_normalizados[campo] = datos_normalizados[campo].strip()

        if datos_normalizados.get("donacion_id") in ("", "None", "none"):
            datos_normalizados["donacion_id"] = None
        if datos_normalizados.get("alimento_preparado_id") in ("", "None", "none"):
            datos_normalizados["alimento_preparado_id"] = None
        if datos_normalizados.get("salon_id") == "":
            datos_normalizados["salon_id"] = None
        if datos_normalizados.get("area_id") == "":
            datos_normalizados["area_id"] = None

        return datos_normalizados

    def validar_datos(self, datos, db):
        """
        Valida los datos para crear o actualizar una distribución.
        :return: Lista de errores encontrados.
        """
        errores = []
        donacion_id = datos.get("donacion_id")
        alimento_preparado_id = datos.get("alimento_preparado_id")
        salon_id = datos.get("salon_id")
        area_id = datos.get("area_id")
        unidad = datos.get("unidad")

        if bool(donacion_id) == bool(alimento_preparado_id):
            errores.append("Debe seleccionar exactamente un origen: donación o alimento preparado.")
        else:
            if donacion_id:
                if not isinstance(donacion_id, int):
                    errores.append("El campo 'donacion_id' debe ser un número entero.")
                elif db.query(Donacion).filter(Donacion.id == donacion_id).first() is None:
                    errores.append(f"No existe una donación con ID {donacion_id}.")
            if alimento_preparado_id:
                if not isinstance(alimento_preparado_id, int):
                    errores.append("El campo 'alimento_preparado_id' debe ser un número entero.")
                elif db.query(AlimentoPreparado).filter(AlimentoPreparado.id == alimento_preparado_id).first() is None:
                    errores.append(f"No existe un alimento preparado con ID {alimento_preparado_id}.")

        if salon_id and not isinstance(salon_id, int):
            errores.append("El campo 'salon_id' debe ser un número entero.")
        if area_id and not isinstance(area_id, int):
            errores.append("El campo 'area_id' debe ser un número entero.")

        if bool(salon_id) == bool(area_id):
            errores.append("Debe seleccionar exactamente un destino: salón o área.")
        elif salon_id and db.query(Salon).filter(Salon.id == salon_id).first() is None:
            errores.append(f"No existe un salón con ID {salon_id}.")
        elif area_id and db.query(Area).filter(Area.id == area_id).first() is None:
            errores.append(f"No existe un área con ID {area_id}.")

        cantidad = datos.get("cantidad")
        if cantidad is None:
            errores.append("El campo 'cantidad' es obligatorio.")
        elif not isinstance(cantidad, (int, float)):
            errores.append("El campo 'cantidad' debe ser un número.")
        elif cantidad <= 0:
            errores.append("El campo 'cantidad' debe ser un número positivo.")
        elif cantidad > 1000:
            errores.append("El campo 'cantidad' no puede ser mayor a 1000.")

        if not isinstance(unidad, str) or not unidad.strip():
            errores.append("El campo 'unidad' es obligatorio y debe ser texto.")
        elif len(unidad.strip()) > 50:
            errores.append("El campo 'unidad' no puede superar 50 caracteres.")

        fecha = datos.get("fecha")
        if isinstance(fecha, str):
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                errores.append("El campo 'fecha' debe tener el formato 'YYYY-MM-DD'.")
        elif fecha is None or not hasattr(fecha, "year"):
            errores.append("El campo 'fecha' es obligatorio y debe tener formato 'YYYY-MM-DD'.")

        return errores