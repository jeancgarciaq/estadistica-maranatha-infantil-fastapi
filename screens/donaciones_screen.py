import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers import DonacionesController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox

class DonacionesScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/donaciones.kv')
        super().__init__(**kwargs)
        self.controlador = DonacionesController(self)

    def obtener_datos_formulario(self):
        descripcion = self.ids.donacion_descripcion.text
        cantidad = self.ids.donacion_cantidad.text
        unidad = self.ids.donacion_unidad.text
        fecha = self.ids.donacion_fecha.text
        equipo = self.ids.donacion_equipo.text

        # Validación básica
        if not descripcion:
            self.mostrar_error("La descripción es obligatoria.")
            return None
        if not cantidad:
            self.mostrar_error("La cantidad es obligatoria.")
            return None
        try:
            float(cantidad)
        except ValueError:
            self.mostrar_error("La cantidad debe ser un número.")
            return None
        if not unidad:
            self.mostrar_error("La unidad es obligatoria.")
            return None
        if not equipo:
            self.mostrar_error("El equipo es obligatorio.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
            return None

        return {
            "descripcion": descripcion,
            "cantidad": cantidad,
            "unidad": unidad,
            "equipo": equipo,
            "fecha": fecha
        }

    def crear_donacion(self):
        datos = self.obtener_datos_formulario()
        self.controlador.crear_donacion(datos["cantidad"], datos["descripcion"], datos["unidad"], datos["fecha"], datos["equipo"], self.obtener_salones_seleccionados())

    def actualizar_donacion(self):
        datos = self.obtener_datos_formulario()
        self.controlador.actualizar_donacion(self.ids.donacion_id.text, datos["cantidad"], datos["descripcion"], datos["unidad"], datos["fecha"], datos["equipo"], self.obtener_salones_seleccionados())

    def eliminar_donacion(self):
        self.controlador.eliminar_donacion(self.ids.donacion_id.text)

    def listar_donaciones(self):
        self.controlador.listar_donaciones()

    def mostrar_popup_lista(self):
        donaciones = self.controlador.listar_donaciones()  # Obtener la lista de donaciones desde el controlador

        # Crear el contenido del popup (lista de donaciones)
        content = ScrollView(
            GridLayout(
                cols=5,
                size_hint_y=None,
                height=self.minimum_height,
                id='lista_donaciones'
            )
        )

        for donacion in donaciones:
            content.children[0].add_widget(Label(text=str(donacion.id)))
            content.children[0].add_widget(Label(text=donacion.descripcion))
            content.children[0].add_widget(Label(text=str(donacion.cantidad)))
            content.children[0].add_widget(Label(text=str(donacion.fecha)))
            content.children[0].add_widget(Label(text=donacion.equipo))
            content.children[0].add_widget(Label(text=donacion.fecha))
            

        # Crear el botón de cerrar
        close_button = Button(text='Cerrar', size_hint_y=None, height=50)

        # Crear el popup
        popup = Popup(title='Lista de Donaciones', content=BoxLayout(orientation='vertical'), size_hint=(None, None), size=(400, 400))
        popup.content.add_widget(content)
        popup.content.add_widget(close_button)

        # Asignar la función de cierre al botón
        close_button.bind(on_press=popup.dismiss)

        # Mostrar el popup
        popup.open()

    def actualizar_lista_donaciones(self, donaciones):
        self.ids.lista_donaciones.clear_widgets()
        for donacion in donaciones:
            self.ids.lista_donaciones.add_widget(Label(text=str(donacion.id)))
            self.ids.lista_donaciones.add_widget(Label(text=donacion.descripcion))
            editar_btn = Button(text='Editar')
            editar_btn.donacion = donacion
            editar_btn.bind(on_press=self.cargar_donacion_editar)
            self.ids.lista_donaciones.add_widget(editar_btn)

    def cargar_donacion_editar(self, instance):
        donacion = instance.donacion
        self.ids.donacion_id.text = str(donacion.id)
        self.ids.donacion_descripcion.text = donacion.descripcion
        self.ids.donacion_cantidad.text = str(donacion.cantidad)
        self.ids.donacion_unidad.text = donacion.unidad
        self.ids.donacion_equipo.text = donacion.equipo
        self.ids.donacion_fecha.text = donacion.fecha.strftime('%Y-%m-%d')
        self.cargar_salones_seleccionados(donacion.salones)

    def obtener_salones_seleccionados(self):
        salones_seleccionados = []
        for child in self.ids.salones_seleccionados.children:
            if isinstance(child, CheckBox) and child.active:
                salones_seleccionados.append(int(child.text.split('-')[0]))
        return salones_seleccionados

    def cargar_salones(self):
        self.ids.salones_seleccionados.clear_widgets()
        salones = self.controlador.obtener_salones()
        for salon in salones:
            checkbox = CheckBox(text=f"{salon.id}-{salon.nombre}")
            self.ids.salones_seleccionados.add_widget(checkbox)

    def cargar_salones_seleccionados(self, salones):
        for child in self.ids.salones_seleccionados.children:
            if isinstance(child, CheckBox):
                salon_id = int(child.text.split('-')[0])
                if any(s.id == salon_id for s in salones):
                    child.active = True

    def actualizar_salones(self, salones):
        # Limpiar el GridLayout antes de agregar nuevos CheckBoxes
        self.ids.salones_seleccionados.clear_widgets()

        for salon in salones:
            checkbox = CheckBox(active=False)  
            label = Label(text=salon.salon)  
            box_layout = BoxLayout(orientation='horizontal')
            box_layout.add_widget(checkbox)
            box_layout.add_widget(label)
            self.ids.salones_seleccionados.add_widget(box_layout)

    def obtener_salones_seleccionados(self):
        salones_seleccionados = []
        for box_layout in self.ids.salones_seleccionados.children:
            checkbox = box_layout.children[1]  
            label = box_layout.children[0]  
            if checkbox.active:
                salones_seleccionados.append(label.text)
        return salones_seleccionados

    # Función para mostrar los salones
    def mostrar_salones(self):
        # Obtener la lista de salones desde el controlador
        salones = self.controlador.obtener_salones()
        # Llamar a la función para actualizar los salones
        self.actualizar_salones(salones)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()
