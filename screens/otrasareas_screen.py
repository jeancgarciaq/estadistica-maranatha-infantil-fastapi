from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime
from components.styled_popup import StyledPopup


class OtrasAreasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/otras_areas.kv')
        except Exception as e:
            print(f"Error cargando otras_areas.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def obtener_datos_formulario(self):
        alabanza = self.ids.otrasareas_alabanza.text.strip()
        protocolo = self.ids.otrasareas_protocolo.text.strip()
        semillitas = self.ids.otrasareas_semillitas.text.strip()
        sonido = self.ids.otrasareas_sonido.text.strip()
        teatro = self.ids.otrasareas_teatro.text.strip()
        tv = self.ids.otrasareas_tv.text.strip()
        ujier = self.ids.otrasareas_ujier.text.strip()
        fecha = self.ids.otrasareas_fecha.text.strip()

        campos = {
            "alabanza": alabanza, "protocolo": protocolo,
            "semillitas": semillitas, "sonido": sonido,
            "teatro": teatro, "tv": tv, "ujier": ujier, "fecha": fecha
        }
        for nombre, valor in campos.items():
            if not valor:
                StyledPopup.mostrar_popup("Error", f"El campo '{nombre}' es obligatorio.", tipo="error")
                return None

        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Formato de fecha incorrecto. Debe ser YYYY-MM-DD.", tipo="error")
            return None

        try:
            return {
                "alabanza": int(alabanza),
                "protocolo": int(protocolo),
                "semillitas": int(semillitas),
                "sonido": int(sonido),
                "teatro": int(teatro),
                "tv": int(tv),
                "ujier": int(ujier),
                "fecha": fecha
            }
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Los campos numéricos deben ser números enteros.", tipo="error")
            return None

    def _limpiar_campos(self):
        for campo in ['otrasareas_alabanza', 'otrasareas_protocolo', 'otrasareas_semillitas',
                      'otrasareas_sonido', 'otrasareas_teatro', 'otrasareas_tv',
                      'otrasareas_ujier', 'otrasareas_fecha']:
            if hasattr(self.ids, campo):
                getattr(self.ids, campo).text = ""
        if hasattr(self.ids, 'otrasareas_id'):
            self.ids.otrasareas_id.text = ""

    def crear_otrasareas(self):
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.crear_otrasareas(
            datos["alabanza"], datos["protocolo"], datos["semillitas"],
            datos["sonido"], datos["teatro"], datos["tv"], datos["ujier"], datos["fecha"]
        )
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_otrasareas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_otrasareas(self):
        otrasareas_id = self.ids.otrasareas_id.text.strip() if hasattr(self.ids, 'otrasareas_id') else ""
        if not otrasareas_id or not otrasareas_id.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para actualizar.", tipo="error")
            return
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.actualizar_otrasareas(
            int(otrasareas_id), datos["alabanza"], datos["protocolo"], datos["semillitas"],
            datos["sonido"], datos["teatro"], datos["tv"], datos["ujier"], datos["fecha"]
        )
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_otrasareas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_otrasareas(self, id):
        exito, mensaje = self.controlador.eliminar_otrasareas(id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_otrasareas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def cargar_otrasareas(self):
        otrasareas = self.controlador.listar_otrasareas()
        self.actualizar_lista_otrasareas(otrasareas)

    def actualizar_lista_otrasareas(self, otrasareas):
        lista_grid = self.ids.lista_otrasareas
        lista_grid.clear_widgets()
        if not otrasareas:
            lista_grid.add_widget(Label(text="No hay registros de otras áreas", size_hint_y=None, height=40))
            return
        for otrasarea in otrasareas:
            lista_grid.add_widget(Label(text=f"ID: {otrasarea.id} | Fecha: {otrasarea.fecha}", size_hint_y=None, height=40))
            lista_grid.add_widget(Button(text="Editar", size_hint_y=None, height=40,
                                          on_press=lambda *a, id=otrasarea.id: self.editar_otrasareas(id)))
            lista_grid.add_widget(Button(text="Eliminar", size_hint_y=None, height=40,
                                          on_press=lambda *a, id=otrasarea.id: self.eliminar_otrasareas(id)))

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
            if hasattr(self.ids, 'otrasareas_id'):
                self.ids.otrasareas_id.text = str(otrasarea.id)
        else:
            StyledPopup.mostrar_popup("Error", "Registro no encontrado.", tipo="error")

    def on_enter(self):
        self.cargar_otrasareas()