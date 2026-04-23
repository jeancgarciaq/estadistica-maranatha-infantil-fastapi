import logging
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from components.styled_popup import StyledPopup
from datetime import datetime
from components.styled_datepicker import StyledDatePicker
from utils.config_loader import obtener_medidas
import traceback

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)  # Cambiar a DEBUG para mayor detalle
logger = logging.getLogger(__name__)

from models.donaciones import Donacion
from models.alimento_preparado import AlimentoPreparado
from models.salones import Salon
from models.areas import Area

Builder.load_file('views/distribucion.kv')

class DistribucionesScreen(Screen):
    medidas = ListProperty([])

    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.medidas = obtener_medidas()
        self.controlador = controlador
        self.edit_id = None
        logger.info("DistribucionesScreen inicializado correctamente.")

    def abrir_datepicker(self, target_id):
        """Abre el selector de fecha."""
        def set_date(date_str):
            self.ids[target_id].text = date_str
            
        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def on_pre_enter(self, *args):
        """Se ejecuta antes de que la pantalla sea visible."""
        logger.debug(f"Ejecutando on_pre_enter... edit_id: {self.edit_id}")
        if self.edit_id is None:
            Clock.schedule_once(self.cargar_datos, 1)
    
    def obtener_datos_formulario(self):
        donacion_id = self.ids.donacion_id.text.strip()
        alimento_preparado_id = self.ids.alimento_preparado_id.text.strip()
        salon_id = self.ids.salon_id.text.strip()
        area_id = self.ids.area_id.text.strip()
        cantidad = self.ids.donacion_cantidad.text.strip()
        fecha = self.ids.fecha.text.strip()

        #Validación básica
        if not donacion_id and not alimento_preparado_id:
            StyledPopup.mostrar_popup("Error", "Debe seleccionar un origen: donación o preparado.", tipo="error")
            return None
        if donacion_id and alimento_preparado_id:
            StyledPopup.mostrar_popup("Error", "Solo puede seleccionar un origen: donación o preparado.", tipo="error")
            return None
        if not salon_id and not area_id:
            StyledPopup.mostrar_popup("Error", "Debe seleccionar un salón o un área.", tipo="error")
            return None
        if salon_id and area_id:
            StyledPopup.mostrar_popup("Error", "Solo puede seleccionar un destino: salón o área.", tipo="error")
            return None
        if not cantidad:
            StyledPopup.mostrar_popup("Error", "La cantidad es obligatoria.", tipo="error")
            return None
        if not fecha:
            StyledPopup.mostrar_popup("Error", "La fecha es obligatoria.", tipo="error")
            return None
        
        try:
            donacion_id = int(donacion_id) if donacion_id else None
            alimento_preparado_id = int(alimento_preparado_id) if alimento_preparado_id else None
            salon_id = int(salon_id) if salon_id else None
            area_id = int(area_id) if area_id else None
            cantidad = float(cantidad)
            unidad = self.ids.donacion_unidad.text.strip()
            
            # Validación semántica: Si la medida es "Unidad(es)", la cantidad debe ser entera.
            if "Unidad" in unidad and not cantidad.is_integer():
                StyledPopup.mostrar_popup("Error", "Para la medida 'Unidad(es)', la cantidad debe ser un número entero.", tipo="error")
                return None
                
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError as e:
            logger.error(f"⚠️ Error de valor: {e}")
            StyledPopup.mostrar_popup("Error", "Asegúrese de que los IDs y cantidades son numéricos y la fecha es válida.", tipo="error")
            return None
        except Exception as e:
            logger.error(f"⚠️ Error al convertir datos: {e}")
            StyledPopup.mostrar_popup("Error", "Error al procesar los datos del formulario.", tipo="error")
            return None
        return donacion_id, alimento_preparado_id, salon_id, area_id, cantidad, fecha

    def listar_distribuciones(self):
        """Lista todas las distribuciones."""
        logger.debug("Intentando listar distribuciones...")
        try:
            self.controlador.listar_distribuciones()
            logger.info("Distribuciones listadas correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al listar distribuciones: {e}")
            traceback.print_exc()

    def preparar_edicion(self, dist_id):
        """Prepara el formulario para editar una distribución."""
        logger.debug(f"Preparando edición para ID: {dist_id}")
        self.edit_id = dist_id
        try:
            dist = self.controlador.obtener_distribucion(dist_id)
            if dist:
                self.ids.donacion_id.text = str(dist.donacion_id or "")
                self.ids.alimento_preparado_id.text = str(getattr(dist, 'alimento_preparado_id', '') or "")
                self.ids.salon_id.text = str(dist.salon_id or "")
                self.ids.area_id.text = str(dist.area_id or "")
                self.ids.donacion_cantidad.text = str(dist.cantidad)
                self.ids.donacion_unidad.text = str(dist.unidad or "")
                self.ids.fecha.text = str(dist.fecha)
                logger.info(f"Datos de distribución {dist_id} cargados para edición.")
            else:
                StyledPopup.mostrar_popup("Error", "No se pudo encontrar la distribución.", tipo="error")
                self.edit_id = None
        except Exception as e:
            logger.error(f"⚠️ Error al preparar edición: {e}")
            StyledPopup.mostrar_popup("Error", "Error al cargar datos para edición.", tipo="error")
            self.edit_id = None

    def cargar_datos(self, dt):
        """Carga los datos iniciales necesarios para la pantalla."""
        logger.debug("Cargando datos iniciales...")
        try:
            if 'donacion_id' in self.ids:
                self.ids.donacion_id.text = ""
            if 'alimento_preparado_id' in self.ids:
                self.ids.alimento_preparado_id.text = ""
            if 'salon_id' in self.ids:
                self.ids.salon_id.text = ""
            if 'area_id' in self.ids:
                self.ids.area_id.text = ""
            if 'donacion_cantidad' in self.ids:
                self.ids.donacion_cantidad.text = ""
            if 'fecha' in self.ids:
                self.ids.fecha.text = datetime.now().strftime("%Y-%m-%d")
            logger.info("Datos iniciales cargados correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al cargar datos iniciales: {e}")
            traceback.print_exc()

    def abrir_popup_donacion(self):
        """Abre un popup para seleccionar una donación."""
        logger.debug("Obteniendo donaciones para el popup...")
        donaciones = self.controlador.get_db_session().query(Donacion).all() 
        db = self.controlador.get_db_session()
        try:
            donaciones = db.query(Donacion).all()
        except Exception as e:
            StyledPopup.mostrar_popup("Error", f"Error al obtener donaciones: {e}", tipo="error")
            return
        finally:
            db.close()

        if not donaciones:
            StyledPopup.mostrar_popup("Sin Donaciones", "No hay donaciones registradas.", tipo="info")
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        for d in donaciones:
            btn = Button(text=f"ID: {d.id} - {d.descripcion} ({d.cantidad} {d.unidad})", size_hint_y=None, height=40)
            btn.bind(on_press=lambda b, d_id=d.id, d_unid=d.unidad: self._seleccionar_donacion(d_id, d_unid, popup))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        
        close_btn = Button(text="Cerrar", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Seleccionar Donación", content=layout, size_hint=(0.9, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _seleccionar_donacion(self, d_id, d_unid, popup):
        self.ids.donacion_id.text = str(d_id)
        self.ids.alimento_preparado_id.text = ""
        if hasattr(self.ids, 'donacion_unidad'):
            self.ids.donacion_unidad.text = str(d_unid)
        popup.dismiss()

    def abrir_popup_preparado(self):
        """Abre un popup para seleccionar un alimento preparado."""
        db = self.controlador.get_db_session()
        try:
            preparados = db.query(AlimentoPreparado).all()
        except Exception as e:
            StyledPopup.mostrar_popup("Error", f"Error al obtener preparados: {e}", tipo="error")
            return
        finally:
            db.close()

        if not preparados:
            StyledPopup.mostrar_popup("Sin Preparados", "No hay alimentos preparados registrados.", tipo="info")
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        for p in preparados:
            btn = Button(text=f"ID: {p.id} - {p.descripcion} ({p.cantidad} {p.unidad})", size_hint_y=None, height=40)
            btn.bind(on_press=lambda b, p_id=p.id, p_unid=p.unidad: self._seleccionar_preparado(p_id, p_unid, popup))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)

        close_btn = Button(text="Cerrar", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Seleccionar Preparado", content=layout, size_hint=(0.9, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _seleccionar_preparado(self, p_id, p_unid, popup):
        self.ids.alimento_preparado_id.text = str(p_id)
        self.ids.donacion_id.text = ""
        if hasattr(self.ids, 'donacion_unidad'):
            self.ids.donacion_unidad.text = str(p_unid)
        popup.dismiss()

    def abrir_popup_salon(self):
        """Abre un popup para seleccionar un salón."""
        logger.debug("Obteniendo salones para el popup...")
        db = self.controlador.get_db_session()
        try:
            salones = db.query(Salon).all()
        except Exception as e:
            StyledPopup.mostrar_popup("Error", f"Error al obtener salones: {e}", tipo="error")
            return
        finally:
            db.close()

        if not salones:
            StyledPopup.mostrar_popup("Sin Salones", "No hay salones registrados.", tipo="info")
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        for s in salones:
            btn = Button(text=f"ID: {s.id} - {s.salon}", size_hint_y=None, height=40)
            btn.bind(on_press=lambda b, s_id=s.id: self._seleccionar_salon(s_id, popup))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        
        close_btn = Button(text="Cerrar", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Seleccionar Salón", content=layout, size_hint=(0.9, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _seleccionar_salon(self, s_id, popup):
        self.ids.salon_id.text = str(s_id)
        self.ids.area_id.text = ""
        popup.dismiss()

    def abrir_popup_area(self):
        """Abre un popup para seleccionar un área."""
        logger.debug("Obteniendo áreas para el popup...")
        db = self.controlador.get_db_session()
        try:
            areas = db.query(Area).all()
        except Exception as e:
            StyledPopup.mostrar_popup("Error", f"Error al obtener áreas: {e}", tipo="error")
            return
        finally:
            db.close()

        if not areas:
            StyledPopup.mostrar_popup("Sin Áreas", "No hay áreas registradas.", tipo="info")
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        for a in areas:
            btn = Button(text=f"ID: {a.id} - {a.area}", size_hint_y=None, height=40)
            btn.bind(on_press=lambda b, a_id=a.id: self._seleccionar_area(a_id, popup))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)

        close_btn = Button(text="Cerrar", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Seleccionar Área", content=layout, size_hint=(0.9, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _seleccionar_area(self, a_id, popup):
        self.ids.area_id.text = str(a_id)
        self.ids.salon_id.text = ""
        popup.dismiss()

    def guardar_distribucion(self):
        """Guarda una nueva distribución."""
        logger.debug("Intentando guardar una nueva distribución...")
        
        datos_raw = self.obtener_datos_formulario()
        if not datos_raw:
            return

        donacion_id, alimento_preparado_id, salon_id, area_id, cantidad, fecha = datos_raw
        
        datos = {
            "donacion_id": donacion_id,
            "alimento_preparado_id": alimento_preparado_id,
            "salon_id": salon_id,
            "area_id": area_id,
            "cantidad": cantidad,
            "unidad": self.ids.donacion_unidad.text.strip(),
            "fecha": str(fecha)
        }

        if self.edit_id:
            # Modo Edición
            exito, mensaje = self.controlador.actualizar_distribucion(self.edit_id, datos)
        else:
            # Modo Creación
            exito, mensaje = self.controlador.crear_distribucion(datos)

        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.limpiar_formulario()
            # Si veníamos de la lista, volver a ella podría ser bueno, pero por ahora limpiamos.
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def limpiar_formulario(self):
        self.edit_id = None
        self.ids.donacion_id.text = ""
        self.ids.alimento_preparado_id.text = ""
        self.ids.salon_id.text = ""
        self.ids.area_id.text = ""
        self.ids.donacion_cantidad.text = ""
        if hasattr(self.ids, 'donacion_unidad'):
            self.ids.donacion_unidad.text = ""
        self.ids.fecha.text = datetime.now().strftime("%Y-%m-%d")

    