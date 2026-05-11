import logging
from models.logistica import Logistica # Assuming this model exists
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from controllers.base_controller import BaseController # Assuming BaseController exists
from controllers.asistencia_servidores_controller import AsistenciaServidoresController

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LogisticaController(BaseController):
    def __init__(self, session=None):
        super().__init__(model=Logistica, session=session)
        logger.info("LogisticaController inicializado.")

    def crear_logistica(self, datos, user_context=None):
        """
        Crea un nuevo registro de logística en la base de datos.
        :param datos: Diccionario con los datos de la logística.
        :return: (Exito, Mensaje)
        """
        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        fecha_dt = self.validar_y_convertir_fecha(datos.get('fecha'))
        if not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        datos['fecha'] = fecha_dt

        def operacion(db):
            logistica = Logistica(**datos)
            db.add(logistica)
            db.flush()
            self.registrar_evento_sync(db, 'logistica', logistica, 'upsert')
            logger.info("Logística creada.")

        return self.ejecutar_transaccion(operacion, "Logística creada exitosamente.", user_context=user_context)

    def crear_logistica_con_asistencia(self, datos, user_context=None):
        """Crea el registro de logística y registra la asistencia individual de cada puesto."""
        # Validar y convertir fecha
        fecha_dt = self.validar_y_convertir_fecha(datos.get('fecha'))
        if not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        datos['fecha'] = fecha_dt

        # Extraer IDs de servidores
        servidores_puestos = {
            'Capitán': datos.pop('id_capitan', None),
            'Almacén': datos.pop('id_almacen', None),
            'Distribución': datos.pop('id_distribucion', None),
            'Hidratación': datos.pop('id_hidratacion', None),
            'Pasillo': datos.pop('id_pasillo', None),
            'Secretaría': datos.pop('id_secretaria', None),
        }

        # Preparar contadores de resumen para la tabla Logistica (para compatibilidad con reportes)
        datos['almacen'] = 1 if servidores_puestos['Almacén'] else 0
        datos['distribucion'] = 1 if servidores_puestos['Distribución'] else 0
        datos['hidratacion'] = 1 if servidores_puestos['Hidratación'] else 0
        datos['pasillo'] = 1 if servidores_puestos['Pasillo'] else 0
        datos['secretaria'] = 1 if servidores_puestos['Secretaría'] else 0
        datos['capitan'] = 1 if servidores_puestos['Capitán'] else 0
        datos['id_capitan'] = servidores_puestos['Capitán']

        def operacion(db):
            asistencia_ctrl = AsistenciaServidoresController()
            
            # 1. Crear cabecera de Logistica
            logistica = Logistica(**datos)
            db.add(logistica)
            db.flush()

            # 2. Registrar asistencias individuales en la tabla pivote
            for rol, s_id in servidores_puestos.items():
                if s_id:
                    asistencia_ctrl.registrar_asistencia(
                        db,
                        id_servidor=s_id,
                        fecha=logistica.fecha,
                        rol=rol,
                        categoria='logistica',
                        referencia_id=logistica.id
                    )
            
            self.registrar_evento_sync(db, 'logistica', logistica, 'upsert')

        return self.ejecutar_transaccion(operacion, "Logística y asistencias registradas.", user_context=user_context)

    def actualizar_logistica(self, id, datos, user_context=None):
        """
        Actualiza un registro de logística existente.
        :param id: ID de la logística a actualizar.
        :param datos: Diccionario con los datos actualizados.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la logística es obligatorio y debe ser un número entero."

        errores = self.validar_datos(datos)
        if errores:
            return False, "\n".join(errores)

        fecha_dt = self.validar_y_convertir_fecha(datos.get('fecha'))
        if not fecha_dt:
            return False, "Formato de fecha incorrecto. Debe ser YYYY-MM-DD."
        datos['fecha'] = fecha_dt

        def operacion(db):
            logistica = db.query(Logistica).filter(Logistica.id == id, Logistica.is_deleted.is_(False)).first()
            if not logistica:
                raise ValueError("Logística no encontrada.")
            
            for key, value in datos.items():
                setattr(logistica, key, value)
            
            self.registrar_evento_sync(db, 'logistica', logistica, 'upsert')
            logger.info(f"Logística actualizada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Logística actualizada exitosamente.", user_context=user_context)

    def eliminar_logistica(self, id, user_context=None):
        """
        Elimina un registro de logística por su ID.
        :param id: ID de la logística a eliminar.
        :return: (Exito, Mensaje)
        """
        if not id or not isinstance(id, int):
            return False, "El ID de la logística es obligatorio y debe ser un número entero."

        def operacion(db):
            logistica = db.query(Logistica).filter(Logistica.id == id, Logistica.is_deleted.is_(False)).first()
            if not logistica:
                raise ValueError("Logística no encontrada.")
            
            self.marcar_eliminado(logistica, db)
            self.registrar_evento_sync(db, 'logistica', logistica, 'delete')
            logger.info(f"Logística eliminada: ID {id}")

        return self.ejecutar_transaccion(operacion, "Logística eliminada exitosamente.", user_context=user_context)

    def listar_logisticas(self, fecha=None):
        """
        Lista los registros de logística, opcionalmente filtrados por fecha.
        """
        db = self.get_db_session()
        try:
            query = self.query_activa(db)

            if fecha:
                fecha_dt = self.validar_y_convertir_fecha(fecha)
                if fecha_dt:
                    query = query.filter(Logistica.fecha == fecha_dt)

            logisticas = query.order_by(Logistica.fecha.desc(), Logistica.id.desc()).all()
            logger.info(f"{len(logisticas)} registros de logística obtenidos.")
            return logisticas
        except SQLAlchemyError as e:
            logger.error(f"Error al listar logísticas: {e}")
            return []
        finally:
            if not self.session:
                db.close()

    def obtener_logistica(self, id):
        """
        Obtiene un registro de logística por su ID.
        :param id: ID de la logística.
        :return: Objeto Logistica o None.
        """
        db = self.get_db_session()
        try:
            return self.query_activa(db).filter(Logistica.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener logística: {e}")
            return None
        finally:
            if not self.session:
                db.close()

    def validar_datos(self, datos):
        """
        Valida los datos proporcionados para crear o actualizar una logística.
        :param datos: Diccionario con los datos de la logística.
        :return: Lista de errores encontrados.
        """
        errores = []
        campos_numericos = ['almacen', 'capitan', 'distribucion', 'hidratacion', 'pasillo', 'secretaria']

        for campo in campos_numericos:
            valor = datos.get(campo)
            
            # Tratar None o cadenas vacías como 0 para normalizar el registro
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                datos[campo] = 0
                continue

            try:
                int_valor = int(valor)
                if int_valor < 0:
                    errores.append(f"El campo '{campo}' debe ser un número entero no negativo.")
                else:
                    datos[campo] = int_valor  # Aseguramos que el valor en el dict sea int para el modelo
            except (ValueError, TypeError):
                errores.append(f"El campo '{campo}' debe ser un número entero válido.")

        fecha = datos.get("fecha")
        if not fecha:
            errores.append("El campo 'fecha' es obligatorio.")
        elif isinstance(fecha, str):
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                errores.append("El campo 'fecha' debe tener el formato 'YYYY-MM-DD'.")

        return errores