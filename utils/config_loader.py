import json
import os
import logging

logger = logging.getLogger(__name__)

# Cache para evitar lecturas de disco frecuentes en el servidor web
_CACHE_MEDIDAS = None

def obtener_medidas():
    """Carga las unidades de medida desde el archivo JSON centralizado."""
    global _CACHE_MEDIDAS
    if _CACHE_MEDIDAS is not None:
        return _CACHE_MEDIDAS

    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        ruta = os.path.join(base_dir, 'config', 'medidas.json')
        
        if os.path.exists(ruta):
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _CACHE_MEDIDAS = data.get("unidades", [])
                return _CACHE_MEDIDAS
    except Exception as e:
        logger.error(f"Error al cargar medidas.json: {e}")
    
    # Fallback si el archivo no es accesible o no existe
    return ["Unidad(es)", "Kilogramos", "Gramos", "Miligramo", "Litros", "Mililitros"]
