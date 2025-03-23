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