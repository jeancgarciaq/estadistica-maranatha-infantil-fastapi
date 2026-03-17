from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime
from components.styled_popup import StyledPopup


class LogisticaScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/logistica.kv')
        except Exception as e:
            print(f"Error cargando logistica.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def obtener_datos_formulario(self):
        almacen = self.ids.logistica_almacen.text.strip()
        capitan = self.ids.logistica_capitan.text.strip()
        distribucion = self.ids.logistica_distribucion.text.strip()
        hidratacion = self.ids.logistica_hidratacion.text.strip()
        pasillo = self.ids.logistica_pasillo.text.strip()
        secretaria = self.ids.logistica_secretaria.text.strip()
        fecha = self.ids.logistica_fecha.text.strip()

        campos = {
            "almacen": almacen, "capitan": capitan,
            "distribucion": distribucion, "hidratacion": hidratacion,
            "pasillo": pasillo, "secretaria": secretaria, "fecha": fecha
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
                "almacen": int(almacen),
                "capitan": int(capitan),
                "distribucion": int(distribucion),
                "hidratacion": int(hidratacion),
                "pasillo": int(pasillo),
                "secretaria": int(secretaria),
                "fecha": fecha
            }
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Los campos numéricos deben ser números enteros.", tipo="error")
            return None

    def _limpiar_campos(self):
        for campo in ['logistica_almacen', 'logistica_capitan', 'logistica_distribucion',
                      'logistica_hidratacion', 'logistica_pasillo', 'logistica_secretaria', 'logistica_fecha']:
            if hasattr(self.ids, campo):
                getattr(self.ids, campo).text = ""
        if hasattr(self.ids, 'logistica_id'):
            self.ids.logistica_id.text = ""

    def crear_logistica(self):
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.crear_logistica(
            datos["almacen"], datos["capitan"], datos["distribucion"],
            datos["hidratacion"], datos["pasillo"], datos["secretaria"], datos["fecha"]
        )
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_logisticas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_logistica(self):
        logistica_id = self.ids.logistica_id.text.strip() if hasattr(self.ids, 'logistica_id') else ""
        if not logistica_id or not logistica_id.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para actualizar.", tipo="error")
            return
        datos = self.obtener_datos_formulario()
        if not datos:
            return
        exito, mensaje = self.controlador.actualizar_logistica(
            int(logistica_id), datos["almacen"], datos["capitan"], datos["distribucion"],
            datos["hidratacion"], datos["pasillo"], datos["secretaria"], datos["fecha"]
        )
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self._limpiar_campos()
            self.cargar_logisticas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_logistica(self, id):
        exito, mensaje = self.controlador.eliminar_logistica(id)
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.cargar_logisticas()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def cargar_logisticas(self):
        logisticas = self.controlador.listar_logisticas()
        self.actualizar_lista_logisticas(logisticas)

    def actualizar_lista_logisticas(self, logisticas):
        lista_grid = self.ids.lista_logisticas
        lista_grid.clear_widgets()
        if not logisticas:
            lista_grid.add_widget(Label(text="No hay registros de logística", size_hint_y=None, height=40))
            return
        for logistica in logisticas:
            lista_grid.add_widget(Label(text=f"ID: {logistica.id} | Fecha: {logistica.fecha}", size_hint_y=None, height=40))
            lista_grid.add_widget(Button(text="Editar", size_hint_y=None, height=40,
                                          on_press=lambda *a, id=logistica.id: self.editar_logistica(id)))
            lista_grid.add_widget(Button(text="Eliminar", size_hint_y=None, height=40,
                                          on_press=lambda *a, id=logistica.id: self.eliminar_logistica(id)))

    def editar_logistica(self, id):
        logistica = self.controlador.obtener_logistica(id)
        if logistica:
            self.ids.logistica_almacen.text = str(logistica.almacen)
            self.ids.logistica_capitan.text = str(logistica.capitan)
            self.ids.logistica_distribucion.text = str(logistica.distribucion)
            self.ids.logistica_fecha.text = str(logistica.fecha)
            self.ids.logistica_hidratacion.text = str(logistica.hidratacion)
            self.ids.logistica_pasillo.text = str(logistica.pasillo)
            self.ids.logistica_secretaria.text = str(logistica.secretaria)
            if hasattr(self.ids, 'logistica_id'):
                self.ids.logistica_id.text = str(logistica.id)
        else:
            StyledPopup.mostrar_popup("Error", "Logística no encontrada.", tipo="error")

    def on_enter(self):
        self.cargar_logisticas()