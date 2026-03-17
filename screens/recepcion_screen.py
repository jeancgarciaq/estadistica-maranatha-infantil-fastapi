from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime
from components.styled_popup import StyledPopup


class RecepcionScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/recepcion.kv')
        except Exception as e:
            print(f"Error cargando recepcion.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def obtener_datos_formulario(self):
        nombre = self.ids.recepcion_nombre.text.strip()
        fecha = self.ids.recepcion_fecha.text.strip()

        if not nombre:
            StyledPopup.mostrar_popup("Error", "El nombre es obligatorio.", tipo="error")
            return None
        if not fecha:
            StyledPopup.mostrar_popup("Error", "La fecha es obligatoria.", tipo="error")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Formato de fecha incorrecto. Debe ser YYYY-MM-DD.", tipo="error")
            return None

        return {"nombre": nombre, "fecha": fecha}

    def _limpiar_campos(self):
        self.ids.recepcion_nombre.text = ""
        self.ids.recepcion_fecha.text = ""
        if hasattr(self.ids, 'recepcion_id'):
            self.ids.recepcion_id.text = ""

    def crear_recepcion(self):
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.crear_recepcion(datos["nombre"], datos["fecha"])
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_recepciones()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_recepcion(self):
        recepcion_id = self.ids.recepcion_id.text.strip() if hasattr(self.ids, 'recepcion_id') else ""
        if not recepcion_id or not recepcion_id.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para actualizar.", tipo="error")
            return
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.actualizar_recepcion(
            int(recepcion_id), datos["nombre"], datos["fecha"]
        )
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_recepciones()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_recepcion(self, id):
        exito, mensaje = self.controlador.eliminar_recepcion(id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_recepciones()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def cargar_recepciones(self):
        recepciones = self.controlador.listar_recepciones()
        self.actualizar_lista_recepciones(recepciones)

    def actualizar_lista_recepciones(self, recepciones):
        lista_grid = self.ids.lista_recepciones
        lista_grid.clear_widgets()
        if not recepciones:
            lista_grid.add_widget(Label(text="No hay recepciones registradas", size_hint_y=None, height=40))
            return
        for recepcion in recepciones:
            lista_grid.add_widget(Label(text=f"ID: {recepcion.id} | {recepcion.nombre}", size_hint_y=None, height=40))
            lista_grid.add_widget(Button(text="Editar", size_hint_y=None, height=40,
                                          on_press=lambda *a, id=recepcion.id: self.editar_recepcion(id)))
            lista_grid.add_widget(Button(text="Eliminar", size_hint_y=None, height=40,
                                          on_press=lambda *a, id=recepcion.id: self.eliminar_recepcion(id)))

    def editar_recepcion(self, id):
        recepcion = self.controlador.obtener_recepcion(id)
        if recepcion:
            self.ids.recepcion_nombre.text = recepcion.nombre
            fecha = recepcion.fecha
            self.ids.recepcion_fecha.text = fecha.strftime('%Y-%m-%d') if hasattr(fecha, 'strftime') else str(fecha)
            if hasattr(self.ids, 'recepcion_id'):
                self.ids.recepcion_id.text = str(recepcion.id)
        else:
            StyledPopup.mostrar_popup("Error", "Recepción no encontrada.", tipo="error")

    def on_enter(self):
        self.cargar_recepciones()