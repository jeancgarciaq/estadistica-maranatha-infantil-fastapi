import logging
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from controllers import BaseController
from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from models.distribucion import Distribucion
from models.donaciones import Donacion

# Configuracion de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DonacionesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Donacion, session=session)
        logger.info("Inicializando DonacionesController")
        if not session:
            logger.error("No se ha proporcionado una sesion de base de datos.")
            raise ValueError("Se requiere una sesion de base de datos para el controlador.")
        logger.info("DonacionesController inicializado con exito.")

    def crear_donacion(self, datos):
        """
        Crea una nueva donacion en la base de datos.
        :param datos: Diccionario con los datos de la donacion.
        :return: (Exito, Mensaje)
        """
        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        db = self.get_db_session()
        try:
            if 'fecha' in datos and isinstance(datos['fecha'], str):
                try:
                    datos['fecha'] = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            with db.begin():
                donacion = Donacion(**datos)
                db.add(donacion)
                db.flush()
                self.registrar_evento_sync(db, 'donaciones', donacion, 'upsert')
                logger.info("Donacion creada.")
            return True, "Donacion creada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al crear donacion")
        finally:
            db.close()

    def actualizar_donacion(self, id, datos):
        """
        Actualiza una donacion existente.
        :param id: ID de la donacion a actualizar.
        :param datos: Diccionario con los datos actualizados.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la donacion es obligatorio y debe ser un numero entero."

        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        db = self.get_db_session()
        try:
            if 'fecha' in datos and isinstance(datos['fecha'], str):
                try:
                    datos['fecha'] = datetime.strptime(datos['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."

            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == id, Donacion.is_deleted.is_(False)).first()
                if not donacion:
                    return False, "Donacion no encontrada."

                for key, value in datos.items():
                    setattr(donacion, key, value)

                self.registrar_evento_sync(db, 'donaciones', donacion, 'upsert')
                logger.info("Donacion actualizada: ID %s", id)
                return True, "Donacion actualizada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al actualizar donacion")
        finally:
            db.close()

    def eliminar_donacion(self, id):
        """
        Elimina una donacion por su ID (soft delete).
        :param id: ID de la donacion a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la donacion es obligatorio y debe ser un numero entero."

        db = self.get_db_session()
        try:
            with db.begin():
                donacion = db.query(Donacion).filter(Donacion.id == id, Donacion.is_deleted.is_(False)).first()
                if not donacion:
                    return False, "Donacion no encontrada."

                uso_en_preparados = db.query(AlimentoPreparadoComponente).filter(
                    AlimentoPreparadoComponente.donacion_materia_id == id,
                    AlimentoPreparadoComponente.is_deleted.is_(False),
                ).count()
                if uso_en_preparados > 0:
                    return (
                        False,
                        "No se puede eliminar la donacion porque esta asociada a alimentos preparados. "
                        "Elimine primero los preparados relacionados.",
                    )

                distribuciones_vinculadas = db.query(Distribucion).filter(
                    Distribucion.donacion_id == id,
                    Distribucion.is_deleted.is_(False),
                ).all()
                for distribucion in distribuciones_vinculadas:
                    self.marcar_eliminado(distribucion, db)
                    self.registrar_evento_sync(db, 'distribuciones', distribucion, 'delete')

                self.marcar_eliminado(donacion, db)
                self.registrar_evento_sync(db, 'donaciones', donacion, 'delete')
                logger.info("Donacion eliminada: ID %s", id)
                return True, "Donacion eliminada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar donacion")
        finally:
            db.close()

    def combinar_donaciones(self, datos_resultado, lista_componentes):
        """
        Registra un alimento preparado y su composicion, sin descontar inventario de donaciones.
        :param datos_resultado: Diccionario con datos del preparado.
        :param lista_componentes: Lista de diccionarios [{'id': id_materia, 'cantidad': cantidad_usada}, ...]
        :return: (Exito, Mensaje)
        """
        if not lista_componentes:
            return False, "Debe seleccionar al menos una materia prima."

        db = self.get_db_session()
        try:
            with db.begin():
                for item in lista_componentes:
                    materia = db.query(Donacion).filter(Donacion.id == item['id'], Donacion.is_deleted.is_(False)).first()
                    if not materia:
                        return False, f"ID de materia prima {item['id']} no encontrado."

                if 'fecha' in datos_resultado and isinstance(datos_resultado['fecha'], str):
                    datos_resultado['fecha'] = datetime.strptime(datos_resultado['fecha'], '%Y-%m-%d').date()

                preparado = AlimentoPreparado(**datos_resultado)
                db.add(preparado)
                db.flush()

                for item in lista_componentes:
                    componente = AlimentoPreparadoComponente(
                        alimento_preparado_id=preparado.id,
                        donacion_materia_id=item['id'],
                        cantidad_usada=item['cantidad'],
                    )
                    db.add(componente)

                logger.info("Alimento preparado ID %s registrado exitosamente.", preparado.id)
                return True, f"Preparado registrado exitosamente. ID: {preparado.id}"
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al registrar preparado")
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
        finally:
            db.close()

    def listar_preparados(self, fecha=None):
        """Lista los alimentos preparados con sus componentes, opcionalmente filtrados por fecha."""
        db = self.get_db_session()
        try:
            query = db.query(AlimentoPreparado).options(
                joinedload(AlimentoPreparado.componentes).joinedload(AlimentoPreparadoComponente.materia_prima)
            ).filter(AlimentoPreparado.is_deleted.is_(False))

            if fecha:
                if isinstance(fecha, str):
                    try:
                        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
                    except ValueError:
                        logger.warning("Fecha de filtro invalida recibida: %s", fecha)
                        return []
                query = query.filter(AlimentoPreparado.fecha == fecha)

            preparados = query.order_by(AlimentoPreparado.fecha.desc(), AlimentoPreparado.id.desc()).all()
            logger.info("%s preparados obtenidos.", len(preparados))
            return preparados
        except SQLAlchemyError as e:
            logger.error("Error al listar preparados: %s", e)
            return []
        finally:
            db.close()

    def eliminar_preparado(self, preparado_id):
        """Elimina un alimento preparado y sus componentes (soft delete)."""
        if not preparado_id or not isinstance(preparado_id, int):
            return False, "El ID del preparado es obligatorio y debe ser un numero entero."

        db = self.get_db_session()
        try:
            with db.begin():
                preparado = db.query(AlimentoPreparado).filter(
                    AlimentoPreparado.id == preparado_id,
                    AlimentoPreparado.is_deleted.is_(False),
                ).first()
                if not preparado:
                    return False, "Preparado no encontrado."
                self.marcar_eliminado(preparado, db)
            return True, "Preparado eliminado exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar preparado")
        finally:
            db.close()

    def listar_donaciones(self, fecha=None):
        """
        Obtiene la lista de donaciones desde la base de datos.
        :param fecha: Fecha en formato YYYY-MM-DD o date para filtrar resultados (opcional).
        :return: Lista de objetos Donacion.
        """
        db = self.get_db_session()
        try:
            query = db.query(Donacion).filter(Donacion.is_deleted.is_(False))

            if fecha:
                if isinstance(fecha, str):
                    try:
                        fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
                    except ValueError:
                        logger.warning("Fecha de filtro invalida recibida: %s", fecha)
                        return []
                query = query.filter(Donacion.fecha == fecha)

            donaciones = query.order_by(Donacion.id.desc()).all()
            logger.info("%s donaciones obtenidas de la base de datos.", len(donaciones))
            return donaciones
        except SQLAlchemyError as e:
            logger.error("Error al listar donaciones: %s", e)
            return []
        finally:
            db.close()

    def obtener_donacion(self, id):
        """
        Obtiene una donacion por su ID.
        :param id: ID de la donacion.
        :return: Objeto Donacion o None.
        """
        db = self.get_db_session()
        try:
            return db.query(Donacion).filter(Donacion.id == id, Donacion.is_deleted.is_(False)).first()
        except SQLAlchemyError as e:
            logger.error("Error al obtener donacion: %s", e)
            return None
        finally:
            db.close()

    def buscar_donacion(self, id=None, descripcion=None):
        """
        Busca una donacion por ID o descripcion.
        :param id: ID de la donacion a buscar.
        :param descripcion: Descripcion de la donacion a buscar.
        :return: (Exito, Objeto, Mensaje)
        """
        if not id and not descripcion:
            return False, None, "Debe proporcionar un ID o una descripcion para buscar la donacion."
        if id and not isinstance(id, int):
            return False, None, "El ID debe ser un numero entero."

        donacion = self.buscar_por_id_o_nombre(id=id, nombre=descripcion, nombre_campo="descripcion")
        if donacion:
            return True, donacion, "Donacion encontrada exitosamente."
        if id:
            return False, None, f"No existe una donacion con ID {id}."
        return False, None, "No existe una donacion con esa descripcion."

    def validar_datos(self, datos):
        """
        Valida los datos proporcionados para crear o actualizar una donacion.
        :param datos: Diccionario con los datos de la donacion.
        :return: Lista de errores encontrados.
        """
        errores = []
        cantidad = datos.get("cantidad")
        if cantidad is None or not isinstance(cantidad, (int, float)):
            errores.append("El campo 'cantidad' debe ser un numero.")
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

        unidad = datos.get("unidad", "")
        if "Unidad" in unidad and cantidad is not None:
            try:
                if not float(cantidad).is_integer():
                    errores.append("Para la medida 'Unidad(es)', la cantidad debe ser un numero entero.")
            except (ValueError, TypeError):
                pass

        return errores
