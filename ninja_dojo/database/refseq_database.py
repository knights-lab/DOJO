from ninja_trebuchet.factory import download
import sqlite3

from .. import SETTINGS, LOGGER
from ..downloaders import RefseqCatalog, RefseqAssemblySummary, NCBITaxdmp


class RefSeqDatabase:
    def __init__(self, _downloaders=(RefseqCatalog, RefseqAssemblySummary, NCBITaxdmp)):
        self._downloaders = _downloaders

    @download
    def _parse(self):
        SETTINGS.
