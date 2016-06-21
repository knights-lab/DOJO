from ninja_trebuchet.factory import download
import sqlite3
import os

from .. import SETTINGS, LOGGER
from ..downloaders import RefseqCatalog, RefseqAssemblySummary, NCBITaxdmp


class RefSeqDatabase:
    def __init__(self, _downloaders=(RefseqCatalog, RefseqAssemblySummary, NCBITaxdmp)):
        self._downloaders = _downloaders

    @download
    def _parse(self):
        db_path = os.path.join(SETTINGS.get_path('db_dir'), 'refseq.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        # c.execute('''CREATE TABLE tree (date )''')
