from kivy.uix.screenmanager import Logger, Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.app import App
from components import StyledPopup
from components.styled_datepicker import StyledDatePicker

# Cargar la vista a nivel de módulo para evitar errores de inicialización de IDs
try:
    Builder.load_file('views/aulas.kv')
except Exception as e:
    Logger.error(f"Error cargando views/aulas.kv: {e}")

class AulasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        super().__init__(**kwargs)
        self.controlador = controlador

    def _tiene_permiso(self, codigo):
        app = App.get_running_app()
        return bool(app and app.has_permission(codigo))

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if not app or not app.can_access_screen('aulas'):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para ver Aulas.', tipo='error')
            if app and app.root:
                app.root.current = 'menu'
            return

    def abrir_datepicker(self, target_id):
        """Abre el selector de fecha."""
        def set_date(date_str):
            self.ids[target_id].text = date_str
            
        picker = StyledDatePicker(callback=set_date)
        picker.open()
    def obtener_datos_formulario(self):
        auxiliar = self.ids.aula_auxiliar.text
        capitan = self.ids.aula_capitan.text
        colaborador = self.ids.aula_colaborador.text
        condicion = self.ids.aula_condicion.text
        maestra = self.ids.aula_maestra.text
        ninos = self.ids.aula_ninos.text
        ninas = self.ids.aula_ninas.text
        subcapitan = self.ids.aula_subcapitan.text
        fecha = self.ids.aula_fecha.text
        id_salon = self.ids.aula_id_salon.text

        # Validación básica
        if not auxiliar:
            StyledPopup.mostrar_popup("Error", "El número de auxiliares es obligatorio.", tipo="error")
            return None
        if not capitan:
            StyledPopup.mostrar_popup("Error", "El número de capitanes es obligatorio.", tipo="error")
            return None
        if not colaborador:
            StyledPopup.mostrar_popup("Error", "El número de colaboradores es obligatorio.", tipo="error")
            return None
        if not condicion:
            StyledPopup.mostrar_popup("Error", "La condición es obligatoria.", tipo="error")
            return None
        if not maestra:
            StyledPopup.mostrar_popup("Error", "El número de maestras es obligatorio.", tipo="error")
            return None
        if not ninos:
            StyledPopup.mostrar_popup("Error", "El número de niños es obligatorio.", tipo="error")
            return None
        if not ninas:
            StyledPopup.mostrar_popup("Error", "El número de niñas es obligatorio.", tipo="error")
            return None
        if not subcapitan:
            StyledPopup.mostrar_popup("Error", "El número de subcapitanes es obligatorio.", tipo="error")
            return None
        if not fecha:
            StyledPopup.mostrar_popup("Error", "La fecha es obligatoria.", tipo="error")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Formato de fecha incorrecto. Debe ser YYYY-MM-DD.", tipo="error")
            return None

        try:
            int(auxiliar)
            int(capitan)
            int(colaborador)
            int(id_salon)
            int(maestra)
            int(ninos)
            int(ninas)
            int(subcapitan)
            str(fecha)
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Los campos numéricos deben ser números enteros.", tipo="error")
            return None

        return {
            "auxiliar": int(auxiliar),
            "capitan": int(capitan),
            "colaborador": int(colaborador),
            "condicion": condicion,
            "maestra": int(maestra),
            "ninos": int(ninos),
            "ninas": int(ninas),
            "subcapitan": int(subcapitan),
            "id_salon": int(id_salon),
            "fecha": fecha
        }

    def actualizar_lista_aulas(self, aulas):
        lista_aulas_grid = self.ids.lista_aulas
        lista_aulas_grid.clear_widgets()
        for aula in aulas:
            lista_aulas_grid.add_widget(Label(text=f'Aula {aula.id}'))
            lista_aulas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=aula.id: self.editar_aula(id)))
            lista_aulas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=aula.id: self.controlador.eliminar_aula(id)))

    def editar_aula(self, id):
        aula = self.controlador.obtener_aula(id)
        if aula:
            self.ids.aula_auxiliar.text = str(aula.auxiliar)
            self.ids.aula_capitan.text = str(aula.capitan)
            self.ids.aula_colaborador.text = str(aula.colaborador)
            self.ids.aula_condicion.text = aula.condicion
            self.ids.aula_maestra.text = str(aula.maestra)
            self.ids.aula_ninos.text = str(aula.ninos)
            self.ids.aula_ninas.text = str(aula.ninas)
            self.ids.aula_subcapitan.text = str(aula.subcapitan)
            self.ids.aula_id_salon.text = str(aula.id_salon)
            self.ids.aula_id.text = str(aula.id)
            if hasattr(aula, 'fecha') and aula.fecha:
                self.ids.aula_fecha.text = aula.fecha.strftime('%Y-%m-%d') if hasattr(aula.fecha, 'strftime') else str(aula.fecha)

    def mostrar_popup_salones(self):
        """
        Muestra un popup con la lista de salones obtenidos del controlador para seleccionar uno.
        """
        salones = self.controlador.listar_salones()
        
        # Verificar si no hay salones registrados
        if not salones:
            StyledPopup.mostrar_popup("Sin Salones", "No hay salones registrados.", tipo="info")
            return

        # Crear el contenido del popup
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        scroll_view = ScrollView(size_hint=(1, 0.8))
        salones_grid = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=10)
        salones_grid.bind(minimum_height=salones_grid.setter('height'))

        for salon in salones:
            salon_label = Label(
                text=f"ID: {salon.id} - {salon.salon}",
                size_hint_y=None,
                height=30,
                font_size=18,
                color=(1, 1, 1, 1)
            )
            salones_grid.add_widget(salon_label)

            select_button = Button(
                text="Seleccionar",
                size_hint_y=None,
                height=30,
                font_size=16,
                background_normal='',
                background_color=(0, 119/255, 194/255, 1)
            )
            # Definir el callback para dismiss el popup después de seleccionar
            select_button.bind(on_press=lambda btn, s_id=salon.id: self._finalizar_seleccion_salon(s_id, popup))
            salones_grid.add_widget(select_button)

        scroll_view.add_widget(salones_grid)
        popup_layout.add_widget(scroll_view)

        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.2),
            height=50,
            font_size=18,
            background_normal='',
            background_color=(0, 119/255, 194/255, 1)
        )
        popup_layout.add_widget(close_button)

        popup = Popup(
            title="Seleccionar Salón",
            title_align="center",
            title_size=20,
            content=popup_layout,
            size_hint=(0.8, 0.8),
            background_color=(0.102, 0.2, 0.396, 1)
        )
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def _finalizar_seleccion_salon(self, salon_id, popup):
        self.seleccionar_salon(salon_id)
        popup.dismiss()

    def seleccionar_salon(self, salon_id):
        """
        Asigna el ID del salón seleccionado al campo de entrada correspondiente.
        """
        self.ids.aula_id_salon.text = str(salon_id)
    
    def buscar_aula(self):
        """Obtiene los datos del formulario y llama al método buscar_aula del controlador."""
        aula_id = self.ids.aula_id.text.strip()
        if not aula_id:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID del área.", tipo="error")
            return
        
        if not aula_id.isdigit():
            StyledPopup.mostrar_popup("Error", "El ID debe ser un número entero.", tipo="error")
            return

        exito, aula, mensaje = self.controlador.buscar_aula(id=int(aula_id))
        if exito:
            self.editar_aula(aula.id)
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def crear_aula(self):
        if not self._tiene_permiso('aulas.manage'):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para crear aulas.', tipo='error')
            return
        datos = self.obtener_datos_formulario()
        if datos:
            exito, mensaje = self.controlador.crear_aula(datos)
            if exito:
                StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
                self.limpiar_formulario()
            else:
                StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_aula(self):
        if not self._tiene_permiso('aulas.manage'):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para actualizar aulas.', tipo='error')
            return
        id_texto = self.ids.aula_id.text.strip()
        if not id_texto or not id_texto.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para actualizar.", tipo="error")
            return
        
        datos = self.obtener_datos_formulario()
        if datos:
            exito, mensaje = self.controlador.actualizar_aula(int(id_texto), datos)
            if exito:
                StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
                self.limpiar_formulario()
            else:
                StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_aula(self, aula_id_val):
        if not self._tiene_permiso('aulas.manage'):
            StyledPopup.mostrar_popup('Acceso denegado', 'No tiene permisos para eliminar aulas.', tipo='error')
            return
        if not aula_id_val:
            StyledPopup.mostrar_popup("Error", "ID de aula no válido.", tipo="error")
            return
            
        exito, mensaje = self.controlador.eliminar_aula(int(aula_id_val))
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.controlador.listar_aulas() # Actualiza la lista si estamos en la vista de lista
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def limpiar_formulario(self):
        self.ids.aula_id.text = ""
        self.ids.aula_auxiliar.text = ""
        self.ids.aula_capitan.text = ""
        self.ids.aula_colaborador.text = ""
        self.ids.aula_condicion.text = ""
        self.ids.aula_maestra.text = ""
        self.ids.aula_ninos.text = ""
        self.ids.aula_ninas.text = ""
        self.ids.aula_subcapitan.text = ""
        self.ids.aula_fecha.text = ""
        self.ids.aula_id_salon.text = ""