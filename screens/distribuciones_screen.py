import logging
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from components.styled_popup import StyledPopup
from datetime import datetime
import traceback

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)  # Cambiar a DEBUG para mayor detalle
logger = logging.getLogger(__name__)

from models.donaciones import Donacion
from models.salones import Salon

class DistribucionesScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            logger.debug("Cargando archivo distribucion.kv...")
            Builder.load_file('views/distribucion.kv')
        except Exception as e:
            logger.error(f"⚠️ Error al cargar distribucion.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador
        logger.info("DistribucionesScreen inicializado correctamente.")

    def on_pre_enter(self, *args):
        """Se ejecuta antes de que la pantalla sea visible."""
        logger.debug("Ejecutando on_pre_enter...")
        Clock.schedule_once(self.cargar_datos, 1)
    
    def obtener_datos_formulario(self):
        donacion_id = self.ids.donacion_id.text.strip()
        salon_id = self.ids.salon_id.text.strip()
        cantidad = self.ids.donacion_cantidad.text.strip()
        fecha = self.ids.fecha.text.strip()

        #Validación básica
        if not donacion_id:
            StyledPopup.mostrar_popup("Error", "El ID de donación es obligatorio.", tipo="error")
            return None
        if not salon_id:
            StyledPopup.mostrar_popup("Error", "El ID de salón es obligatorio.", tipo="error")
            return None
        if not cantidad:
            StyledPopup.mostrar_popup("Error", "La cantidad es obligatoria.", tipo="error")
            return None
        if not fecha:
            StyledPopup.mostrar_popup("Error", "La fecha es obligatoria.", tipo="error")
            return None
        
        try:
            donacion_id = int(donacion_id)
            salon_id = int(salon_id)
            cantidad = float(cantidad)
            fecha = datetime.strptime(fecha, "%Y-%m-%d").date()
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Formato de fecha incorrecto. Debe ser YYYY-MM-DD.", tipo="error")
            return None
        except Exception as e:
            logger.error(f"⚠️ Error al convertir datos: {e}")
            StyledPopup.mostrar_popup("Error", "Error al procesar los datos del formulario.", tipo="error")
            return None
        return donacion_id, salon_id, cantidad, fecha

    def listar_distribuciones(self):
        """Lista todas las distribuciones."""
        logger.debug("Intentando listar distribuciones...")
        try:
            self.controlador.listar_distribuciones()
            logger.info("Distribuciones listadas correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al listar distribuciones: {e}")
            traceback.print_exc()

    def editar_distribucion(self):
        """Edita una distribución existente."""
        logger.debug("Intentando editar distribución...")
        try:
            datos = self.obtener_datos_formulario()
            if datos:
                self.controlador.editar_distribucion(datos)
                logger.info("Distribución editada correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al editar distribución: {e}")
            traceback.print_exc()

    def cargar_datos(self, dt):
        """Carga los datos iniciales necesarios para la pantalla."""
        logger.debug("Cargando datos iniciales...")
        try:
            self.ids.donacion_id.text = ""
            self.ids.salon_id.text = ""
            self.ids.donacion_cantidad.text = ""
            self.ids.fecha.text = datetime.now().strftime("%Y-%m-%d")
            logger.info("Datos iniciales cargados correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al cargar datos iniciales: {e}")
            traceback.print_exc()

    def abrir_popup_donacion(self):
        """Abre un popup para seleccionar una donación."""
        logger.debug("Obteniendo donaciones para el popup...")
        donaciones = self.controlador.get_db_session().query(Donacion).all() # Usar el controlador sería mejor, pero el controlador no tiene listar_donaciones, DonacionesController sí.
        # En una arquitectura MVC pura, DistribucionesController debería tener acceso o app.py debería proveerlo.
        # Como DistribucionesController no tiene listar_donaciones, y queremos evitar tocar mucho los controladores ahora:
        # Pero espera, DistribucionesController hereda de BaseController.
        
        # Vamos a usar el método del controlador si existe, si no, lo hacemos aquí pero idealmente a través del controlador.
        # En este caso, el usuario quiere MVC, así que el controlador de distribuciones DEBERÍA poder proveer donaciones o usamos el de donaciones.
        
        # Para ser consistentes con AulasScreen:
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
        if hasattr(self.ids, 'donacion_unidad'):
            self.ids.donacion_unidad.text = str(d_unid)
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
        popup.dismiss()

    def guardar_distribucion(self):
        """Guarda una nueva distribución."""
        logger.debug("Intentando guardar una nueva distribución...")
        
        datos_raw = self.obtener_datos_formulario()
        if not datos_raw:
            return

        donacion_id, salon_id, cantidad, fecha = datos_raw
        
        datos = {
            "donacion_id": donacion_id,
            "salon_id": salon_id,
            "cantidad": cantidad,
            "fecha": str(fecha)
        }

        exito, mensaje = self.controlador.crear_distribucion(datos)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.limpiar_formulario()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def limpiar_formulario(self):
        self.ids.donacion_id.text = ""
        self.ids.salon_id.text = ""
        self.ids.donacion_cantidad.text = ""
        if hasattr(self.ids, 'donacion_unidad'):
            self.ids.donacion_unidad.text = ""
        self.ids.fecha.text = datetime.now().strftime("%Y-%m-%d")

    