from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from datetime import datetime
from components import StyledPopup

class DonacionesScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/donaciones.kv')
        except Exception as e:
            print(f"Error al cargar la vista donaciones: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador

    def obtener_datos_formulario(self):
        descripcion = self.ids.donacion_descripcion.text.strip()
        cantidad = self.ids.donacion_cantidad.text.strip()
        unidad = self.ids.donacion_unidad.text.strip()
        fecha = self.ids.donacion_fecha.text.strip()
        equipo = self.ids.donacion_equipo.text.strip()

        # Validación básica
        if not descripcion:
            StyledPopup.mostrar_popup("Error", "La descripción es obligatoria.", tipo="error")
            return None
        if not cantidad:
            StyledPopup.mostrar_popup("Error", "La cantidad es obligatoria.", tipo="error")
            return None
        try:
            float_cantidad = float(cantidad)
        except ValueError:
            StyledPopup.mostrar_popup("Error", "La cantidad debe ser un número.", tipo="error")
            return None
        if not unidad:
            StyledPopup.mostrar_popup("Error", "La unidad es obligatoria.", tipo="error")
            return None
        if not equipo:
            StyledPopup.mostrar_popup("Error", "El equipo es obligatorio.", tipo="error")
            return None
        if not fecha:
            StyledPopup.mostrar_popup("Error", "La fecha es obligatoria.", tipo="error")
            return None
        try:
            datetime.strptime(fecha, '%Y-%m-%d').date()
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Formato de fecha incorrecto. Debe ser YYYY-MM-DD.", tipo="error")
            return None

        return {
            "descripcion": descripcion,
            "cantidad": float_cantidad,
            "unidad": unidad,
            "equipo": equipo,
            "fecha": fecha
        }

    def crear_donacion(self):
        datos = self.obtener_datos_formulario()
        if datos:
            exito, mensaje = self.controlador.crear_donacion(datos)
            if exito:
                StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
                self.limpiar_formulario()
            else:
                StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def actualizar_donacion(self):
        id_texto = self.ids.donacion_id.text.strip()
        if not id_texto or not id_texto.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para actualizar.", tipo="error")
            return
        
        datos = self.obtener_datos_formulario()
        if datos:
            exito, mensaje = self.controlador.actualizar_donacion(int(id_texto), datos)
            if exito:
                StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
                self.limpiar_formulario()
            else:
                StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def eliminar_donacion(self, id_val):
        if not id_val or not id_val.isdigit():
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID válido para eliminar.", tipo="error")
            return
            
        exito, mensaje = self.controlador.eliminar_donacion(int(id_val))
        if exito:
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
            self.limpiar_formulario()
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

    def limpiar_formulario(self):
        self.ids.donacion_id.text = ""
        self.ids.donacion_descripcion.text = ""
        self.ids.donacion_cantidad.text = ""
        self.ids.donacion_unidad.text = ""
        self.ids.donacion_fecha.text = ""
        self.ids.donacion_equipo.text = ""

    def actualizar_lista_donaciones(self, donaciones):
        lista_donaciones_grid = self.ids.lista_donaciones
        lista_donaciones_grid.clear_widgets()
        for donacion in donaciones:
            lista_donaciones_grid.add_widget(Label(text=donacion.descripcion))
            lista_donaciones_grid.add_widget(Label(text=str(donacion.cantidad)))
            lista_donaciones_grid.add_widget(Label(text=donacion.unidad))
            lista_donaciones_grid.add_widget(Label(text=donacion.equipo))
            lista_donaciones_grid.add_widget(Label(text=donacion.fecha))
            lista_donaciones_grid.add_widget(Button(text="Editar", on_press=lambda btn, id=donacion.id: self.editar_donacion(id)))
            # No llamar directamente al controlador en eliminar
            lista_donaciones_grid.add_widget(Button(text="Eliminar", on_press=lambda btn, id=donacion.id: self.eliminar_donacion(str(id))))
    
    def editar_donacion(self, id):
        donacion = self.controlador.obtener_donacion(id)
        if donacion:
            self.ids.donacion_id.text = str(donacion.id)
            self.ids.donacion_descripcion.text = donacion.descripcion
            self.ids.donacion_cantidad.text = str(donacion.cantidad)
            self.ids.donacion_unidad.text = donacion.unidad
            self.ids.donacion_equipo.text = donacion.equipo
            self.ids.donacion_fecha.text = donacion.fecha.strftime('%Y-%m-%d')
            self.cargar_salones_seleccionados(donacion.salones)

    def buscar_donacion(self):
        """Obtiene los datos del formulario y llama al método buscar_donacion del controlador."""
        donacion_id = self.ids.donacion_id.text.strip()
        donacion_descripcion = self.ids.donacion_descripcion.text.strip()

        if not donacion_id and not donacion_descripcion:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID o una descripción para buscar la donación.", tipo="error")
            return

        d_id = int(donacion_id) if donacion_id.isdigit() else None
        exito, donacion, mensaje = self.controlador.buscar_donacion(id=d_id, descripcion=donacion_descripcion)
        
        if exito:
            self.editar_donacion(donacion.id)
            StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
        else:
            StyledPopup.mostrar_popup("Error", mensaje, tipo="error")
