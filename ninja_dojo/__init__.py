from ninja_trebuchet.config import Settings
from ninja_trebuchet import Logger
from ninja_dojo.config.settings import ninja_dojo_settings

SETTINGS = Settings('shogun', ninja_dojo_settings)
LOGGER = Logger()

__all__ = ['config',
           'taxonomy']
