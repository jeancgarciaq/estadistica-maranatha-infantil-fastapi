from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.lang import Builder

class ListSalonesScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/list_salones.kv')
        super().__init__(**kwargs)
        self.controlador = controlador
        self.cargar_salones()

    def on_pre_enter(self):
        self.cargar_salones()

    def cargar_salones(self):
        lista_salones_grid = self.ids.lista_salones
        lista_salones_grid.clear_widgets()
        salones = self.controlador.obtener_todos_los_salones()
        if not salones:
            lista_salones_grid.add_widget(Label(text="No hay salones disponibles.", size_hint_y=None, height=40))
        else:
            for salon in salones:
                lista_salones_grid.add_widget(Label(text=f"{salon.salon} ({salon.edad})", size_hint_y=None, height=40))