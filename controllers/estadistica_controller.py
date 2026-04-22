import logging

from controllers.base_controller import BaseController
from utils.reporte_estadistico import ReporteEstadisticoService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EstadisticaController(BaseController):
	def __init__(self, session=None):
		super().__init__(session=session)
		if session is None:
			logger.error('No se ha proporcionado una sesión de base de datos.')
			raise ValueError('Se requiere una sesión de base de datos para el controlador.')
		self.servicio = ReporteEstadisticoService(self.session)
		logger.info('EstadisticaController inicializado con éxito.')

	def obtener_vista_estadistica(self, fecha_corte):
		resumen = self.servicio.obtener_resumen(fecha_corte)
		graficos = self.servicio.generar_graficos(resumen)
		return {
			'resumen': resumen,
			'graficos': graficos,
			'secciones': self._construir_secciones(resumen, graficos),
		}

	def _construir_secciones(self, resumen, graficos):
		total_ninos = resumen.asistencia_ninos + resumen.asistencia_ninas
		introduccion = (
			f'Se está presentando la información relacionada con la estadística del servicio de fecha '
			f'{resumen.fecha_corte.strftime("%d/%m/%Y")}. '
			f'Inicialmente damos a conocer que estuvieron trabajando {resumen.asistencia_servidores} servidores '
			f'y se atendió un total de {total_ninos} niños.'
		)

		distribucion_por_preparado = {}
		for distribucion in resumen.distribuciones:
			preparado_id = getattr(distribucion, 'alimento_preparado_id', None)
			if preparado_id:
				distribucion_por_preparado[preparado_id] = distribucion_por_preparado.get(preparado_id, 0) + (distribucion.cantidad or 0)

		secciones = [
			{
				'tipo': 'texto',
				'titulo': '1. Asistencia Del Servicio',
				'texto': introduccion,
			},
			{
				'tipo': 'tabla',
				'titulo': 'Tabla de Asistencia Resumen',
				'encabezados': ['Indicador', 'Valor'],
				'filas': [
					['Asistencia niños', str(resumen.asistencia_ninos)],
					['Asistencia niñas', str(resumen.asistencia_ninas)],
					['Asistencia servidores', str(resumen.asistencia_servidores)],
					['Total asistencia', str(resumen.total_asistencia)],
				],
			},
			{
				'tipo': 'tabla',
				'titulo': 'Tabla de Asistencia por Aula',
				'encabezados': ['ID', 'Aula', 'Niños', 'Niñas', 'Servidores', 'Total'],
				'filas': [
					[
						str(aula.id),
						getattr(aula.salon, 'salon', str(aula.id_salon)),
						str(aula.ninos or 0),
						str(aula.ninas or 0),
						str((aula.auxiliar or 0) + (aula.capitan or 0) + (aula.colaborador or 0) + (aula.maestra or 0) + (aula.subcapitan or 0)),
						str((aula.ninos or 0) + (aula.ninas or 0) + (aula.auxiliar or 0) + (aula.capitan or 0) + (aula.colaborador or 0) + (aula.maestra or 0) + (aula.subcapitan or 0)),
					]
					for aula in resumen.aulas
				] or [['Sin aulas registradas', '-', '-', '-', '-', '-']],
			},
			{
				'tipo': 'imagen',
				'titulo': '2. Representación Gráfica De La Asistencia',
				'ruta': graficos['asistencia'],
			},
			{
				'tipo': 'texto',
				'titulo': '3. Donaciones, Preparados Y Observaciones Del Servicio',
				'texto': 'Estas son las donaciones que se recibieron para el servicio del día domingo:',
			},
			{
				'tipo': 'tabla',
				'titulo': 'Tabla de Donaciones Recibidas',
				'encabezados': ['Descripción', 'Cantidad', 'Unidad'],
				'filas': [
					[donacion.descripcion, f'{donacion.cantidad:.2f}', donacion.unidad]
					for donacion in resumen.donaciones
				] or [['Sin donaciones registradas para la fecha', '-', '-']],
			},
			{
				'tipo': 'texto',
				'texto': 'Luego de estas donaciones se lograron preparar la siguiente cantidad de alimentos:',
			},
			{
				'tipo': 'tabla',
				'titulo': 'Tabla de Alimentos Preparados',
				'encabezados': ['Descripción', 'Cantidad', 'Unidad', 'Equipo'],
				'filas': [
					[preparado.descripcion, f'{preparado.cantidad:.2f}', preparado.unidad, preparado.equipo]
					for preparado in resumen.preparados
				] or [['Sin preparados registrados para la fecha', '-', '-', '-']],
			},
			{
				'tipo': 'tabla',
				'titulo': 'Cantidad Repartida Y Sobrante De Alimentos Preparados',
				'encabezados': ['Alimento preparado', 'Cantidad preparada', 'Cantidad repartida', 'Cantidad sobrante', 'Unidad'],
				'filas': self._filas_control_preparados(resumen, distribucion_por_preparado),
			},
			{
				'tipo': 'tabla',
				'titulo': 'Tabla de Sobrantes de Alimentos Preparados',
				'encabezados': ['Alimento preparado', 'Cantidad sobrante', 'Unidad'],
				'filas': self._filas_sobrantes_preparados(resumen, distribucion_por_preparado),
			},
			{
				'tipo': 'texto',
				'texto': 'Las siguientes donaciones no fueron repartidas a los niños ni a los servidores durante el servicio:',
			},
			{
				'tipo': 'tabla',
				'titulo': 'Donaciones No Repartidas',
				'encabezados': ['Descripción', 'Cantidad', 'Unidad'],
				'filas': [
					[donacion.descripcion, f'{donacion.cantidad:.2f}', donacion.unidad]
					for donacion in resumen.donaciones_no_repartidas
				] or [['No hay donaciones pendientes sin repartir', '-', '-']],
			},
			{
				'tipo': 'tabla',
				'titulo': 'Salones Cerrados',
				'encabezados': ['Salón', 'Edad'],
				'filas': [
					[salon.salon, salon.edad]
					for salon in resumen.salones_cerrados
				] or [['No se registran salones cerrados para la fecha', '-']],
			},
			{
				'tipo': 'texto',
				'texto': (
					'Esta fue la información que se recopiló del servicio del día, esperando que la información pueda ser de utilidad. '
					'Sin más que añadir, atentamente la coordinación de Maranatha Kids.'
				),
			},
		]
		return secciones

	def _filas_control_preparados(self, resumen, distribucion_por_preparado):
		filas = []
		for preparado in resumen.preparados:
			cantidad_preparada = preparado.cantidad or 0
			cantidad_repartida = distribucion_por_preparado.get(preparado.id, 0)
			cantidad_sobrante = max(cantidad_preparada - cantidad_repartida, 0)
			filas.append([
				preparado.descripcion,
				f'{cantidad_preparada:.2f}',
				f'{cantidad_repartida:.2f}',
				f'{cantidad_sobrante:.2f}',
				preparado.unidad,
			])
		if not filas:
			return [['Sin alimentos preparados para la fecha', '-', '-', '-', '-']]
		return filas

	def _filas_sobrantes_preparados(self, resumen, distribucion_por_preparado):
		filas = []
		for preparado in resumen.preparados:
			cantidad_preparada = preparado.cantidad or 0
			cantidad_repartida = distribucion_por_preparado.get(preparado.id, 0)
			cantidad_sobrante = max(cantidad_preparada - cantidad_repartida, 0)
			if cantidad_sobrante > 0:
				filas.append([
					preparado.descripcion,
					f'{cantidad_sobrante:.2f}',
					preparado.unidad,
				])
		if not filas:
			return [['No hubo sobrantes de alimentos preparados', '-', '-']]
		return filas