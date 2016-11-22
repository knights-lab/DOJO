from ninja_utils.config import Settings
from ninja_utils import Logger
from dojo.config.settings import dojo_settings

SETTINGS = Settings('dojo', dojo_settings)
LOGGER = Logger(logfp=SETTINGS.settings['log'], log_persist=SETTINGS.settings['log_persists'])

__all__ = [
    'annotaters'
    'config',
    'downloaders',
    'taxonomy',
    'database'
]
