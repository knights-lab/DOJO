from ninja_trebuchet.config import Settings
from ninja_trebuchet import Logger
from ninja_dojo.config.settings import ninja_dojo_settings

SETTINGS = Settings('dojo', ninja_dojo_settings)
LOGGER = Logger(logfp=SETTINGS.settings['log'], log_persist=SETTINGS.settings['log_persists'])

__all__ = ['config',
           'taxonomy']
