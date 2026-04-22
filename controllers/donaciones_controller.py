import logging
from models.donaciones import Donacion
from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from models.distribucion import Distribucion
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
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
                if not donacion:
                    return False, "Donación no encontrada."

                # No permitir eliminar si la donación es materia prima de algún preparado.
                uso_en_preparados = db.query(AlimentoPreparadoComponente).filter(
                    AlimentoPreparadoComponente.donacion_materia_id == id
                ).count()
                if uso_en_preparados > 0:
                    return (
                        False,
                        "No se puede eliminar la donación porque está asociada a alimentos preparados. "
                        "Elimine primero los preparados relacionados."
                    )

                # Limpiar distribuciones ligadas para evitar violación de check de origen exclusivo.
                distribuciones_vinculadas = db.query(Distribucion).filter(Distribucion.donacion_id == id).all()
                for distribucion in distribuciones_vinculadas:
                    db.delete(distribucion)

                db.delete(donacion)
                logger.info(f"Donación eliminada: ID {id}")
                return True, "Donación eliminada exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar donación")
        finally:
            db.close()

    def combinar_donaciones(self, datos_resultado, lista_componentes):
        """
        Registra un alimento preparado y su composición, sin descontar inventario de donaciones.
        :param datos_resultado: Diccionario con datos del preparado (descripcion, cantidad, unidad, fecha, equipo).
        :param lista_componentes: Lista de diccionarios [{'id': id_materia, 'cantidad': cantidad_usada}, ...]
        :return: (Exito, Mensaje)
        """
        if not lista_componentes:
            return False, "Debe seleccionar al menos una materia prima."

        db = self.get_db_session()
        try:
            with db.begin():
                # 1. Validar que todas las materias primas existan
                for item in lista_componentes:
                    materia = db.query(Donacion).filter(Donacion.id == item['id']).first()
                    if not materia:
                        return False, f"ID de materia prima {item['id']} no encontrado."

                # 2. Crear el alimento preparado
                if 'fecha' in datos_resultado and isinstance(datos_resultado['fecha'], str):
                    datos_resultado['fecha'] = datetime.strptime(datos_resultado['fecha'], '%Y-%m-%d').date()

                preparado = AlimentoPreparado(**datos_resultado)
                db.add(preparado)
                db.flush()

                # 3. Registrar componentes utilizados sin alterar cantidades de donación
                for item in lista_componentes:
                    componente = AlimentoPreparadoComponente(
                        alimento_preparado_id=preparado.id,
                        donacion_materia_id=item['id'],
                        cantidad_usada=item['cantidad']
                    )
                    db.add(componente)

                logger.info(f"Alimento preparado ID {preparado.id} registrado exitosamente.")
                return True, f"Preparado registrado exitosamente. ID: {preparado.id}"
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al registrar preparado")
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
        finally:
            db.close()

    def listar_preparados(self):
        """
        Lista los alimentos preparados con sus componentes.
        """
        db = self.get_db_session()
        try:
            return db.query(AlimentoPreparado).options(
                joinedload(AlimentoPreparado.componentes).joinedload(AlimentoPreparadoComponente.materia_prima)
            ).order_by(AlimentoPreparado.fecha.desc(), AlimentoPreparado.id.desc()).all()
        except SQLAlchemyError as e:
            logger.error(f"Error al listar preparados: {e}")
            return []
        finally:
            db.close()

    def eliminar_preparado(self, preparado_id):
        """
        Elimina un alimento preparado y sus componentes.
        """
        if not preparado_id or not isinstance(preparado_id, int):
            return False, "El ID del preparado es obligatorio y debe ser un número entero."

        db = self.get_db_session()
        try:
            with db.begin():
                preparado = db.query(AlimentoPreparado).filter(AlimentoPreparado.id == preparado_id).first()
                if not preparado:
                    return False, "Preparado no encontrado."
                db.delete(preparado)
            return True, "Preparado eliminado exitosamente."
        except SQLAlchemyError as e:
            return self.manejar_excepcion(e, "Error al eliminar preparado")
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
            
        # Validación: Si la medida es "Unidad(es)", la cantidad debe ser entera.
        unidad = datos.get("unidad", "")
        if "Unidad" in unidad and cantidad is not None:
            try:
                if not float(cantidad).is_integer():
                    errores.append("Para la medida 'Unidad(es)', la cantidad debe ser un número entero.")
            except (ValueError, TypeError):
                pass
                
        return errores