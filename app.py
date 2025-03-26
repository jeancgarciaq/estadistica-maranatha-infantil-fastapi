import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from models.database import get_db, SessionLocal
from models.salones import Salon
from models.database import get_db
from sqlalchemy.orm import Session
from controllers import (
    AreasController, SalonesController, AulasController, DonacionesController, EnsenanzaController, 
    LogisticaController, OtrasAreasController, RecepcionController, DistribucionesController )
from screens import (
    MenuScreen, AreasScreen, SalonesScreen, EstadisticaScreen, DonacionesScreen, DistribucionesScreen, 
    LogisticaScreen, OtrasAreasScreen, EnsenanzaScreen, RecepcionScreen, ReporteScreen, AyudaScreen, 
    AulasScreen )

class EmiApp(App):    
    def build(self):
        Window.clearcolor = (20/255, 40/255, 80/255, 1)
        
        #Icono
        self.icon = 'kids.ico'
        
        # Inicialización de la sesión de SQLAlchemy
        self.session = SessionLocal()

        #Manejador de las ventanas
        sm = ScreenManager()

        # Inicialización de los controladores con la sesión
        areas_controller = AreasController(self.session)
        salones_controller = SalonesController(self.session)
        aulas_controller = AulasController(self.session)
        donaciones_controller = DonacionesController(self.session)
        ensenanza_controller = EnsenanzaController(self.session)
        logistica_controller = LogisticaController(self.session)
        otrasareas_controller = OtrasAreasController(self.session)
        recepcion_controller = RecepcionController(self.session)
        distribuciones_controller = DistribucionesController(self.session)

        # Inicialización de las vistas con los controladores
        menu_screen = MenuScreen(name='menu')
        areas_screen = AreasScreen(areas_controller, name='areas')
        salones_screen = SalonesScreen(salones_controller, name='salones')
        aulas_screen = AulasScreen(aulas_controller, name='aulas')
        estadistica_screen = EstadisticaScreen(name='estadistica')
        donaciones_screen = DonacionesScreen(donaciones_controller, name='donaciones')
        distribuciones_screen = DistribucionesScreen(distribuciones_controller, name='distribucion')
        logistica_screen = LogisticaScreen(logistica_controller, name='logistica')
        otrasareas_screen = OtrasAreasScreen(otrasareas_controller, name='otrasareas')
        ensenanza_screen = EnsenanzaScreen(ensenanza_controller, name='ensenanza')
        recepcion_screen = RecepcionScreen(recepcion_controller, name='recepcion')
        reporte_screen = ReporteScreen(name='reporte')
        ayuda_screen = AyudaScreen(name='ayuda')

        # Widget
        sm.add_widget(menu_screen)
        sm.add_widget(areas_screen)
        sm.add_widget(salones_screen)
        sm.add_widget(aulas_screen)
        sm.add_widget(estadistica_screen)
        sm.add_widget(donaciones_screen)
        sm.add_widget(distribuciones_screen)
        sm.add_widget(logistica_screen)
        sm.add_widget(otrasareas_screen)
        sm.add_widget(ensenanza_screen)
        sm.add_widget(recepcion_screen)
        sm.add_widget(reporte_screen)
        sm.add_widget(ayuda_screen)

        return sm

if __name__ == '__main__':
    EmiApp().run()
