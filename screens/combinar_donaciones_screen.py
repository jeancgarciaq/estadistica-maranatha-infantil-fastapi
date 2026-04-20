import logging
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from components.styled_popup import StyledPopup
from datetime import datetime
from components.styled_datepicker import StyledDatePicker
from models.donaciones import Donacion
from utils.config_loader import obtener_medidas

# Configuración de logging
logger = logging.getLogger(__name__)

class CombinarDonacionesScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/combinar_donaciones.kv')
        except Exception as e:
            logger.error(f"Error al cargar combinar_donaciones.kv: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador
        self.medidas = obtener_medidas()
        self.componentes_seleccionados = [] # Lista de {'id': id, 'descripcion': desc, 'cantidad_usada': cant}

    def on_pre_enter(self, *args):
        self.limpiar_todo()

    def abrir_datepicker(self, target_id):
        def set_date(date_str):
            self.ids[target_id].text = date_str
        picker = StyledDatePicker(callback=set_date)
        picker.open()

    def abrir_popup_materias_primas(self):
        db = self.controlador.get_db_session()
        try:
            # Solo mostrar donaciones que NO son compuestas (materia prima) y tienen stock
            materias = db.query(Donacion).filter(Donacion.cantidad > 0, Donacion.es_compuesta == False).all()
        except Exception as e:
            StyledPopup.mostrar_popup("Error", f"Error al obtener materias: {e}", tipo="error")
            return
        finally:
            db.close()

        if not materias:
            StyledPopup.mostrar_popup("Aviso", "No hay materias primas disponibles con stock.", tipo="info")
            return

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        grid = GridLayout(cols=1, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        for m in materias:
            # Evitar duplicados ya en la lista actual
            if any(comp['id'] == m.id for comp in self.componentes_seleccionados):
                continue
                
            btn = Button(text=f"ID: {m.id} - {m.descripcion} ({m.cantidad} {m.unidad})", size_hint_y=None, height=50)
            btn.bind(on_press=lambda b, m_id=m.id, m_desc=m.descripcion, m_unid=m.unidad: self._seleccionar_materia(m_id, m_desc, m_unid, popup))
            grid.add_widget(btn)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        
        close_btn = Button(text="Cerrar", size_hint_y=None, height=40)
        layout.add_widget(close_btn)

        popup = Popup(title="Seleccionar Materia Prima", content=layout, size_hint=(0.9, 0.9))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def _seleccionar_materia(self, m_id, m_desc, m_unid, popup):
        popup.dismiss()
        # Pedir la cantidad a usar de esa materia
        self.abrir_popup_cantidad_materia(m_id, m_desc, m_unid)

    def abrir_popup_cantidad_materia(self, m_id, m_desc, m_unid):
        from kivy.uix.textinput import TextInput
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        layout.add_widget(Label(text=f"¿Qué cantidad de '{m_desc}' usará?\n(Unidad: {m_unid})", size_hint_y=None, height=60))
        
        cant_input = TextInput(text='', multiline=False, input_filter='float', size_hint_y=None, height=40)
        layout.add_widget(cant_input)
        
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_add = Button(text="Agregar", background_color=(0, 1, 0, 1))
        btn_cancel = Button(text="Cancelar")
        
        btn_layout.add_widget(btn_add)
        btn_layout.add_widget(btn_cancel)
        layout.add_widget(btn_layout)
        
        popup = Popup(title="Cantidad a usar", content=layout, size_hint=(0.8, 0.4))
        
        def agregar(instance):
            cant_str = cant_input.text.strip()
            if not cant_str:
                return
            try:
                cant = float(cant_str)
                if cant <= 0:
                    return
                
                self.componentes_seleccionados.append({
                    'id': m_id,
                    'descripcion': m_desc,
                    'cantidad_usada': cant,
                    'unidad': m_unid
                })
                self.actualizar_lista_ui()
                popup.dismiss()
            except ValueError:
                pass

        btn_add.bind(on_press=agregar)
        btn_cancel.bind(on_press=popup.dismiss)
        popup.open()

    def actualizar_lista_ui(self):
        container = self.ids.lista_componentes
        container.clear_widgets()
        for i, comp in enumerate(self.componentes_seleccionados):
            row = BoxLayout(size_hint_y=None, height=40, spacing=10)
            row.add_widget(Label(text=f"{comp['descripcion']} - {comp['cantidad_usada']} {comp['unidad']}", size_hint_x=0.7))
            
            btn_del = Button(text="X", size_hint_x=0.3, background_color=(1, 0, 0, 1))
            btn_del.bind(on_press=lambda b, idx=i: self.quitar_componente(idx))
            row.add_widget(btn_del)
            container.add_widget(row)

    def quitar_componente(self, index):
        if 0 <= index < len(self.componentes_seleccionados):
            self.componentes_seleccionados.pop(index)
            self.actualizar_lista_ui()

    def realizar_combinacion(self):
        desc = self.ids.res_descripcion.text.strip()
        cant = self.ids.res_cantidad.text.strip()
        unid = self.ids.res_unidad.text
        fecha = self.ids.res_fecha.text.strip()
        equipo = self.ids.res_equipo.text.strip()

        if not desc or not cant or not fecha or not equipo:
            StyledPopup.mostrar_popup("Error", "Todos los campos del producto resultante son obligatorios.", tipo="error")
            return

        if not self.componentes_seleccionados:
            StyledPopup.mostrar_popup("Error", "Debe agregar al menos una materia prima.", tipo="error")
            return

        try:
            val_cant = float(cant)
            if "Unidad" in unid and not val_cant.is_integer():
                StyledPopup.mostrar_popup("Error", "Para 'Unidad(es)', la cantidad debe ser entera.", tipo="error")
                return

            datos_resultado = {
                "descripcion": desc,
                "cantidad": val_cant,
                "unidad": unid,
                "fecha": fecha,
                "equipo": equipo
            }
            
            # Formatear componentes para el controlador
            lista_comp = [{'id': c['id'], 'cantidad': c['cantidad_usada']} for c in self.componentes_seleccionados]
            
            exito, mensaje = self.controlador.combinar_donaciones(datos_resultado, lista_comp)
            if exito:
                StyledPopup.mostrar_popup("Éxito", mensaje, tipo="success")
                self.limpiar_todo()
                self.manager.current = 'menu'
            else:
                StyledPopup.mostrar_popup("Error", mensaje, tipo="error")

        except Exception as e:
            StyledPopup.mostrar_popup("Error", f"Error procesando datos: {str(e)}", tipo="error")

    def limpiar_todo(self):
        self.ids.res_descripcion.text = ""
        self.ids.res_cantidad.text = ""
        self.ids.res_unidad.text = "Unidad(es)"
        self.ids.res_fecha.text = datetime.now().strftime("%Y-%m-%d")
        self.ids.res_equipo.text = ""
        self.componentes_seleccionados = []
        self.ids.lista_componentes.clear_widgets()
