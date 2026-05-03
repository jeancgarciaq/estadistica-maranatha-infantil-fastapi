import logging
from datetime import datetime
from controllers.base_controller import BaseController
from models.donaciones import Donacion
from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from sqlalchemy.exc import SQLAlchemyError

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DonacionesController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Donacion, session=session)
        logger.info("DonacionesController inicializado.")

    def crear_donacion(self, datos: dict, user_context=None):
        # Validaciones basadas en donaciones_screen.py
        if not datos.get('descripcion'):
            return False, "La descripción es obligatoria."
        if not datos.get('cantidad'):
            return False, "La cantidad es obligatoria."
        if not datos.get('unidad'):
            return False, "La unidad es obligatoria."
        if not datos.get('equipo'):
            return False, "El equipo es obligatorio."
        if not datos.get('fecha'):
            return False, "La fecha es obligatoria."

        try:
            float_cantidad = float(datos['cantidad'])
            if "Unidad" in datos['unidad'] and not float_cantidad.is_integer():
                return False, "Para la medida 'Unidad(es)', la cantidad debe ser un número entero."
            fecha_obj = self.validar_y_convertir_fecha(datos['fecha'])
            if not fecha_obj:
                return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except ValueError:
            return False, "La cantidad debe ser un número válido."

        def operacion(db):
            donacion = Donacion(
                descripcion=datos['descripcion'],
                cantidad=float_cantidad,
                unidad=datos['unidad'],
                equipo=datos['equipo'],
                fecha=fecha_obj
            )
            db.add(donacion)
            db.flush()
            self.registrar_evento_sync(db, 'donaciones', donacion, 'upsert')
            logger.info(f"Donación creada: {donacion.descripcion}")

        return self.ejecutar_transaccion(operacion, "Donación creada exitosamente.", user_context=user_context)

    def actualizar_donacion(self, id: int, datos: dict, user_context=None):
        if not id:
            return False, "El ID de la donación es obligatorio."
        if not datos.get('descripcion'):
            return False, "La descripción es obligatoria."
        if not datos.get('cantidad'):
            return False, "La cantidad es obligatoria."
        if not datos.get('unidad'):
            return False, "La unidad es obligatoria."
        if not datos.get('equipo'):
            return False, "El equipo es obligatorio."
        if not datos.get('fecha'):
            return False, "La fecha es obligatoria."

        try:
            float_cantidad = float(datos['cantidad'])
            if "Unidad" in datos['unidad'] and not float_cantidad.is_integer():
                return False, "Para la medida 'Unidad(es)', la cantidad debe ser un número entero."
            fecha_obj = self.validar_y_convertir_fecha(datos['fecha'])
            if not fecha_obj:
                return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        except ValueError:
            return False, "La cantidad debe ser un número válido."

        def operacion(db):
            donacion = self.query_activa(db).filter(Donacion.id == id).first()
            if not donacion:
                raise ValueError("Donación no encontrada.")
            
            donacion.descripcion = datos['descripcion']
            donacion.cantidad = float_cantidad
            donacion.unidad = datos['unidad']
            donacion.equipo = datos['equipo']
            donacion.fecha = fecha_obj
            self.registrar_evento_sync(db, 'donaciones', donacion, 'upsert')
            logger.info(f"Donación actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Donación actualizada exitosamente.", user_context=user_context)

    def eliminar_donacion(self, id: int, user_context=None):
        if not id:
            return False, "El ID de la donación es obligatorio."

        def operacion(db):
            donacion = self.query_activa(db).filter(Donacion.id == id).first()
            if not donacion:
                raise ValueError("Donación no encontrada.")
            
            self.marcar_eliminado(donacion, db)
            self.registrar_evento_sync(db, 'donaciones', donacion, 'delete')
            logger.info(f"Donación eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Donación eliminada exitosamente.", user_context=user_context)

    def listar_donaciones(self, fecha: str = None):
        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            if fecha:
                fecha_obj = self.validar_y_convertir_fecha(fecha)
                if fecha_obj:
                    query = query.filter(Donacion.fecha == fecha_obj)
            donaciones = query.order_by(Donacion.fecha.desc(), Donacion.id.desc()).all()
            logger.info(f"{len(donaciones)} donaciones obtenidas de la base de datos.")
            return donaciones
        except SQLAlchemyError as e:
            logger.error(f"Error al listar donaciones: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def combinar_donaciones(self, datos_resultado: dict, lista_componentes: list, user_context=None):
        """
        Crea un AlimentoPreparado a partir de varias Donaciones (materias primas).
        :param datos_resultado: Datos del alimento producido.
        :param lista_componentes: Lista de {'id': donacion_id, 'cantidad': cant_usada}
        """
        if not datos_resultado.get('descripcion') or not datos_resultado.get('cantidad'):
            return False, "Los datos del alimento preparado son incompletos."
        if not lista_componentes:
            return False, "Debe incluir al menos una materia prima."

        fecha_obj = self.validar_y_convertir_fecha(datos_resultado.get('fecha'))
        if not fecha_obj:
            return False, "Fecha inválida."

        def operacion(db):
            # 1. Crear el Alimento Preparado
            preparado = AlimentoPreparado(
                descripcion=datos_resultado['descripcion'],
                cantidad=float(datos_resultado['cantidad']),
                unidad=datos_resultado['unidad'],
                equipo=datos_resultado['equipo'],
                fecha=fecha_obj
            )
            db.add(preparado)
            db.flush() # Para obtener el ID

            # 2. Registrar los componentes (materias primas usadas)
            for comp in lista_componentes:
                # Verificar que la donación exista
                materia = db.query(Donacion).filter(Donacion.id == comp['id']).first()
                if not materia:
                    raise ValueError(f"Materia prima con ID {comp['id']} no encontrada.")
                
                componente = AlimentoPreparadoComponente(
                    alimento_preparado_id=preparado.id,
                    donacion_materia_id=materia.id,
                    cantidad_usada=float(comp['cantidad'])
                )
                db.add(componente)
                # Nota: Siguiendo la lógica de tu Kivy, no descontamos del stock original.
            
            db.flush()
            self.registrar_evento_sync(db, 'alimentos_preparados', preparado, 'upsert')
            logger.info(f"Alimento preparado registrado: {preparado.descripcion}")

        return self.ejecutar_transaccion(operacion, "Alimento preparado registrado exitosamente.", user_context=user_context)

    def listar_preparados(self, fecha: str = None):
        db = self.get_db_session()
        try:
            query = db.query(AlimentoPreparado).filter(AlimentoPreparado.is_deleted.is_(False))
            if fecha:
                fecha_obj = self.validar_y_convertir_fecha(fecha)
                if fecha_obj:
                    query = query.filter(AlimentoPreparado.fecha == fecha_obj)
            return query.order_by(AlimentoPreparado.fecha.desc()).all()
        finally:
            if not self.session:
                db.close()

    def eliminar_preparado(self, id: int, user_context=None):
        def operacion(db):
            preparado = db.query(AlimentoPreparado).filter(AlimentoPreparado.id == id).first()
            if not preparado:
                raise ValueError("Registro no encontrado.")
            self.marcar_eliminado(preparado, db)
            self.registrar_evento_sync(db, 'alimentos_preparados', preparado, 'delete')
        return self.ejecutar_transaccion(operacion, "Registro eliminado.", user_context=user_context)

    def obtener_donacion(self, id: int):
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Donacion.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener donación: {e}")
            return None
        finally:
            if not self.session:
                db.close()

    def buscar_donacion(self, id=None, descripcion=None):
        if not id and not descripcion:
            return False, None, "Debe proporcionar un ID o una descripción para buscar la donación."
        
        db = self.get_db_session()
        try:
            query = self.query_activa(db)
            donacion = None
            if id:
                donacion = query.filter(Donacion.id == id).first()
            elif descripcion:
                donacion = query.filter(Donacion.descripcion.ilike(f"%{descripcion}%")).first()

            if donacion:
                return True, donacion, "Donación encontrada exitosamente."
            else:
                return False, None, "No se encontró la donación solicitada."
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar donación: {e}")
            return False, None, f"Error al buscar donación: {e}"
        finally:
            if not self.session:
                db.close()