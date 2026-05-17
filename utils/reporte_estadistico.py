import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPM
    REPORTLAB_DISPONIBLE = True
except ModuleNotFoundError:
    colors: Any = None
    A4: Any = None
    getSampleStyleSheet: Any = None
    ParagraphStyle: Any = None
    cm: Any = None
    SimpleDocTemplate: Any = None
    Paragraph: Any = None
    Spacer: Any = None
    Table: Any = None
    TableStyle: Any = None
    Image: Any = None
    Drawing: Any = None
    VerticalBarChart: Any = None
    renderPM: Any = None
    REPORTLAB_DISPONIBLE = False

from sqlalchemy.orm import joinedload
from sqlalchemy import and_

from models.aulas import Aula
from models.donaciones import Donacion
from models.salones import Salon
from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from models.distribucion import Distribucion
from models.areas import Area
from models.otras_areas import OtrasAreas
from models.recepcion import Recepcion
from models.logistica import Logistica


@dataclass
class ResumenEstadistico:
    fecha_corte: date
    asistencia_ninos: int
    asistencia_ninas: int
    asistencia_servidores_aulas: int
    asistencia_servidores_areas: int
    asistencia_servidores_recepcion: int
    asistencia_servidores: int
    total_asistencia: int
    donaciones_recibidas: float
    donaciones_combinadas: float
    materiales_usados: float
    distribuciones_total: float
    distribuciones_combinadas: float
    inventario_actual: float
    faltante_preparado: float
    preparacion_completa: bool
    aulas: list
    aulas_por_categoria: dict # Agrupación por Maternal, Infantil, Pre-juvenil
    otras_areas: list
    recepciones: list
    logisticas: list # Nueva sección discriminada
    donaciones: list
    preparados: list
    componentes: list
    distribuciones: list
    donaciones_sin_distribuir: list
    preparados_sin_distribuir: list
    salones_cerrados: list # Nuevo campo para salones cerrados


