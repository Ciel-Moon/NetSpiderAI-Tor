import logging
import logging.config
import os
from config import settings

def get_logger(name: str) -> logging.Logger:
    """Return a logger configured from logging.conf."""
    log_conf = os.path.join(os.path.dirname(__file__), '..', 'config', 'logging.conf')
    if os.path.exists(log_conf):
        logging.config.fileConfig(log_conf, defaults={'log_file': settings.LOG_FILE})
    else:
        logging.basicConfig(level=settings.LOG_LEVEL)
    return logging.getLogger(name)
