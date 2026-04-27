import os
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    REPORTLAB_DISPONIBLE = True
except ModuleNotFoundError:
    colors = None
    A4 = None
    getSampleStyleSheet = None
    ParagraphStyle = None
    cm = None
    SimpleDocTemplate = None
    Paragraph = None
    Spacer = None
    Table = None
    TableStyle = None
    Image = None
    REPORTLAB_DISPONIBLE = False

from sqlalchemy.orm import joinedload

from models.aulas import Aula
from models.donaciones import Donacion
from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from models.distribucion import Distribucion
from models.areas import Area
from models.otras_areas import OtrasAreas
from models.recepcion import Recepcion


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
    otras_areas: list
    recepciones: list
    donaciones: list
    preparados: list
    distribuciones: list
    donaciones_sin_distribuir: list
    preparados_sin_distribuir: list


class ReporteEstadisticoService:
    def __init__(self, session):
        self.session = session
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.output_dir = os.path.join(self.base_dir, 'tmp', 'reportes')
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
        servidores = self._sumar_campos(aula, ['auxiliar', 'capitan', 'colaborador', 'maestra', 'subcapitan'])
        return {
            'id': aula.id,
            'nombre': getattr(aula.salon, 'salon', str(aula.id_salon)),
            'ninos': int(aula.ninos or 0),
            'ninas': int(aula.ninas or 0),
            'auxiliar': int(aula.auxiliar or 0),
            'capitan': int(aula.capitan or 0),
            'colaborador': int(aula.colaborador or 0),
            'maestra': int(aula.maestra or 0),
            'subcapitan': int(aula.subcapitan or 0),
            'servidores': servidores,
            'total': int(aula.ninos or 0) + int(aula.ninas or 0) + servidores,
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

    def _serializar_recepcion(self, recepcion):
        return {
            'id': recepcion.id,
            'nombre': str(recepcion.nombre or ''),
            'fecha': recepcion.fecha,
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

    def _pendientes_por_fuente(self, fuentes, distribuciones, atributo_id):
        distribuidos = defaultdict(float)
        for distribucion in distribuciones:
            origen_id = getattr(distribucion, atributo_id, None)
            if origen_id:
                distribuidos[origen_id] += float(distribucion.cantidad or 0)

        pendientes = []
        for fuente in fuentes:
            restante = float(fuente['cantidad']) - distribuidos.get(fuente['id'], 0.0)
            if restante > 0.0001:
                pendientes.append({
                    'id': fuente['id'],
                    'descripcion': fuente['descripcion'],
                    'cantidad_original': float(fuente['cantidad']),
                    'cantidad_distribuida': round(distribuidos.get(fuente['id'], 0.0), 2),
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

        aulas = self.session.query(Aula).options(joinedload(Aula.salon)).filter(Aula.fecha == fecha_corte).all()
        otras_areas = self.session.query(OtrasAreas).filter(OtrasAreas.fecha == fecha_corte).all()
        recepciones = self.session.query(Recepcion).filter(Recepcion.fecha == fecha_corte).all()
        donaciones = self.session.query(Donacion).filter(Donacion.fecha == fecha_corte).all()
        preparados = self.session.query(AlimentoPreparado).filter(AlimentoPreparado.fecha == fecha_corte).all()
        componentes = (
            self.session.query(AlimentoPreparadoComponente)
            .options(joinedload(AlimentoPreparadoComponente.materia_prima))
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

        aulas_data = [self._serializar_aula(aula) for aula in aulas]
        otras_areas_data = [self._serializar_otra_area(registro) for registro in otras_areas]
        recepciones_data = [self._serializar_recepcion(recepcion) for recepcion in recepciones]
        donaciones_data = [self._serializar_donacion(donacion) for donacion in donaciones]
        preparados_data = [self._serializar_preparado(preparado) for preparado in preparados]
        distribuciones_data = [self._serializar_distribucion(distribucion) for distribucion in distribuciones]

        asistencia_ninos = sum(item['ninos'] for item in aulas_data)
        asistencia_ninas = sum(item['ninas'] for item in aulas_data)
        asistencia_servidores_aulas = sum(item['servidores'] for item in aulas_data)
        asistencia_servidores_areas = sum(item['servidores'] for item in otras_areas_data)
        asistencia_servidores_recepcion = len(recepciones_data)
        asistencia_servidores = asistencia_servidores_aulas + asistencia_servidores_areas + asistencia_servidores_recepcion
        total_asistencia = asistencia_ninos + asistencia_ninas + asistencia_servidores

        donaciones_recibidas = sum(item['cantidad'] for item in donaciones_data)
        donaciones_combinadas = sum(item['cantidad'] for item in preparados_data)
        materiales_usados = sum(float(getattr(c, 'cantidad_usada', 0) or 0) for c in componentes)
        distribuciones_total = sum(item['cantidad'] for item in distribuciones_data)
        distribuciones_combinadas = sum(item['cantidad'] for item in distribuciones_data if item['origen_tipo'] == 'preparado')
        inventario_actual = max(donaciones_recibidas - distribuciones_total, 0)
        faltante_preparado = max(donaciones_combinadas - distribuciones_combinadas, 0)
        preparacion_completa = faltante_preparado == 0

        donaciones_sin_distribuir = self._pendientes_por_fuente(donaciones_data, distribuciones, 'donacion_id')
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
            otras_areas=otras_areas_data,
            recepciones=recepciones_data,
            donaciones=donaciones_data,
            preparados=preparados_data,
            distribuciones=distribuciones_data,
            donaciones_sin_distribuir=donaciones_sin_distribuir,
            preparados_sin_distribuir=preparados_sin_distribuir,
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
            f"Servidores de recepción: {resumen.asistencia_servidores_recepcion}",
            f"Total servidores: {resumen.asistencia_servidores}",
            f"Total asistencia: {resumen.total_asistencia}",
            '',
            '2. Asistencia por aula',
        ]
        if resumen.aulas:
            for aula in resumen.aulas:
                lineas.append(
                    f"- {aula['nombre']}: Niños {aula['ninos']}, Niñas {aula['ninas']}, "
                    f"Servidores {aula['servidores']}, Total {aula['total']}"
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
            '5. Distribución detallada',
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
            '6. Pendientes sin distribuir',
            f"Donaciones pendientes: {len(resumen.donaciones_sin_distribuir)}",
        ])
        for pendiente in resumen.donaciones_sin_distribuir:
            lineas.append(
                f"- {pendiente['descripcion']}: pendiente {self._fmt(pendiente['pendiente'])} {pendiente['unidad']}"
            )
        lineas.append(f"Alimentos preparados pendientes: {len(resumen.preparados_sin_distribuir)}")
        for pendiente in resumen.preparados_sin_distribuir:
            lineas.append(
                f"- {pendiente['descripcion']}: pendiente {self._fmt(pendiente['pendiente'])} {pendiente['unidad']}"
            )

        lineas.extend([
            '',
            '7. Servidores de otras áreas',
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
            '8. Recepción',
        ])
        if resumen.recepciones:
            for recepcion in resumen.recepciones:
                lineas.append(f"- ID {recepcion['id']}: {recepcion['nombre']}")
        else:
            lineas.append('- Sin registros de recepción.')

        lineas.extend([
            '',
            f"Estas son las estadísticas del servicio de fecha {resumen.fecha_corte.strftime('%d/%m/%Y')}, sin más que agregar atentamente, Coordinación de Secretaria.",
        ])
        return '\n'.join(lineas)

    def generar_graficos(self, resumen):
        fecha_texto = resumen.fecha_corte.strftime('%Y%m%d')
        ruta_asistencia = os.path.join(self.output_dir, f'asistencia_{fecha_texto}.png')
        ruta_alimentos = os.path.join(self.output_dir, f'alimentos_{fecha_texto}.png')

        plt.figure(figsize=(7, 4))
        categorias = ['Niños', 'Niñas', 'Servidores']
        valores = [resumen.asistencia_ninos, resumen.asistencia_ninas, resumen.asistencia_servidores]
        colores = ['#2F80ED', '#EB5757', '#27AE60']
        plt.bar(categorias, valores, color=colores)
        plt.title(f'Asistencia - {resumen.fecha_corte}')
        plt.ylabel('Cantidad')
        plt.tight_layout()
        plt.savefig(ruta_asistencia, dpi=180)
        plt.close()

        plt.figure(figsize=(7, 4))
        valores_alimentos = [resumen.donaciones_combinadas, resumen.distribuciones_combinadas, resumen.faltante_preparado]
        etiquetas = ['Preparado', 'Distribuido', 'Pendiente']
        colores = ['#F2994A', '#9B51E0', '#56CCF2']
        if sum(valores_alimentos) > 0:
            plt.pie(valores_alimentos, labels=etiquetas, autopct='%1.1f%%', colors=colores, startangle=90)
        else:
            plt.pie([1], labels=['Sin datos'], colors=['#BDBDBD'], startangle=90)
        plt.title('Estado de alimentos preparados')
        plt.tight_layout()
        plt.savefig(ruta_alimentos, dpi=180)
        plt.close()

        return {
            'asistencia': ruta_asistencia,
            'alimentos': ruta_alimentos,
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
        styles.add(ParagraphStyle(name='TituloInforme', parent=styles['Title'], fontSize=18, leading=22, spaceAfter=12))
        styles.add(ParagraphStyle(name='SubTituloInforme', parent=styles['Heading2'], fontSize=12, leading=14, spaceAfter=8))
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
        story.append(Spacer(1, 0.25 * cm))

        if graficos:
            graficos_existentes = [ruta for ruta in graficos.values() if ruta and os.path.exists(ruta)]
            if graficos_existentes:
                self._agregar_seccion(story, '2. Gráficos de referencia', styles)
                for ruta in graficos_existentes:
                    story.append(Image(ruta, width=16 * cm, height=7.5 * cm))
                    story.append(Spacer(1, 0.2 * cm))

        self._agregar_seccion(story, '3. Asistencia por aula', styles)
        aulas_data = [[
            'Aula', 'Niños', 'Niñas', 'Auxiliares', 'Capitanes', 'Colaboradores', 'Maestras', 'Subcapitanes', 'Total'
        ]]
        for aula in resumen.aulas:
            aulas_data.append([
                aula['nombre'],
                self._fmt(aula['ninos']),
                self._fmt(aula['ninas']),
                self._fmt(aula['auxiliar']),
                self._fmt(aula['capitan']),
                self._fmt(aula['colaborador']),
                self._fmt(aula['maestra']),
                self._fmt(aula['subcapitan']),
                self._fmt(aula['total']),
            ])
        if len(aulas_data) == 1:
            story.append(Paragraph('Sin registros de aulas.', styles['CuerpoInforme']))
        else:
            story.append(self._tabla(aulas_data))
        story.append(Spacer(1, 0.25 * cm))

        self._agregar_seccion(story, '4. Donaciones registradas', styles)
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
        story.append(Spacer(1, 0.25 * cm))

        self._agregar_seccion(story, '5. Alimentos preparados', styles)
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
        story.append(Spacer(1, 0.25 * cm))

        self._agregar_seccion(story, '6. Distribución detallada', styles)
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
        story.append(Spacer(1, 0.25 * cm))

        self._agregar_seccion(story, '7. Alimentos o donaciones no distribuidos', styles)
        if not resumen.donaciones_sin_distribuir and not resumen.preparados_sin_distribuir:
            story.append(Paragraph('No hay elementos pendientes por distribuir.', styles['CuerpoInforme']))
        else:
            if resumen.donaciones_sin_distribuir:
                story.append(Paragraph('Donaciones pendientes:', styles['CuerpoInforme']))
                pendientes_donaciones = [['Descripción', 'Original', 'Distribuido', 'Pendiente', 'Unidad']]
                for pendiente in resumen.donaciones_sin_distribuir:
                    pendientes_donaciones.append([
                        pendiente['descripcion'],
                        self._fmt(pendiente['cantidad_original']),
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
        story.append(Spacer(1, 0.25 * cm))

        self._agregar_seccion(story, '8. Servidores de otras áreas', styles)
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
        story.append(Spacer(1, 0.25 * cm))

        self._agregar_seccion(story, '9. Recepción', styles)
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
        self._agregar_seccion(story, '10. Cierre', styles)
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
