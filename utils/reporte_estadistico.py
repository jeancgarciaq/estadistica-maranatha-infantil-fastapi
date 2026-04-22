import os
from dataclasses import dataclass
from datetime import datetime, date

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
        Image,
        PageBreak,
    )
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
    PageBreak = None
    REPORTLAB_DISPONIBLE = False

from sqlalchemy.orm import joinedload

from models.aulas import Aula
from models.donaciones import Donacion
from models.alimento_preparado import AlimentoPreparado
from models.alimento_preparado_componente import AlimentoPreparadoComponente
from models.distribucion import Distribucion
from models.logistica import Logistica


@dataclass
class ResumenEstadistico:
    fecha_corte: date
    asistencia_ninos: int
    asistencia_ninas: int
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
    logistica: list
    aulas: list
    donaciones: list
    preparados: list
    distribuciones: list
    componentes: list


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

    def obtener_resumen(self, fecha_corte):
        fecha_corte = self._parse_fecha(fecha_corte)

        aulas = self.session.query(Aula).options(joinedload(Aula.salon)).filter(Aula.fecha == fecha_corte).all()
        logistica = self.session.query(Logistica).filter(Logistica.fecha == fecha_corte).all()
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
                joinedload(Distribucion.salon),
                joinedload(Distribucion.area),
            )
            .filter(Distribucion.fecha == fecha_corte)
            .all()
        )

        asistencia_ninos = sum((a.ninos or 0) for a in aulas if (a.ninos or 0) > 0)
        asistencia_ninas = sum((a.ninas or 0) for a in aulas if (a.ninas or 0) > 0)

        servidores_aulas = sum(
            (a.auxiliar or 0) if (a.auxiliar or 0) > 0 else 0
            for a in aulas
        )
        servidores_aulas += sum(
            (a.capitan or 0) if (a.capitan or 0) > 0 else 0
            for a in aulas
        )
        servidores_aulas += sum(
            (a.colaborador or 0) if (a.colaborador or 0) > 0 else 0
            for a in aulas
        )
        servidores_aulas += sum(
            (a.maestra or 0) if (a.maestra or 0) > 0 else 0
            for a in aulas
        )
        servidores_aulas += sum(
            (a.subcapitan or 0) if (a.subcapitan or 0) > 0 else 0
            for a in aulas
        )

        servidores_logistica = 0
        for registro in logistica:
            for campo in ('almacen', 'capitan', 'distribucion', 'hidratacion', 'pasillo', 'secretaria'):
                valor = getattr(registro, campo, 0) or 0
                if valor > 0:
                    servidores_logistica += valor

        asistencia_servidores = servidores_aulas + servidores_logistica
        total_asistencia = asistencia_ninos + asistencia_ninas + asistencia_servidores

        donaciones_recibidas = sum((d.cantidad or 0) for d in donaciones)
        donaciones_combinadas = sum((p.cantidad or 0) for p in preparados)
        materiales_usados = sum((c.cantidad_usada or 0) for c in componentes)
        distribuciones_total = sum((d.cantidad or 0) for d in distribuciones)
        distribuciones_combinadas = distribuciones_total
        inventario_actual = sum((d.cantidad or 0) for d in self.session.query(Donacion).all()) - sum(
            (d.cantidad or 0) for d in self.session.query(Distribucion).all()
        )
        faltante_preparado = max(donaciones_combinadas - distribuciones_combinadas, 0)
        preparacion_completa = faltante_preparado == 0

        return ResumenEstadistico(
            fecha_corte=fecha_corte,
            asistencia_ninos=asistencia_ninos,
            asistencia_ninas=asistencia_ninas,
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
            logistica=logistica,
            aulas=aulas,
            donaciones=donaciones,
            preparados=preparados,
            distribuciones=distribuciones,
            componentes=componentes,
        )

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

    def _destino_texto(self, distribucion):
        if distribucion.salon:
            return f"Salón: {distribucion.salon.salon}"
        if distribucion.area:
            return f"Área: {distribucion.area.area}"
        return "Sin destino"

    def _nombre_donacion(self, distribucion):
        if distribucion.donacion:
            return distribucion.donacion.descripcion
        return str(distribucion.donacion_id)

    def generar_pdf(self, resumen, graficos, archivo_salida=None):
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
        story.append(Paragraph('Informe Estadístico de Domingo', styles['TituloInforme']))
        story.append(Paragraph(f'Fecha de corte: {resumen.fecha_corte.strftime("%d/%m/%Y")}', styles['CuerpoInforme']))
        story.append(Spacer(1, 0.3 * cm))

        story.append(Paragraph('1. Resumen Ejecutivo de Asistencia', styles['SubTituloInforme']))
        resumen_data = [
            ['Indicador', 'Valor'],
            ['Asistencia niños', str(resumen.asistencia_ninos)],
            ['Asistencia niñas', str(resumen.asistencia_ninas)],
            ['Asistencia servidores', str(resumen.asistencia_servidores)],
            ['Total asistencia', str(resumen.total_asistencia)],
        ]
        tabla = Table(resumen_data, colWidths=[9 * cm, 5 * cm])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A335C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(tabla)
        story.append(Spacer(1, 0.4 * cm))

        conclusion = 'La totalidad de lo preparado fue distribuida.' if resumen.preparacion_completa else (
            f'Quedó pendiente por distribuir {resumen.faltante_preparado:.2f} de lo preparado.'
        )
        story.append(Paragraph('2. Conclusión Operativa', styles['SubTituloInforme']))
        story.append(Paragraph(conclusion, styles['CuerpoInforme']))
        story.append(Spacer(1, 0.3 * cm))

        story.append(Paragraph('3. Gráficos', styles['SubTituloInforme']))
        story.append(Image(graficos['asistencia'], width=16 * cm, height=7.5 * cm))
        story.append(Spacer(1, 0.2 * cm))
        story.append(Image(graficos['alimentos'], width=16 * cm, height=7.5 * cm))
        story.append(Spacer(1, 0.3 * cm))

        story.append(Paragraph('4. Detalle de Asistencia por Aula', styles['SubTituloInforme']))
        aulas_data = [['ID', 'Aula', 'Niños', 'Niñas', 'Servidores', 'Total']]
        for aula in resumen.aulas:
            aulas_data.append([
                str(aula.id),
                getattr(aula.salon, 'salon', str(aula.id_salon)),
                str(aula.ninos or 0),
                str(aula.ninas or 0),
                str((aula.auxiliar or 0) + (aula.capitan or 0) + (aula.colaborador or 0) + (aula.maestra or 0) + (aula.subcapitan or 0)),
                str((aula.ninos or 0) + (aula.ninas or 0) + (aula.auxiliar or 0) + (aula.capitan or 0) + (aula.colaborador or 0) + (aula.maestra or 0) + (aula.subcapitan or 0)),
            ])
        tabla_aulas = Table(aulas_data, repeatRows=1)
        tabla_aulas.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A335C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(tabla_aulas)
        story.append(Spacer(1, 0.4 * cm))

        story.append(Paragraph('5. Donaciones', styles['SubTituloInforme']))
        donaciones_data = [['Descripción', 'Cantidad', 'Unidad']]
        for donacion in resumen.donaciones:
            donaciones_data.append([
                donacion.descripcion,
                f'{donacion.cantidad:.2f}',
                donacion.unidad,
            ])
        tabla_donaciones = Table(donaciones_data, repeatRows=1)
        tabla_donaciones.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A335C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(tabla_donaciones)
        story.append(Spacer(1, 0.3 * cm))

        story.append(Paragraph('6. Alimentos Preparados', styles['SubTituloInforme']))
        preparados_data = [['Descripción', 'Cantidad', 'Unidad', 'Equipo']]
        for preparado in resumen.preparados:
            preparados_data.append([
                preparado.descripcion,
                f'{preparado.cantidad:.2f}',
                preparado.unidad,
                preparado.equipo,
            ])
        tabla_preparados = Table(preparados_data, repeatRows=1)
        tabla_preparados.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A335C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(tabla_preparados)
        story.append(Spacer(1, 0.3 * cm))

        story.append(Paragraph('7. Alimentos Distribuidos', styles['SubTituloInforme']))
        distribuciones_data = [['Donación', 'Destino', 'Cantidad', 'Unidad']]
        for distribucion in resumen.distribuciones:
            distribuciones_data.append([
                self._nombre_donacion(distribucion),
                self._destino_texto(distribucion),
                f'{distribucion.cantidad:.2f}',
                distribucion.unidad,
            ])
        tabla_distribuciones = Table(distribuciones_data, repeatRows=1)
        tabla_distribuciones.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1A335C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))
        story.append(tabla_distribuciones)

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
