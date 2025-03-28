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
    MenuScreen, AreasScreen, SalonesScreen, EstadisticaScreen, DonacionesScreen, DistribucionesScreen, 
    LogisticaScreen, OtrasAreasScreen, EnsenanzaScreen, RecepcionScreen, ReporteScreen, AyudaScreen, 
    AulasScreen, ListAreasScreen ) 
import logging

class EmiApp(App):    
    def build(self):
        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        
        # Icono
        self.icon = 'kids.ico'
        
        # Inicialización de la sesión de SQLAlchemy
        self.session = SessionLocal()
        logger.debug("SQLAlchemy session initialized.")

        # Manejador de las ventanas
        sm = ScreenManager()

        # Inicialización de los controladores con la sesión
        controllers = {
            "areas": AreasController(self.session),
            "salones": SalonesController(self.session),
            "aulas": AulasController(self.session),
            "donaciones": DonacionesController(self.session),
            "ensenanza": EnsenanzaController(self.session),
            "logistica": LogisticaController(self.session),
            "otrasareas": OtrasAreasController(self.session),
            "recepcion": RecepcionController(self.session),
            "distribuciones": DistribucionesController(self.session),
        }
        logger.debug("Controllers initialized: %s", list(controllers.keys()))

        # Creación de pantallas
        screens = [
            MenuScreen(name='menu'),
            AreasScreen(controllers["areas"], name='areas'),
            SalonesScreen(controllers["salones"], name='salones'),
            AulasScreen(controllers["aulas"], name='aulas'),
            EstadisticaScreen(name='estadistica'),
            DonacionesScreen(controllers["donaciones"], name='donaciones'),
            DistribucionesScreen(controllers["distribuciones"], name='distribucion'),
            LogisticaScreen(controllers["logistica"], name='logistica'),
            OtrasAreasScreen(controllers["otrasareas"], name='otrasareas'),
            EnsenanzaScreen(controllers["ensenanza"], name='ensenanza'),
            RecepcionScreen(controllers["recepcion"], name='recepcion'),
            ReporteScreen(name='reporte'),
            AyudaScreen(name='ayuda'),
            ListAreasScreen(name='list_areas'),  # Add the new screen
        ]

        # Agregar pantallas al manejador
        for screen in screens:
            sm.add_widget(screen)
            logger.debug("Screen added: %s", screen.name)

        return sm

    def on_stop(self):
        """ Cierra la sesión de la base de datos al salir de la aplicación. """
        self.session.close()
        logging.getLogger(__name__).debug("SQLAlchemy session closed.")

if __name__ == '__main__':
    EmiApp().run()
