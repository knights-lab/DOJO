from ninja_utils.config import Settings
from ninja_utils import Logger
from ninja_dojo.config.settings import ninja_dojo_settings

SETTINGS = Settings('dojo', ninja_dojo_settings)
LOGGER = Logger(logfp=SETTINGS.settings['log'], log_persist=SETTINGS.settings['log_persists'])

__all__ = [
    'annotaters'
    'config',
    'downloaders',
    'taxonomy',
    'database'
]
