import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from models.database import SessionLocal
from controllers import (
    AreasController, SalonesController, AulasController, DonacionesController, EnsenanzaController, 
    LogisticaController, OtrasAreasController, RecepcionController, DistribucionesController )
from screens import (
    MenuScreen, AreasScreen, SalonesScreen, EstadisticaScreen, DonacionesScreen, CombinarDonacionesScreen,
    DistribucionesScreen, LogisticaScreen, OtrasAreasScreen, EnsenanzaScreen, RecepcionScreen, ReporteScreen,
    AyudaScreen, AulasScreen, ListAreasScreen, ListSalonesScreen, ListAulasScreen, ListDonacionesScreen,
    ListDistribucionesScreen, ListOtrasAreasScreen )
import logging

# Configure logging
logger = logging.getLogger(__name__)

class EmiApp(App):    
    def build(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log"),
                logging.StreamHandler()
            ]
        )
        
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        
        # Icono
        self.icon = 'kids.ico'
        
        # Inicialización de la sesión de SQLAlchemy
        self.session = SessionLocal()
        logger.debug("SQLAlchemy sesión inicializada.")

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
        }
        logger.debug("Controladores inicializados: %s", list(controllers.keys()))

        # Asignar los controladores como atributos de la aplicación
        self.areas_controller = controllers["areas"]
        self.salones_controller = controllers["salones"]
        self.aulas_controller = controllers["aulas"]
        self.donaciones_controller = controllers["donaciones"]
        self.distribuciones_controller = controllers["distribuciones"]  
        logger.debug("AreasController, SalonesController, AulasController, DonacionesController y DistribucionesController fueron asignados a EmiApp.")

        # Manejador de las ventanas
        sm = ScreenManager()

        # Creación de pantallas
        screens = [
            MenuScreen(name='menu'),
            AreasScreen(controllers["areas"], name='areas'),
            SalonesScreen(controllers["salones"], name='salones'),
            AulasScreen(controllers["aulas"], name='aulas'),
            EstadisticaScreen(name='estadistica'),
            DonacionesScreen(controllers["donaciones"], name='donaciones'),
            CombinarDonacionesScreen(controllers["donaciones"], name='combinar_donaciones'),
            DistribucionesScreen(controllers["distribuciones"], name='distribuciones'),
            LogisticaScreen(controllers["logistica"], name='logistica'),
            OtrasAreasScreen(controllers["otrasareas"], name='otrasareas'),
            EnsenanzaScreen(controllers["ensenanza"], name='ensenanza'),
            RecepcionScreen(controllers["recepcion"], name='recepcion'),
            ReporteScreen(name='reporte'),
            AyudaScreen(name='ayuda'),
            ListAreasScreen(controlador=controllers["areas"], name='lista_areas'),  
            ListSalonesScreen(controlador=controllers["salones"], name='lista_salones'),
            ListAulasScreen(controlador=controllers["aulas"], name='lista_aulas'),
            ListDonacionesScreen(controlador=controllers["donaciones"], name='lista_donaciones'),
            ListDistribucionesScreen(controlador=controllers["distribuciones"], name='lista_distribuciones'),
            ListOtrasAreasScreen(controlador=controllers["otrasareas"], name='lista_otras_areas'),
        ]

        # Agregar pantallas al manejador
        for screen in screens:
            try:
                sm.add_widget(screen)
                logger.debug("Screen added: %s", screen.name)
            except Exception as e:
                logger.error(f"Error al agregar la pantalla {screen.name}: {e}")

        return sm

    def on_stop(self):
        """ Cierra la sesión de la base de datos al salir de la aplicación. """
        if hasattr(self, 'session') and self.session:
            self.session.close()
            logger.debug("SQLAlchemy session closed.")

if __name__ == '__main__':
    EmiApp().run()
