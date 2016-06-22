from ninja_trebuchet.factory import download
import sqlite3
import os

from .. import SETTINGS, LOGGER
from ..taxonomy import NCBITree
from ..taxonomy.maps import RefseqAssemblyMap, RefseqCatalogMap


class RefSeqDatabase:
    def __init__(self):


    def _parse(self):
        db_path = os.path.join(SETTINGS.get_path('db_dir'), 'refseq.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE tree (ncbi_tid integer, name text, parent_ncbi_tid integer, assembly_version text, refseq_version text, ftp text)''')
        tree = NCBITree()
        assembly_map = RefseqAssemblyMap()
        refseq_catalog_map = RefseqCatalogMap()
        for tree in 
