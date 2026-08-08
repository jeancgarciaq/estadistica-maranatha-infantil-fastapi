import logging
import os
from logging.handlers import RotatingFileHandler

APP_LOG_DIR = "logs"
APP_LOG_FILE = "app.log"

_configured = False


def _get_log_dir():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    log_dir = os.path.join(project_root, APP_LOG_DIR)
    os.makedirs(log_dir, exist_ok=True)
    return log_dir


def setup_logging(level: int = logging.INFO, log_file: str | None = None):
    """Configura el logging de la aplicacion a consola + archivo rotativo.

    Debe llamarse una sola vez durante el startup. Si otros modulos ya dejaron
    un handler por defecto en el root logger, se reemplaza.
    """
    global _configured

    log_path = log_file or os.path.join(_get_log_dir(), APP_LOG_FILE)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8", delay=False
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()
    root.addHandler(file_handler)
    root.addHandler(console_handler)

    for noisy in ("uvicorn.access", "uvicorn.error", "uvicorn", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _configured = True
    logging.getLogger(__name__).info(
        "Logging configurado -> archivo: %s", log_path
    )
    return log_path