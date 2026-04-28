import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase
from kivy.core.window import Window
from models.database import SessionLocal
from utils.firebase_sync import SyncManager
from controllers import (
    AreasController, SalonesController, AulasController, DonacionesController, EnsenanzaController, 
    LogisticaController, OtrasAreasController, RecepcionController, DistribucionesController,
    UsuariosController )
from screens import (
    LoginScreen,
    MenuScreen, AreasScreen, SalonesScreen, EstadisticaScreen, DonacionesScreen, CombinarDonacionesScreen,
    DistribucionesScreen, LogisticaScreen, OtrasAreasScreen, EnsenanzaScreen, RecepcionScreen, ReporteScreen,
    AyudaScreen, AulasScreen, ListAreasScreen, ListSalonesScreen, ListAulasScreen, ListDonacionesScreen,
    ListPreparadosScreen, ListDistribucionesScreen, ListOtrasAreasScreen, ListLogisticaScreen,
    UsuariosScreen)
from models.security import ROLE_ROOT, seed_security_data
import logging

# Configure logging
logger = logging.getLogger(__name__)

class EmiApp(App):    
    current_user = None

    def build(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log"),
                logging.StreamHandler()
            ]
        )

        LabelBase.register(
            name='LineAwesome', 
            fn_regular='assets/fonts/la-regular-400.ttf'
        )
        
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        
        # Icono
        self.icon = 'kids.ico'
        
        # Inicialización de la sesión de SQLAlchemy
        self.session = SessionLocal()
        logger.debug("SQLAlchemy sesión inicializada.")

        # Sincronización piloto con Firebase.
        self.sync_manager = SyncManager()

        # Inicializa roles/permisos y usuarios base si aún no existen.
        try:
            with self.session.begin():
                seed_security_data(self.session)
        except Exception as e:
            logger.error("No se pudo inicializar seguridad: %s", e)
            self.session.rollback()

        # Inicialización de los controladores con la sesión
        controllers = {
            "areas": AreasController(session=self.session),
            "salones": SalonesController(session=self.session),
            "aulas": AulasController(session=self.session),
            "donaciones": DonacionesController(session=self.session),
            "ensenanza": EnsenanzaController(session=self.session),
            "logistica": LogisticaController(session=self.session),
            "otrasareas": OtrasAreasController(session=self.session),
            "recepcion": RecepcionController(session=self.session),
            "distribuciones": DistribucionesController(session=self.session),
            "usuarios": UsuariosController(session=self.session),
        }
        logger.debug("Controladores inicializados: %s", list(controllers.keys()))

        # Asignar los controladores como atributos de la aplicación
        self.areas_controller = controllers["areas"]
        self.salones_controller = controllers["salones"]
        self.aulas_controller = controllers["aulas"]
        self.donaciones_controller = controllers["donaciones"]
        self.distribuciones_controller = controllers["distribuciones"]  
        self.usuarios_controller = controllers["usuarios"]
        logger.debug("AreasController, SalonesController, AulasController, DonacionesController y DistribucionesController fueron asignados a EmiApp.")

        # Manejador de las ventanas
        sm = ScreenManager()

        # Creación de pantallas
        screens = [
            LoginScreen(name='login'),
            MenuScreen(name='menu'),
            AreasScreen(controllers["areas"], name='areas'),
            SalonesScreen(controllers["salones"], name='salones'),
            AulasScreen(controllers["aulas"], name='aulas'),
            EstadisticaScreen(name='estadistica'),
            DonacionesScreen(controllers["donaciones"], name='donaciones'),
            CombinarDonacionesScreen(controllers["donaciones"], name='combinar_donaciones'),
            DistribucionesScreen(controllers["distribuciones"], name='distribuciones'),
            LogisticaScreen(controllers["logistica"], name='logisticas'),
            OtrasAreasScreen(controllers["otrasareas"], name='otrasareas'),
            EnsenanzaScreen(controllers["ensenanza"], name='ensenanza'),
            RecepcionScreen(controllers["recepcion"], name='recepcion'),
            ReporteScreen(name='reporte'),
            AyudaScreen(name='ayuda'),
            ListAreasScreen(controlador=controllers["areas"], name='lista_areas'),  
            ListSalonesScreen(controlador=controllers["salones"], name='lista_salones'),
            ListAulasScreen(controlador=controllers["aulas"], name='lista_aulas'),
            ListDonacionesScreen(controlador=controllers["donaciones"], name='lista_donaciones'),
            ListPreparadosScreen(controlador=controllers["donaciones"], name='lista_preparados'),
            ListDistribucionesScreen(controlador=controllers["distribuciones"], name='lista_distribuciones'),
            ListOtrasAreasScreen(controlador=controllers["otrasareas"], name='lista_otras_areas'),
            ListLogisticaScreen(controlador=controllers["logistica"], name='lista_logisticas'),
            UsuariosScreen(controlador=controllers["usuarios"], name='usuarios'),
        ]

        # Agregar pantallas al manejador
        for screen in screens:
            try:
                sm.add_widget(screen)
                logger.debug("Screen added: %s", screen.name)
            except Exception as e:
                logger.error(f"Error al agregar la pantalla {screen.name}: {e}")

        sm.current = 'login'

        return sm

    def sincronizar_piloto(self):
        """Sincroniza la cola local y descarga cambios de donaciones/distribuciones si Firebase está configurado."""
        if not hasattr(self, 'sync_manager'):
            self.sync_manager = SyncManager()

        self.sync_manager.set_auth_token_provider(
            lambda: self.usuarios_controller.obtener_token_firebase(self.current_user)
        )

        if not self.sync_manager.client.is_configured():
            logger.info("Firebase no está configurado; sincronización piloto omitida.")
            return {'pushed': [], 'pulled': []}

        pushed = self.sync_manager.push_pending(self.session)
        pulled_donaciones = self.sync_manager.pull_collection(self.session, 'donaciones')
        pulled_distribuciones = self.sync_manager.pull_collection(self.session, 'distribuciones')
        pulled_usuarios = self.sync_manager.pull_collection(self.session, 'usuarios')

        return {
            'pushed': pushed,
            'pulled': {
                'donaciones': pulled_donaciones,
                'distribuciones': pulled_distribuciones,
                'usuarios': pulled_usuarios,
            },
        }

    def set_current_user(self, user):
        self.current_user = user
        logger.info("Usuario autenticado: %s", getattr(user, 'username', 'desconocido'))

    def logout(self):
        self.current_user = None
        if self.root:
            self.root.current = 'login'

    def has_permission(self, permiso_codigo):
        user = self.current_user
        if user is None:
            return False

        role = getattr(user, 'rol', None)
        if role is None:
            return False

        if role.nombre == ROLE_ROOT:
            return True

        permisos = {perm.codigo for perm in (role.permisos or [])}
        return permiso_codigo in permisos or '*' in permisos

    def can_access_screen(self, screen_name):
        if not self.current_user:
            return screen_name == 'login'

        screen_permissions = {
            'areas': 'areas.view',
            'lista_areas': 'areas.view',
            'salones': 'salones.manage',
            'lista_salones': 'salones.view',
            'aulas': 'aulas.manage',
            'lista_aulas': 'aulas.view',
            'estadistica': 'estadistica.view',
            'donaciones': 'donaciones.view',
            'lista_donaciones': 'donaciones.view',
            'combinar_donaciones': 'preparados.view',
            'lista_preparados': 'preparados.view',
            'distribuciones': 'distribuciones.view',
            'lista_distribuciones': 'distribuciones.view',
            'logisticas': 'logistica.view',
            'lista_logisticas': 'logistica.view',
            'otrasareas': 'otras_areas.view',
            'lista_otras_areas': 'otras_areas.view',
            'ensenanza': 'ensenanza.view',
            'recepcion': 'recepcion.view',
            'reporte': 'reporte.view',
            'ayuda': 'ayuda.view',
            'usuarios': 'users.manage',
            'menu': 'estadistica.view',
        }

        required_permission = screen_permissions.get(screen_name)
        if not required_permission:
            return True
        return self.has_permission(required_permission)

    def on_stop(self):
        """ Cierra la sesión de la base de datos al salir de la aplicación. """
        if hasattr(self, 'session') and self.session:
            self.session.close()
            logger.debug("SQLAlchemy session closed.")

if __name__ == '__main__':
    EmiApp().run()
