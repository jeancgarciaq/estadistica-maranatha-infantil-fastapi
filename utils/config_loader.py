import json
import os
import logging

logger = logging.getLogger(__name__)

def obtener_medidas():
    """Carga las unidades de medida desde el archivo JSON centralizado."""
    try:
        ruta = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'medidas.json')
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("unidades", [])
    except Exception as e:
        logger.error(f"Error al cargar medidas.json: {e}")
    
    # Fallback por si falla el archivo
    return ["Unidad(es)", "Kilogramos", "Gramos", "Miligramo", "Litros", "Mililitros"]
