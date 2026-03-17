from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from components import StyledPopup

class AulasScreen(Screen):
    def __init__(self, controlador, **kwargs):
        try:
            Builder.load_file('views/aulas.kv')
        except Exception as e:
            print(f"Error al cargar la vista aulas: {e}")
        super().__init__(**kwargs)
        self.controlador = controlador
    def obtener_datos_formulario(self):
        auxiliar = self.ids.aula_auxiliar.text
        capitan = self.ids.aula_capitan.text
        colaborador = self.ids.aula_colaborador.text
        condicion = self.ids.aula_condicion.text
        maestra = self.ids.aula_maestra.text
        ninos = self.ids.aula_ninos.text
        ninas = self.ids.aula_ninas.text
        subcapitan = self.ids.aula_subcapitan.text
        fecha = self.ids.aula_fecha.text
        id_salon = self.ids.aula_id_salon.text

        # Validación básica
        if not auxiliar:
            StyledPopup.mostrar_popup("Error", "El número de auxiliares es obligatorio.", tipo="error")
            return None
        if not capitan:
            StyledPopup.mostrar_popup("Error", "El número de capitanes es obligatorio.", tipo="error")
            return None
        if not colaborador:
            StyledPopup.mostrar_popup("Error", "El número de colaboradores es obligatorio.", tipo="error")
            return None
        if not condicion:
            StyledPopup.mostrar_popup("Error", "La condición es obligatoria.", tipo="error")
            return None
        if not maestra:
            StyledPopup.mostrar_popup("Error", "El número de maestras es obligatorio.", tipo="error")
            return None
        if not ninos:
            StyledPopup.mostrar_popup("Error", "El número de niños es obligatorio.", tipo="error")
            return None
        if not ninas:
            StyledPopup.mostrar_popup("Error", "El número de niñas es obligatorio.", tipo="error")
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
            int(auxiliar)
            int(capitan)
            int(colaborador)
            int(id_salon)
            int(condicion)
            int(maestra)
            int(ninos)
            int(ninas)
            int(subcapitan)
            str(fecha)
        except ValueError:
            StyledPopup.mostrar_popup("Error", "Los campos numéricos deben ser números enteros.", tipo="error")
            return None

        return {
            "auxiliar": int(auxiliar),
            "capitan": int(capitan),
            "colaborador": int(colaborador),
            "condicion": condicion,
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
            self.ids.aula_maestra.text = str(aula.maestra)
            self.ids.aula_ninos.text = str(aula.ninos)
            self.ids.aula_ninas.text = str(aula.ninas)
            self.ids.aula_subcapitan.text = str(aula.subcapitan)
            self.ids.aula_id_salon.text = str(aula.id_salon)
            self.ids.aula_id.text = str(aula.id)

    def mostrar_popup_salones(self):
        """
        Muestra un popup con la lista de salones para seleccionar uno.
        """
        db = self.controlador.get_db_session()
        try:
            salones = db.query(Salon).all()
        except Exception as e:
            self.mostrar_error(f"Error al obtener salones: {e}")
            return
        finally:
            db.close()
            logger.info("Conexión a la base de datos cerrada.")
        

        # Verificar si no hay salones registrados
        if not salones:
            popup = Popup(
                title='Sin Salones',
                content=Label(
                    text='No hay salones registrados.',
                    size_hint=(1, 1),
                    halign='center',
                    valign='middle'
                ),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()
            return

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
        """
        Asigna el ID del salón seleccionado al campo de entrada correspondiente.
        """
        self.ids.aula_id_salon.text = str(salon_id)
    
    def buscar_aula(self):
        """Obtiene los datos del formulario y llama al método buscar_aula del controlador."""
        aula_id = self.ids.aula_id.text.strip()  # ID del aula

        # Validar que al menos uno de los campos esté lleno
        if not aula_id:
            StyledPopup.mostrar_popup("Error", "Debe proporcionar un ID del área.", tipo="error")
            return

        # Convertir el ID a entero si es posible
        aula_id = int(aula_id) if aula_id.isdigit() else None

        # Llamar al método buscar_aula del controlador
        self.controlador.buscar_aula(id=aula_id)