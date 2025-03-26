import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers import DistribucionesController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import traceback

class DistribucionesScreen(Screen):

    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/distribucion.kv')
        except Exception as e:
            print(f"⚠️ Error al cargar distribucion.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.cargar_donaciones, 1)  # 📌 Esperar a que Kivy termine de cargar

    def cargar_donaciones(self, dt):
        if not self.ids:
            Clock.schedule_once(self.cargar_donaciones, 0.1)
            return
        print("Contenido de self.ids:", self.ids)
        if 'donacion_spinner' not in self.ids:
            print("⚠️ Error: 'donacion_spinner' no está en self.ids. Verifica el archivo KV.")
            return #Añadido
        if 'salones_seleccionados' not in self.ids:
            print("⚠️ Error: 'salones_seleccionados' no está en self.ids. Verifica el archivo KV.")
            return #Añadido
        donaciones = self.controlador.listar_donaciones()
        self.ids.donacion_spinner.values = [donacion.descripcion for donacion in donaciones]
        salones = self.controlador.obtener_salones()
        self.actualizar_salones(salones)
        self.actualizar_lista_distribuciones()

    def actualizar_salones(self, salones):
        self.ids.salones_seleccionados.clear_widgets()
        for salon in salones:
            checkbox = CheckBox(active=False)
            label = Label(text=salon.nombre)
            cantidad_input = TextInput(hint_text='Cantidad', input_type='float')
            unidad_input = TextInput(hint_text='Unidad')
            box_layout = BoxLayout(orientation='horizontal')
            box_layout.add_widget(checkbox)
            box_layout.add_widget(label)
            box_layout.add_widget(cantidad_input)
            box_layout.add_widget(unidad_input)
            self.ids.salones_seleccionados.add_widget(box_layout)

    def obtener_salones_seleccionados(self):
        salones_distribucion = []
        for box_layout in self.ids.salones_seleccionados.children:
            checkbox = box_layout.children[3]
            label = box_layout.children[2]
            cantidad_input = box_layout.children[1]
            unidad_input = box_layout.children[0]
            if checkbox.active:
                salones_distribucion.append((label.text, float(cantidad_input.text), unidad_input.text))
        return salones_distribucion

    def obtener_donacion_seleccionada(self):
        return self.ids.donacion_spinner.text

    def registrar_distribucion(self):
        donacion_id = self.obtener_donacion_seleccionada()
        salones_distribucion = self.obtener_salones_seleccionados()
        self.controlador.registrar_distribucion(donacion_id, salones_distribucion)
        self.actualizar_lista_distribuciones()

    def actualizar_lista_distribuciones(self):
        distribuciones = self.controlador.listar_distribuciones()
        self.ids.lista_distribuciones.clear_widgets()
        for distribucion in distribuciones:
            self.ids.lista_distribuciones.add_widget(Label(text=distribucion.donacion.descripcion))
            self.ids.lista_distribuciones.add_widget(Label(text=distribucion.salon.nombre))
            self.ids.lista_distribuciones.add_widget(Label(text=str(distribucion.cantidad)))
            self.ids.lista_distribuciones.add_widget(Label(text=distribucion.unidad))

    def mostrar_popup_lista(self):
        distribuciones = self.controlador.listar_distribuciones()

        content = ScrollView(
            GridLayout(
                cols=4,
                size_hint_y=None,
                height=self.minimum_height,
                id='lista_distribuciones_popup'
            )
        )

        for distribucion in distribuciones:
            content.children[0].add_widget(Label(text=distribucion.donacion.descripcion))
            content.children[0].add_widget(Label(text=distribucion.salon.nombre))
            content.children[0].add_widget(Label(text=str(distribucion.cantidad)))
            content.children[0].add_widget(Label(text=distribucion.unidad))

        close_button = Button(text='Cerrar', size_hint_y=None, height=50)

        popup = Popup(title='Lista de Distribuciones', content=BoxLayout(orientation='vertical'), size_hint=(None, None), size=(600, 400))
        popup.content.add_widget(content)
        popup.content.add_widget(close_button)

        close_button.bind(on_press=popup.dismiss)
        popup.open()