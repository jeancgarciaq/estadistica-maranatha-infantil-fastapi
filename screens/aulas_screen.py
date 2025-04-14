import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers import AulasController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from models.salones import Salon

class AulasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/aulas.kv')
        super().__init__(**kwargs)
        self.controlador = AulasController(self)
    
    def obtener_datos_formulario(self):
        auxiliar = self.ids.aula_auxiliar.text
        capitan = self.ids.aula_capitan.text
        colaborador = self.ids.aula_colaborador.text
        condicion = self.ids.aula_condicion.text
        edad = self.ids.aula_edad.text
        maestra = self.ids.aula_maestra.text
        ninos = self.ids.aula_ninos.text
        ninas = self.ids.aula_ninas.text
        subcapitan = self.ids.aula_subcapitan.text
        fecha = self.ids.aula_fecha.text
        id_salon = self.ids.aula_id_salon.text

        # Validación básica
        if not auxiliar:
            self.mostrar_error("El número de auxiliares es obligatorio.")
            return None
        if not capitan:
            self.mostrar_error("El número de capitanes es obligatorio.")
            return None
        if not colaborador:
            self.mostrar_error("El número de colaboradores es obligatorio.")
            return None
        if not condicion:
            self.mostrar_error("La condición es obligatoria.")
            return None
        if not edad:
            self.mostrar_error("La edad es obligatoria.")
            return None
        if not maestra:
            self.mostrar_error("El número de maestras es obligatorio.")
            return None
        if not ninos:
            self.mostrar_error("El número de niños es obligatorio.")
            return None
        if not ninas:
            self.mostrar_error("El número de niñas es obligatorio.")
            return None
        if not subcapitan:
            self.mostrar_error("El número de subcapitanes es obligatorio.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Formato de fecha incorrecto. Debe ser YYYY-MM-DD.")
            return None

        try:
            int(auxiliar)
            int(capitan)
            int(colaborador)
            int(maestra)
            int(ninos)
            int(ninas)
            int(subcapitan)
        except ValueError:
            self.mostrar_error("Los campos numéricos deben ser números enteros.")
            return None

        return {
            "auxiliar": int(auxiliar),
            "capitan": int(capitan),
            "colaborador": int(colaborador),
            "condicion": condicion,
            "edad": edad,
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
            self.ids.aula_edad.text = aula.edad
            self.ids.aula_maestra.text = str(aula.maestra)
            self.ids.aula_ninos.text = str(aula.ninos)
            self.ids.aula_ninas.text = str(aula.ninas)
            self.ids.aula_subcapitan.text = str(aula.subcapitan)
            self.ids.aula_id_salon.text = str(aula.id_salon)
            self.ids.aula_id.text = str(aula.id)

    def mostrar_popup_lista(self):
        aulas = self.controlador.listar_aulas()  # Obtener la lista de aulas desde el controlador

        # Crear el contenido del popup (lista de aulas)
        content = ScrollView(
            GridLayout(
                cols=10,
                size_hint_y=None,
                height=self.minimum_height,
                id='lista_aulas_popup'
            )
        )

        for aula in aulas:
            content.children[0].add_widget(Label(text=str(aula.id)))
            content.children[0].add_widget(Label(text=str(aula.auxiliar)))
            content.children[0].add_widget(Label(text=str(aula.capitan)))
            content.children[0].add_widget(Label(text=str(aula.colaborador)))
            content.children[0].add_widget(Label(text=aula.condicion))
            content.children[0].add_widget(Label(text=aula.edad))
            content.children[0].add_widget(Label(text=str(aula.maestra)))
            content.children[0].add_widget(Label(text=str(aula.ninos)))
            content.children[0].add_widget(Label(text=str(aula.ninas)))
            content.children[0].add_widget(Label(text=str(aula.subcapitan)))
            content.children[0].add_widget(Label(text=str(aula.fecha)))
            

        # Crear el botón de cerrar
        close_button = Button(text='Cerrar', size_hint_y=None, height=50)

        # Crear el popup
        popup = Popup(title='Lista de Aulas', content=BoxLayout(orientation='vertical'), size_hint=(None, None), size=(400, 400))
        popup.content.add_widget(content)
        popup.content.add_widget(close_button)

        # Asignar la función de cierre al botón
        close_button.bind(on_press=popup.dismiss)

        # Mostrar el popup
        popup.open()

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()   

    def mostrar_popup_salones(self):
        db = self.controlador.get_db_session()
        try:
            salones = db.query(Salon).all()
        except Exception as e:
            self.mostrar_error(f"Error al obtener salones: {e}")
            return
        finally:
            db.close()

        # Crear el contenido del popup
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        scroll_view = ScrollView(size_hint=(1, 0.8))
        salones_grid = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=10)
        salones_grid.bind(minimum_height=salones_grid.setter('height'))

        for salon in salones:
            # Estilo para las etiquetas
            salon_label = Label(
                text=f"ID: {salon.id} - {salon.salon}",
                size_hint_y=None,
                height=30,
                font_size=18,
                color=(1, 1, 1, 1)  # Texto blanco
            )
            salones_grid.add_widget(salon_label)

            # Estilo para los botones
            select_button = Button(
                text="Seleccionar",
                size_hint_y=None,
                height=30,
                font_size=16,
                background_normal='',
                background_color=(0, 119/255, 194/255, 1)  # Azul consistente con el estilo
            )
            select_button.bind(on_press=lambda btn, salon_id=salon.id: self.seleccionar_salon(salon_id))
            salones_grid.add_widget(select_button)

        scroll_view.add_widget(salones_grid)
        popup_layout.add_widget(scroll_view)

        # Botón de cerrar con estilo
        close_button = Button(
            text="Cerrar",
            size_hint=(1, 0.2),
            height=50,
            font_size=18,
            background_normal='',
            background_color=(0, 119/255, 194/255, 1)  # Azul consistente con el estilo
        )
        close_button.bind(on_press=lambda *args: popup.dismiss())
        popup_layout.add_widget(close_button)

        # Crear el popup con estilo consistente
        popup = Popup(
            title="Seleccionar Salón",
            title_align="center",
            title_size=20,
            title_color=(1, 1, 1, 1),  # Título en blanco
            content=popup_layout,
            size_hint=(0.8, 0.8),
            background_color=(0.102, 0.2, 0.396, 1)  # Fondo azul oscuro
        )
        popup.open()

    def seleccionar_salon(self, salon_id):
        self.ids.aula_id_salon.text = str(salon_id)