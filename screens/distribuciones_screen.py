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
        logger.debug("Abriendo popup para seleccionar donación...")
        try:
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
            layout.add_widget(Label(text="Seleccionar Donación"))
            close_button = Button(text="Cerrar", size_hint_y=None, height=50)
            close_button.bind(on_press=lambda *args: popup.dismiss())
            popup = Popup(title="Seleccionar Donación", content=layout, size_hint=(0.8, 0.8))
            popup.open()
            logger.info("Popup de selección de donación abierto correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al abrir popup de donación: {e}")
            traceback.print_exc()

    def abrir_popup_salon(self):
        """Abre un popup para seleccionar un salón."""
        logger.debug("Abriendo popup para seleccionar salón...")
        try:
            layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
            layout.add_widget(Label(text="Seleccionar Salón"))
            close_button = Button(text="Cerrar", size_hint_y=None, height=50)
            close_button.bind(on_press=lambda *args: popup.dismiss())
            popup = Popup(title="Seleccionar Salón", content=layout, size_hint=(0.8, 0.8))
            popup.open()
            logger.info("Popup de selección de salón abierto correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al abrir popup de salón: {e}")
            traceback.print_exc()

    def guardar_distribucion(self):
        """Guarda una nueva distribución."""
        logger.debug("Intentando guardar una nueva distribución...")
        try:
            datos = {
                "donacion_id": self.ids.donacion_id.text.strip(),
                "salon_id": self.ids.salon_id.text.strip(),
                "cantidad": self.ids.donacion_cantidad.text.strip(),
                "fecha": self.ids.fecha.text.strip()
            }

            # Validar datos
            if not datos["donacion_id"] or not datos["salon_id"] or not datos["cantidad"] or not datos["fecha"]:
                logger.warning("Faltan datos obligatorios en el formulario.")
                StyledPopup.mostrar_popup("Error", "Todos los campos son obligatorios.", tipo="error")
                return

            try:
                datos["donacion_id"] = int(datos["donacion_id"])
                datos["salon_id"] = int(datos["salon_id"])
                datos["cantidad"] = float(datos["cantidad"])
                datos["fecha"] = datetime.strptime(datos["fecha"], "%Y-%m-%d").date()
            except ValueError as e:
                logger.error(f"Error al convertir datos: {e}")
                StyledPopup.mostrar_popup("Error", "ID de donación, ID de salón y cantidad deben ser números válidos.", tipo="error")
                return

            # Llamar al controlador para guardar la distribución
            logger.info(f"Datos validados correctamente: {datos}")
            self.controlador.crear_distribucion(datos)
            logger.info("Distribución guardada correctamente.")
        except Exception as e:
            logger.error(f"⚠️ Error al guardar distribución: {e}")
            traceback.print_exc()

    