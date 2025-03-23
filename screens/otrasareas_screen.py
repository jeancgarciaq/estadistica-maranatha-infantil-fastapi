import kivy
kivy.require('2.3.1')

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from controllers import OtrasAreasController
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class OtrasAreasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        Builder.load_file('views/otras_areas.kv')
        super().__init__(**kwargs)
        self.controlador = OtrasAreasController(self)

    def obtener_datos_formulario(self):
        alabanza = self.ids.otrasareas_alabanza.text
        fecha = self.ids.otrasareas_fecha.text
        protocolo = self.ids.otrasareas_protocolo.text
        semillitas = self.ids.otrasareas_semillitas.text
        sonido = self.ids.otrasareas_sonido.text
        teatro = self.ids.otrasareas_teatro.text
        tv = self.ids.otrasareas_tv.text
        ujier = self.ids.otrasareas_ujier.text
        fecha = self.ids.otrasareas_fecha.text

        # Validación básica
        if not alabanza:
            self.mostrar_error("El número de alabanzas es obligatorio.")
            return None
        if not fecha:
            self.mostrar_error("La fecha es obligatoria.")
            return None
        if not protocolo:
            self.mostrar_error("El número de protocolos es obligatorio.")
            return None
        if not semillitas:
            self.mostrar_error("El número de semillitas es obligatorio.")
            return None
        if not sonido:
            self.mostrar_error("El número de sonidos es obligatorio.")
            return None
        if not teatro:
            self.mostrar_error("El número de teatros es obligatorio.")
            return None
        if not tv:
            self.mostrar_error("El número de tvs es obligatorio.")
            return None
        if not ujier:
            self.mostrar_error("El número de ujieres es obligatorio.")
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
            int(alabanza)
            int(protocolo)
            int(semillitas)
            int(sonido)
            int(teatro)
            int(tv)
            int(ujier)
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            self.mostrar_error("Los campos numéricos deben ser números enteros y la fecha debe tener el formato AAAA-MM-DD.")
            return None

        return {
            "alabanza": int(alabanza),
            "fecha": fecha,
            "protocolo": int(protocolo),
            "semillitas": int(semillitas),
            "sonido": int(sonido),
            "teatro": int(teatro),
            "tv": int(tv),
            "ujier": int(ujier),
            "fecha": fecha
        }
    
    def actualizar_lista_otrasareas(self, otrasareas):
        lista_otrasareas_grid = self.ids.lista_otrasareas
        lista_otrasareas_grid.clear_widgets()
        for otrasarea in otrasareas:
            lista_otrasareas_grid.add_widget(Label(text=f'Otras áreas {otrasarea.id}'))
            lista_otrasareas_grid.add_widget(Button(text="Editar", on_press=lambda *args, id=otrasarea.id: self.editar_otrasareas(id)))
            lista_otrasareas_grid.add_widget(Button(text="Eliminar", on_press=lambda *args, id=otrasarea.id: self.controlador.eliminar_otrasareas(id)))

    def editar_otrasareas(self, id):
        otrasarea = self.controlador.obtener_otrasareas(id)
        if otrasarea:
            self.ids.otrasareas_alabanza.text = str(otrasarea.alabanza)
            self.ids.otrasareas_fecha.text = str(otrasarea.fecha)
            self.ids.otrasareas_protocolo.text = str(otrasarea.protocolo)
            self.ids.otrasareas_semillitas.text = str(otrasarea.semillitas)
            self.ids.otrasareas_sonido.text = str(otrasarea.sonido)
            self.ids.otrasareas_teatro.text = str(otrasarea.teatro)
            self.ids.otrasareas_tv.text = str(otrasarea.tv)
            self.ids.otrasareas_ujier.text = str(otrasarea.ujier)
            self.ids.otrasareas_id.text = str(otrasarea.id)

    def mostrar_error(self, mensaje):
        popup = Popup(title='Error', content=Label(text=mensaje), size_hint=(None, None), size=(400, 200))
        popup.open()