import logging
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ListAreasScreen(Screen):
    """Screen for displaying the list of areas."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info("Initializing ListAreasScreen")
        Builder.load_file("list_areas.kv")
