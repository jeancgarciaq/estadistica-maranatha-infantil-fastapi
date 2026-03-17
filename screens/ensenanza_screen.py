from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime
from components.styled_popup import StyledPopup


class EnsenanzaScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/ensenanza.kv')
        except Exception as e:
            print(f"Error cargando ensenanza.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def obtener_datos_formulario(self):
        capitan = self.ids.ensenanza_capitan.text.strip()
        subcapitan = self.ids.ensenanza_subcapitan.text.strip()
        fecha = self.ids.ensenanza_fecha.text.strip()

        if not capitan:
            StyledPopup.mostrar_popup("Error", "El nombre del capitán es obligatorio.", tipo="error")
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
            int(subcapitan)
        except ValueError:
            StyledPopup.mostrar_popup("Error", "El número de subcapitanes debe ser un entero.", tipo="error")
            return None

        return {
            "capitan": capitan,
            "subcapitan": int(subcapitan),
            "fecha": fecha
        }

    def _limpiar_campos(self):
        self.ids.ensenanza_capitan.text = ""
        self.ids.ensenanza_subcapitan.text = ""
        self.ids.ensenanza_fecha.text = ""
        if hasattr(self.ids, 'ensenanza_id'):
            self.ids.ensenanza_id.text = ""

    def crear_ensenanza(self):
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.crear_ensenanza(
            datos["capitan"], datos["fecha"], datos["subcapitan"]
        )
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_ensenanzas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_ensenanza(self):
        ensenanza_id = self.ids.ensenanza_id.text.strip() if hasattr(self.ids, 'ensenanza_id') else ""
        if not ensenanza_id or not ensenanza_id.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para actualizar.", tipo="error")
            return
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.actualizar_ensenanza(
            int(ensenanza_id), datos["capitan"], datos["subcapitan"], datos["fecha"]
        )
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_ensenanzas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_ensenanza(self, id):
        exito, mensaje = self.controlador.eliminar_ensenanza(id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_ensenanzas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def cargar_ensenanzas(self):
        ensenanzas = self.controlador.listar_ensenanzas()
        self.actualizar_lista_ensenanzas(ensenanzas)

    def actualizar_lista_ensenanzas(self, ensenanzas):
        lista_grid = self.ids.lista_ensenanzas
        lista_grid.clear_widgets()
        if not ensenanzas:
            lista_grid.add_widget(Label(text="No hay enseñanzas registradas", size_hint_y=None, height=40))
            return
        for ensenanza in ensenanzas:
            lista_grid.add_widget(Label(text=f"ID: {ensenanza.id} | {ensenanza.capitan} | {ensenanza.fecha}", size_hint_y=None, height=40))
            lista_grid.add_widget(Button(text="Editar", size_hint_y=None, height=40,
                                         on_press=lambda *a, id=ensenanza.id: self.editar_ensenanza(id)))
            lista_grid.add_widget(Button(text="Eliminar", size_hint_y=None, height=40,
                                          on_press=lambda *a, id=ensenanza.id: self.eliminar_ensenanza(id)))

    def editar_ensenanza(self, id):
        ensenanza = self.controlador.obtener_ensenanza(id)
        if ensenanza:
            self.ids.ensenanza_capitan.text = ensenanza.capitan
            self.ids.ensenanza_fecha.text = str(ensenanza.fecha)
            self.ids.ensenanza_subcapitan.text = str(ensenanza.subcapitan)
            if hasattr(self.ids, 'ensenanza_id'):
                self.ids.ensenanza_id.text = str(ensenanza.id)
        else:
            StyledPopup.mostrar_popup("Error", "Enseñanza no encontrada.", tipo="error")

    def on_enter(self):
        self.cargar_ensenanzas()