class ReporteEstadisticoService:
    def __init__(self, session):
        self.session = session
        # En el entorno web móvil, guardamos los reportes en el almacenamiento del servidor
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.output_dir = os.path.join(self.base_dir, 'reportes')
        os.makedirs(self.output_dir, exist_ok=True)

    def _parse_fecha(self, fecha_corte):
        if isinstance(fecha_corte, date):
            return fecha_corte
        if isinstance(fecha_corte, str):
            return datetime.strptime(fecha_corte, '%Y-%m-%d').date()
        raise ValueError('La fecha de corte debe ser una fecha válida o cadena YYYY-MM-DD.')

    def _fmt(self, value):
        if value is None:
            return '0'
        if isinstance(value, float):
            return f'{value:.2f}'
        return str(value)

    def _sumar_campos(self, registro, campos):
        total = 0
        for campo in campos:
            total += int(getattr(registro, campo, 0) or 0)
        return total

    def _texto_destino(self, distribucion):
        if getattr(distribucion, 'salon', None):
            return f"Salón: {distribucion.salon.salon}"
        if getattr(distribucion, 'area', None):
            return f"Área: {distribucion.area.area}"
        if getattr(distribucion, 'recepcion', None):
            return f"Recepción: {distribucion.recepcion.nombre}"
        if getattr(distribucion, 'salon_id', None):
            return f"Salón ID {distribucion.salon_id}"
        if getattr(distribucion, 'area_id', None):
            return f"Área ID {distribucion.area_id}"
        if getattr(distribucion, 'recepcion_id', None):
            return f"Recepción ID {distribucion.recepcion_id}"
        return 'Sin destino'

    def _texto_origen(self, distribucion):
        if getattr(distribucion, 'donacion', None):
            return f"Donación: {distribucion.donacion.descripcion}"
        if getattr(distribucion, 'alimento_preparado', None):
            return f"Preparado: {distribucion.alimento_preparado.descripcion}"
        if getattr(distribucion, 'donacion_id', None):
            return f"Donación ID {distribucion.donacion_id}"
        if getattr(distribucion, 'alimento_preparado_id', None):
            return f"Preparado ID {distribucion.alimento_preparado_id}"
        return 'Sin origen'

    def _serializar_aula(self, aula):
        # Contamos servidores reales a partir de las nuevas relaciones jerárquicas
        cant_maestra = 1 if aula.id_maestra else 0
        cant_auxiliar = 1 if aula.id_auxiliar else 0
        
        # Obtenemos la lista de asistencias de colaboradores registrados para esta sesión
        asistencias_colab = getattr(aula, 'colaboradores_asistencias', [])
        cant_colaboradores = len(asistencias_colab)
        servidores = cant_maestra + cant_auxiliar + cant_colaboradores

        maestra_nom = aula.maestra_rel.nombre if aula.maestra_rel else "N/A"
        auxiliar_nom = aula.auxiliar_rel.nombre if aula.auxiliar_rel else "N/A"
        
        # Concatenamos nombres de todos los colaboradores para una visualización precisa
        nombres_colab = [a.servidor.nombre for a in asistencias_colab if a.servidor]
        colaborador_txt = ", ".join(nombres_colab) if nombres_colab else "N/A"
        
        return {
            'id': aula.id,
            'nombre': getattr(aula.salon, 'salon', str(aula.id_salon)),
            'categoria': getattr(aula.salon, 'edad', 'General'),
            'ninos': int(aula.ninos or 0),
            'ninas': int(aula.ninas or 0),
            'maestra': maestra_nom,
            'auxiliar': auxiliar_nom,
            'colaborador': colaborador_txt,
            'servidores': servidores,
            'total': int(aula.ninos or 0) + int(aula.ninas or 0) + servidores,
            'condicion': getattr(aula, 'condicion', 'Abierto')
        }

    def _serializar_otra_area(self, registro):
        servidores = self._sumar_campos(registro, ['alabanza', 'protocolo', 'semillitas', 'sonido', 'teatro', 'tv', 'ujier', 'seguridad'])
        return {
            'id': registro.id,
            'alabanza': int(registro.alabanza or 0),
            'protocolo': int(registro.protocolo or 0),
            'semillitas': int(registro.semillitas or 0),
            'sonido': int(registro.sonido or 0),
            'teatro': int(registro.teatro or 0),
            'tv': int(registro.tv or 0),
            'ujier': int(registro.ujier or 0),
            'seguridad': int(registro.seguridad or 0),
            'servidores': servidores,
            'fecha': registro.fecha,
        }

    def _serializar_logistica(self, log):
        # Recuperamos nombres de los capitanes y responsables de área
        return {
            'id': log.id,
            'capitan': getattr(log, 'capitan_rel', None).nombre if hasattr(log, 'capitan_rel') and log.capitan_rel else "No asignado",
            'almacen': "Sí" if log.almacen else "No",
            'distribucion': "Sí" if log.distribucion else "No",
            'hidratacion': "Sí" if log.hidratacion else "No",
            'pasillo': "Sí" if log.pasillo else "No",
            'secretaria': "Sí" if log.secretaria else "No",
            'observaciones': log.observaciones or ""
        }

    def _serializar_recepcion(self, recepcion):
        return {
            'id': recepcion.id,
            'nombre': str(recepcion.nombre or ''),
            'fecha': recepcion.fecha,
        }

    def _serializar_salon(self, salon):
        return {
            'id': salon.id,
            'nombre': salon.salon,
            'edad': salon.edad,
        }

    def _serializar_donacion(self, donacion):
        return {
            'id': donacion.id,
            'descripcion': donacion.descripcion,
            'cantidad': float(donacion.cantidad or 0),
            'unidad': donacion.unidad,
            'equipo': donacion.equipo or '',
        }

    def _serializar_preparado(self, preparado):
        return {
            'id': preparado.id,
            'descripcion': preparado.descripcion,
            'cantidad': float(preparado.cantidad or 0),
            'unidad': preparado.unidad,
            'equipo': preparado.equipo or '',
        }

    def _serializar_componente(self, componente):
        materia = getattr(componente, 'materia_prima', None)
        preparado = getattr(componente, 'alimento_preparado', None)
        return {
            'preparado_id': getattr(preparado, 'id', componente.alimento_preparado_id),
            'preparado_descripcion': getattr(preparado, 'descripcion', f'Preparado ID {componente.alimento_preparado_id}'),
            'materia_id': getattr(materia, 'id', componente.donacion_materia_id),
            'materia_descripcion': getattr(materia, 'descripcion', f'Donación ID {componente.donacion_materia_id}'),
            'cantidad_usada': float(componente.cantidad_usada or 0),
            'unidad': getattr(materia, 'unidad', ''),
        }

    def _serializar_distribucion(self, distribucion):
        return {
            'id': distribucion.id,
            'origen': self._texto_origen(distribucion),
            'destino': self._texto_destino(distribucion),
            'cantidad': float(distribucion.cantidad or 0),
            'unidad': distribucion.unidad,
            'fecha': distribucion.fecha,
            'origen_tipo': 'donación' if distribucion.donacion_id else 'preparado',
        }

    def _pendientes_por_fuente(self, fuentes, distribuciones, atributo_id, consumo_extra=None):
        distribuidos = defaultdict(float)
        for distribucion in distribuciones:
            origen_id = getattr(distribucion, atributo_id, None)
            if origen_id:
                distribuidos[origen_id] += float(distribucion.cantidad or 0)

        consumo_extra = consumo_extra or defaultdict(float)

        pendientes = []
        for fuente in fuentes:
            restante = float(fuente['cantidad']) - distribuidos.get(fuente['id'], 0.0) - consumo_extra.get(fuente['id'], 0.0)
            if restante > 0.0001:
                pendientes.append({
                    'id': fuente['id'],
                    'descripcion': fuente['descripcion'],
                    'cantidad_original': float(fuente['cantidad']),
                    'cantidad_distribuida': round(distribuidos.get(fuente['id'], 0.0), 2),
                    'cantidad_usada_en_preparados': round(consumo_extra.get(fuente['id'], 0.0), 2),
                    'pendiente': round(restante, 2),
                    'unidad': fuente['unidad'],
                })
        return pendientes

    def _tabla(self, datos, col_widths=None):
        tabla = Table(datos, repeatRows=1, colWidths=col_widths)
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A335C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ]))
        return tabla

    def _agregar_seccion(self, story, titulo, styles):
        story.append(Paragraph(titulo, styles['SubTituloInforme']))

    def obtener_resumen(self, fecha_corte):
        fecha_corte = self._parse_fecha(fecha_corte)

        aulas = (
            self.session.query(Aula)
            .options(
                joinedload(Aula.salon),
                joinedload(Aula.maestra_rel),
                joinedload(Aula.auxiliar_rel),
                joinedload(Aula.colaboradores_asistencias).joinedload('servidor')
            )
            .filter(Aula.fecha == fecha_corte)
            .all()
        )
        otras_areas = self.session.query(OtrasAreas).filter(OtrasAreas.fecha == fecha_corte).all()
        recepciones = self.session.query(Recepcion).filter(Recepcion.fecha == fecha_corte).all()
        logisticas = self.session.query(Logistica).filter(Logistica.fecha == fecha_corte).all()
        donaciones = self.session.query(Donacion).filter(Donacion.fecha == fecha_corte).all()
        preparados = self.session.query(AlimentoPreparado).filter(AlimentoPreparado.fecha == fecha_corte).all()
        componentes = (
            self.session.query(AlimentoPreparadoComponente)
            .options(
                joinedload(AlimentoPreparadoComponente.materia_prima),
                joinedload(AlimentoPreparadoComponente.alimento_preparado),
            )
            .join(AlimentoPreparado, AlimentoPreparado.id == AlimentoPreparadoComponente.alimento_preparado_id)
            .filter(AlimentoPreparado.fecha == fecha_corte)
            .all()
        )
        distribuciones = (
            self.session.query(Distribucion)
            .options(
                joinedload(Distribucion.donacion),
                joinedload(Distribucion.alimento_preparado),
                joinedload(Distribucion.salon),
                joinedload(Distribucion.area),
                joinedload(Distribucion.recepcion),
            )
            .filter(Distribucion.fecha == fecha_corte)
            .all()
        )

        # Obtener todos los salones activos
        todos_salones = self.session.query(Salon).filter(Salon.is_deleted == False).all()
        
        # IDs de los salones que sí tuvieron actividad (aulas registradas)
        salones_con_actividad_ids = {aula.id_salon for aula in aulas}

        aulas_data = [self._serializar_aula(aula) for aula in aulas]
        otras_areas_data = [self._serializar_otra_area(registro) for registro in otras_areas]
        recepciones_data = [self._serializar_recepcion(recepcion) for recepcion in recepciones]
        logisticas_data = [self._serializar_logistica(log) for log in logisticas]
        donaciones_data = [self._serializar_donacion(donacion) for donacion in donaciones]
        preparados_data = [self._serializar_preparado(preparado) for preparado in preparados]
        componentes_data = [self._serializar_componente(componente) for componente in componentes]
        distribuciones_data = [self._serializar_distribucion(distribucion) for distribucion in distribuciones]

        # Agrupar aulas por categoría (Edad)
        aulas_por_cat = defaultdict(list)
        for a in aulas_data:
            aulas_por_cat[a['categoria']].append(a)

        # Determinar salones cerrados
        salones_cerrados_data = [self._serializar_salon(s) for s in todos_salones 
                                 if s.id not in salones_con_actividad_ids]

        asistencia_ninos = sum(item['ninos'] for item in aulas_data)
        asistencia_ninas = sum(item['ninas'] for item in aulas_data)
        asistencia_servidores_aulas = sum(item['servidores'] for item in aulas_data)
        asistencia_servidores_areas = sum(item['servidores'] for item in otras_areas_data)
        asistencia_servidores_recepcion = len(recepciones_data) + sum(1 for l in logisticas_data if l['capitan'] != "No asignado")
        asistencia_servidores = asistencia_servidores_aulas + asistencia_servidores_areas + asistencia_servidores_recepcion
        total_asistencia = asistencia_ninos + asistencia_ninas + asistencia_servidores

        donaciones_recibidas = sum(item['cantidad'] for item in donaciones_data)
        donaciones_combinadas = sum(item['cantidad'] for item in preparados_data)
        materiales_usados = sum(item['cantidad_usada'] for item in componentes_data)
        distribuciones_total = sum(item['cantidad'] for item in distribuciones_data)
        distribuciones_donaciones = sum(item['cantidad'] for item in distribuciones_data if item['origen_tipo'] == 'donación')
        distribuciones_combinadas = sum(item['cantidad'] for item in distribuciones_data if item['origen_tipo'] == 'preparado')
        inventario_actual = max(donaciones_recibidas - distribuciones_donaciones - materiales_usados, 0)
        faltante_preparado = max(donaciones_combinadas - distribuciones_combinadas, 0)
        preparacion_completa = faltante_preparado == 0

        consumo_materias_primas = defaultdict(float)
        for componente in componentes_data:
            consumo_materias_primas[componente['materia_id']] += componente['cantidad_usada']

        donaciones_sin_distribuir = self._pendientes_por_fuente(donaciones_data, distribuciones, 'donacion_id', consumo_materias_primas)
        preparados_sin_distribuir = self._pendientes_por_fuente(preparados_data, distribuciones, 'alimento_preparado_id')

        return ResumenEstadistico(
            fecha_corte=fecha_corte,
            asistencia_ninos=asistencia_ninos,
            asistencia_ninas=asistencia_ninas,
            asistencia_servidores_aulas=asistencia_servidores_aulas,
            asistencia_servidores_areas=asistencia_servidores_areas,
            asistencia_servidores_recepcion=asistencia_servidores_recepcion,
            asistencia_servidores=asistencia_servidores,
            total_asistencia=total_asistencia,
            donaciones_recibidas=donaciones_recibidas,
            donaciones_combinadas=donaciones_combinadas,
            materiales_usados=materiales_usados,
            distribuciones_total=distribuciones_total,
            distribuciones_combinadas=distribuciones_combinadas,
            inventario_actual=inventario_actual,
            faltante_preparado=faltante_preparado,
            preparacion_completa=preparacion_completa,
            aulas=aulas_data,
            aulas_por_categoria=dict(aulas_por_cat),
            otras_areas=otras_areas_data,
            recepciones=recepciones_data,
            logisticas=logisticas_data,
            donaciones=donaciones_data,
            preparados=preparados_data,
            componentes=componentes_data,
            distribuciones=distribuciones_data,
            donaciones_sin_distribuir=donaciones_sin_distribuir,
            preparados_sin_distribuir=preparados_sin_distribuir,
            salones_cerrados=salones_cerrados_data,
        )

    def formatear_vista_previa(self, resumen):
        lineas = [
            f"Fecha del servicio: {resumen.fecha_corte.strftime('%d/%m/%Y')}",
            '',
            '1. Asistencia general',
            f"Niños: {resumen.asistencia_ninos}",
            f"Niñas: {resumen.asistencia_ninas}",
            f"Servidores de aulas: {resumen.asistencia_servidores_aulas}",
            f"Servidores de otras áreas: {resumen.asistencia_servidores_areas}",
            f"Servidores de recepción/logística: {resumen.asistencia_servidores_recepcion}",
            f"Total servidores: {resumen.asistencia_servidores}",
            f"Total asistencia: {resumen.total_asistencia}",
            '',
            '2. Asistencia Detallada por Aulas',
        ]
        if resumen.aulas_por_categoria:
            for cat, lista in resumen.aulas_por_categoria.items():
                lineas.append(f"\n--- Categoría: {cat} ---")
                for aula in lista:
                    lineas.append(
                        f"- {aula['nombre']}: {aula['ninos']} Niños, {aula['ninas']} Niñas | "
                        f"Maestra: {aula['maestra']} | Aux: {aula['auxiliar']} | Colab: {aula['colaborador']}"
                    )
        else:
            lineas.append('- Sin registros de aulas.')

        lineas.extend([
            '',
            '3. Donaciones registradas',
        ])
        if resumen.donaciones:
            for donacion in resumen.donaciones:
                lineas.append(f"- {donacion['descripcion']}: {self._fmt(donacion['cantidad'])} {donacion['unidad']}")
        else:
            lineas.append('- Sin donaciones registradas.')

        lineas.extend([
            '',
            '4. Alimentos preparados',
        ])
        if resumen.preparados:
            for preparado in resumen.preparados:
                lineas.append(f"- {preparado['descripcion']}: {self._fmt(preparado['cantidad'])} {preparado['unidad']} ({preparado['equipo']})")
        else:
            lineas.append('- Sin alimentos preparados registrados.')

        lineas.extend([
            '',
            '5. Conversión de donaciones en alimentos preparados',
        ])
        if resumen.componentes:
            agrupados = defaultdict(list)
            for componente in resumen.componentes:
                agrupados[componente['preparado_id']].append(componente)
            for items in agrupados.values():
                lineas.append(f"- {items[0]['preparado_descripcion']}:")
                for item in items:
                    lineas.append(
                        f"  * {item['materia_descripcion']}: {self._fmt(item['cantidad_usada'])} {item['unidad']}"
                    )
        else:
            lineas.append('- Sin conversión registrada.')

        lineas.extend([
            '',
            '6. Distribución detallada',
        ])
        if resumen.distribuciones:
            for distribucion in resumen.distribuciones:
                lineas.append(
                    f"- {distribucion['origen']} -> {distribucion['destino']}: {self._fmt(distribucion['cantidad'])} {distribucion['unidad']}"
                )
        else:
            lineas.append('- Sin distribuciones registradas.')

        lineas.extend([
            '',
            '7. Pendientes sin distribuir',
            f"Donaciones pendientes: {len(resumen.donaciones_sin_distribuir)}",
        ])
        for pendiente in resumen.donaciones_sin_distribuir:
            lineas.append(
                f"- {pendiente['descripcion']}: usada en preparados {self._fmt(pendiente['cantidad_usada_en_preparados'])} {pendiente['unidad']}, pendiente {self._fmt(pendiente['pendiente'])} {pendiente['unidad']}"
            )
        lineas.append(f"Alimentos preparados pendientes: {len(resumen.preparados_sin_distribuir)}")
        for pendiente in resumen.preparados_sin_distribuir:
            lineas.append(
                f"- {pendiente['descripcion']}: pendiente {self._fmt(pendiente['pendiente'])} {pendiente['unidad']}"
            )

        lineas.extend([
            '',
            '8. Servidores de otras áreas',
        ])
        if resumen.otras_areas:
            for registro in resumen.otras_areas:
                lineas.append(
                    f"- ID {registro['id']}: total {registro['servidores']} (Alabanza {registro['alabanza']}, Protocolo {registro['protocolo']}, Semillitas {registro['semillitas']}, Sonido {registro['sonido']}, Teatro {registro['teatro']}, TV {registro['tv']}, Ujier {registro['ujier']}, Seguridad {registro['seguridad']})"
                )
        else:
            lineas.append('- Sin registros de otras áreas.')

        lineas.extend([
            '',
            '9. Gestión de Logística',
        ])
        if resumen.logisticas:
            for log in resumen.logisticas:
                lineas.append(
                    f"- Capitán: {log['capitan']} | Almacén: {log['almacen']} | Hidratación: {log['hidratacion']} | Pasillo: {log['pasillo']}"
                )
        else:
            lineas.append('- Sin registros de logística.')

        lineas.extend([
            '',
            '9. Recepción',
        ])
        if resumen.recepciones:
            for recepcion in resumen.recepciones:
                lineas.append(f"- ID {recepcion['id']}: {recepcion['nombre']}")
        else:
            lineas.append('- Sin registros de recepción.')
            
        lineas.extend([
            '',
            '2. Salones Cerrados (sin registro de asistencia)',
        ])
        if resumen.salones_cerrados:
            for salon in resumen.salones_cerrados:
                lineas.append(f"- {salon['nombre']} (Edad: {salon['edad']})")
        else:
            lineas.append('- Todos los salones tuvieron registro de asistencia.')

        lineas.extend([
            '',
            f"Estas son las estadísticas del servicio de fecha {resumen.fecha_corte.strftime('%d/%m/%Y')}, sin más que agregar atentamente, Coordinación de Secretaria.",
        ])
        return '\n'.join(lineas)

    def generar_graficos(self, resumen):
        if not REPORTLAB_DISPONIBLE:
            return {'asistencia': None}

        # Creamos el objeto Drawing. No necesitamos renderPM (PNG) si insertamos 
        # el vector directamente en el PDF, evitando errores de backends (rlPyCairo/Pillow).
        drawing = Drawing(450, 250)
        chart = VerticalBarChart()
        chart.x = 40
        chart.y = 50
        chart.width = 380
        chart.height = 160
        
        # Aseguramos que los datos sean numéricos y forzamos una serie explícita
        ninos = int(resumen.asistencia_ninos or 0)
        ninas = int(resumen.asistencia_ninas or 0)
        servidores = int(resumen.asistencia_servidores or 0)
        chart.data = [[ninos, ninas, servidores]]
        chart.categoryAxis.categoryNames = ['Niños', 'Niñas', 'Servidores']
        
        # Colores individuales para cada barra
        chart.bars[(0, 0)].fillColor = colors.HexColor('#2F80ED')  # Azul para Niños
        chart.bars[(0, 1)].fillColor = colors.HexColor('#EB5757')  # Rojo para Niñas
        chart.bars[(0, 2)].fillColor = colors.HexColor('#27AE60')  # Verde para Servidores
        
        # Configuración del eje de valores (Y) para mejor visibilidad
        chart.valueAxis.labelTextFormat = '%d'
        chart.valueAxis.forceZero = 1
        chart.valueAxis.valueMin = 0
        
        drawing.add(chart)
        return {
            'asistencia': drawing,
        }

    def generar_pdf(self, resumen, graficos=None, archivo_salida=None):
        if not REPORTLAB_DISPONIBLE:
            raise ModuleNotFoundError(
                'reportlab no está instalado en el entorno activo. Instale la dependencia antes de generar el PDF.'
            )

        fecha_texto = resumen.fecha_corte.strftime('%Y%m%d')
        if archivo_salida is None:
            archivo_salida = os.path.join(self.output_dir, f'reporte_estadistico_{fecha_texto}.pdf')

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='TituloInforme', parent=styles['Title'], fontSize=18, leading=22, spaceAfter=12, keepWithNext=True))
        styles.add(ParagraphStyle(name='SubTituloInforme', parent=styles['Heading2'], fontSize=12, leading=14, spaceAfter=8, keepWithNext=True))
        styles.add(ParagraphStyle(name='CuerpoInforme', parent=styles['BodyText'], fontSize=9, leading=12))

        story = []
        story.append(Paragraph('Informe Estadístico del Servicio', styles['TituloInforme']))
        story.append(Paragraph(f'Fecha de corte: {resumen.fecha_corte.strftime("%d/%m/%Y")}', styles['CuerpoInforme']))
        story.append(Spacer(1, 0.3 * cm))

        self._agregar_seccion(story, '1. Resumen general', styles)
        resumen_data = [
            ['Indicador', 'Valor'],
            ['Niños', self._fmt(resumen.asistencia_ninos)],
            ['Niñas', self._fmt(resumen.asistencia_ninas)],
            ['Servidores aulas', self._fmt(resumen.asistencia_servidores_aulas)],
            ['Servidores otras áreas', self._fmt(resumen.asistencia_servidores_areas)],
            ['Servidores recepción', self._fmt(resumen.asistencia_servidores_recepcion)],
            ['Total servidores', self._fmt(resumen.asistencia_servidores)],
            ['Total asistencia', self._fmt(resumen.total_asistencia)],
        ]
        story.append(self._tabla(resumen_data, [9 * cm, 5 * cm]))

        story.append(Spacer(1, 0.3 * cm))
        self._agregar_seccion(story, '2. Salones Cerrados (sin registro de asistencia)', styles)
        if resumen.salones_cerrados:
            salones_cerrados_data = [['ID', 'Nombre del Salón', 'Edad']]
            for salon in resumen.salones_cerrados:
                salones_cerrados_data.append([
                    str(salon['id']),
                    salon['nombre'],
                    salon['edad'],
                ])
            story.append(self._tabla(salones_cerrados_data))
        else:
            story.append(Paragraph('Todos los salones tuvieron registro de asistencia.', styles['CuerpoInforme']))

        if graficos:
            # Verificamos si hay gráficos (objetos Drawing o rutas de archivos)
            graficos_validos = [v for v in graficos.values() if v]
            if graficos_validos:
                story.append(Spacer(1, 0.5 * cm))
                self._agregar_seccion(story, '3. Gráficos de referencia', styles)
                for item in graficos_validos:
                    if isinstance(item, str) and os.path.exists(item):
                        story.append(Image(item, width=16 * cm, height=7.5 * cm))
                    else:
                        story.append(item) # Insertar Drawing directamente
                    story.append(Spacer(1, 0.3 * cm))

        self._agregar_seccion(story, '4. Asistencia detallada por aula', styles)
        if resumen.aulas_por_categoria:
            for cat, aulas_cat in resumen.aulas_por_categoria.items():
                story.append(Paragraph(f"Categoría: {cat}", styles['SubTituloInforme']))
                data_cat = [['Aula', 'Niños', 'Niñas', 'Maestra', 'Auxiliar', 'Colaboradores', 'Total']]
                for a in aulas_cat:
                    data_cat.append([
                        a['nombre'],
                        self._fmt(a['ninos']),
                        self._fmt(a['ninas']),
                        a['maestra'],
                        a['auxiliar'],
                        a['colaborador'],
                        self._fmt(a['total']),
                    ])
                story.append(self._tabla(data_cat, [3*cm, 1*cm, 1*cm, 2.5*cm, 2.5*cm, 3.5*cm, 1.5*cm]))
                story.append(Spacer(1, 0.4 * cm))
        else:
            story.append(Paragraph('Sin registros de aulas.', styles['CuerpoInforme']))

        self._agregar_seccion(story, '5. Donaciones registradas', styles)
        donaciones_data = [['Descripción', 'Cantidad', 'Unidad', 'Equipo']]
        for donacion in resumen.donaciones:
            donaciones_data.append([
                donacion['descripcion'],
                self._fmt(donacion['cantidad']),
                donacion['unidad'],
                donacion['equipo'],
            ])
        if len(donaciones_data) == 1:
            story.append(Paragraph('Sin donaciones registradas.', styles['CuerpoInforme']))
        else:
            story.append(self._tabla(donaciones_data))

        self._agregar_seccion(story, '6. Alimentos preparados', styles)
        preparados_data = [['Descripción', 'Cantidad', 'Unidad', 'Equipo']]
        for preparado in resumen.preparados:
            preparados_data.append([
                preparado['descripcion'],
                self._fmt(preparado['cantidad']),
                preparado['unidad'],
                preparado['equipo'],
            ])
        if len(preparados_data) == 1:
            story.append(Paragraph('Sin alimentos preparados registrados.', styles['CuerpoInforme']))
        else:
            story.append(self._tabla(preparados_data))

        self._agregar_seccion(story, '7. Conversión de donaciones en alimentos preparados', styles)
        if resumen.componentes:
            conversion_data = [['Preparado', 'Materia prima', 'Cantidad usada', 'Unidad']]
            for componente in resumen.componentes:
                conversion_data.append([
                    componente['preparado_descripcion'],
                    componente['materia_descripcion'],
                    self._fmt(componente['cantidad_usada']),
                    componente['unidad'],
                ])
            story.append(self._tabla(conversion_data))
        else:
            story.append(Paragraph('Sin conversión registrada.', styles['CuerpoInforme']))

        self._agregar_seccion(story, '8. Distribución detallada', styles)
        distribuciones_data = [['Origen', 'Destino', 'Cantidad', 'Unidad']]
        for distribucion in resumen.distribuciones:
            distribuciones_data.append([
                distribucion['origen'],
                distribucion['destino'],
                self._fmt(distribucion['cantidad']),
                distribucion['unidad'],
            ])
        if len(distribuciones_data) == 1:
            story.append(Paragraph('Sin distribuciones registradas.', styles['CuerpoInforme']))
        else:
            story.append(self._tabla(distribuciones_data))

        self._agregar_seccion(story, '9. Alimentos o donaciones no distribuidos', styles)
        if not resumen.donaciones_sin_distribuir and not resumen.preparados_sin_distribuir:
            story.append(Paragraph('No hay elementos pendientes por distribuir.', styles['CuerpoInforme']))
        else:
            if resumen.donaciones_sin_distribuir:
                story.append(Paragraph('Donaciones pendientes:', styles['CuerpoInforme']))
                pendientes_donaciones = [['Descripción', 'Original', 'Usado en preparados', 'Distribuido', 'Pendiente', 'Unidad']]
                for pendiente in resumen.donaciones_sin_distribuir:
                    pendientes_donaciones.append([
                        pendiente['descripcion'],
                        self._fmt(pendiente['cantidad_original']),
                        self._fmt(pendiente['cantidad_usada_en_preparados']),
                        self._fmt(pendiente['cantidad_distribuida']),
                        self._fmt(pendiente['pendiente']),
                        pendiente['unidad'],
                    ])
                story.append(self._tabla(pendientes_donaciones))
                story.append(Spacer(1, 0.15 * cm))
            if resumen.preparados_sin_distribuir:
                story.append(Paragraph('Preparados pendientes:', styles['CuerpoInforme']))
                pendientes_preparados = [['Descripción', 'Original', 'Distribuido', 'Pendiente', 'Unidad']]
                for pendiente in resumen.preparados_sin_distribuir:
                    pendientes_preparados.append([
                        pendiente['descripcion'],
                        self._fmt(pendiente['cantidad_original']),
                        self._fmt(pendiente['cantidad_distribuida']),
                        self._fmt(pendiente['pendiente']),
                        pendiente['unidad'],
                    ])
                story.append(self._tabla(pendientes_preparados))

        self._agregar_seccion(story, '10. Servidores de otras áreas', styles)
        if resumen.otras_areas:
            otras_areas_data = [['ID', 'Alabanza', 'Protocolo', 'Semillitas', 'Sonido', 'Teatro', 'TV', 'Ujier', 'Seguridad', 'Total']]
            for registro in resumen.otras_areas:
                otras_areas_data.append([
                    str(registro['id']),
                    self._fmt(registro['alabanza']),
                    self._fmt(registro['protocolo']),
                    self._fmt(registro['semillitas']),
                    self._fmt(registro['sonido']),
                    self._fmt(registro['teatro']),
                    self._fmt(registro['tv']),
                    self._fmt(registro['ujier']),
                    self._fmt(registro['seguridad']),
                    self._fmt(registro['servidores']),
                ])
            story.append(self._tabla(otras_areas_data))
        else:
            story.append(Paragraph('Sin registros de otras áreas.', styles['CuerpoInforme']))

        self._agregar_seccion(story, '11. Gestión de Logística', styles)
        if resumen.logisticas:
            log_data = [['Capitán', 'Almacén', 'Hidratación', 'Pasillo', 'Secretaría']]
            for log in resumen.logisticas:
                log_data.append([
                    log['capitan'],
                    log['almacen'],
                    log['hidratacion'],
                    log['pasillo'],
                    log['secretaria']
                ])
            story.append(self._tabla(log_data))
        else:
            story.append(Paragraph('Sin registros de logística.', styles['CuerpoInforme']))

        self._agregar_seccion(story, '12. Recepción', styles)
        if resumen.recepciones:
            recepciones_data = [['ID', 'Nombre']]
            for recepcion in resumen.recepciones:
                recepciones_data.append([str(recepcion['id']), recepcion['nombre']])
            story.append(self._tabla(recepciones_data, [3 * cm, 12 * cm]))
        else:
            story.append(Paragraph('Sin registros de recepción.', styles['CuerpoInforme']))
            
        story.append(Spacer(1, 0.3 * cm))

        conclusion = (
            f'Estas son las estadísticas del servicio de fecha {resumen.fecha_corte.strftime("%d/%m/%Y")}, '
            'sin más que agregar atentamente, Coordinación de Secretaria.'
        )
        self._agregar_seccion(story, '13. Cierre', styles)
        story.append(Paragraph(conclusion, styles['CuerpoInforme']))

        doc = SimpleDocTemplate(
            archivo_salida,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )
        doc.build(story)
        return archivo_salida
