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
    AulasScreen, ListAreasScreen, ListSalonesScreen ) 
import logging

class EmiApp(App):    
    def build(self):
        # Configure logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("app.log"),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)
        
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        
        # Icono
        self.icon = 'kids.ico'
        
        # Inicialización de la sesión de SQLAlchemy
        self.session = SessionLocal()
        logger.debug("SQLAlchemy session initialized.")

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

        # Asignar los controladores de áreas, salones como atributo de la aplicación
        self.areas_controller = controllers["areas"]
        self.salones_controller = controllers["salones"]  
        logger.debug("AreasController and SalonesController assigned to EmiApp.")

        # Manejador de las ventanas
        sm = ScreenManager()

        # Creación de pantallas
        screens = [
            MenuScreen(name='menu'),
            AreasScreen(controllers["areas"], vista="areas_vista", name='areas'),
            SalonesScreen(controllers["salones"], vista="salones_vista", name='salones'),
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
            ListAreasScreen(controlador=controllers["areas"], vista="lista_areas_vista", name='lista_areas'),  
            ListSalonesScreen(controlador=controllers["salones"], vista="lista_salones_vista", name='lista_salones'),
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
