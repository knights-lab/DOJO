import sqlite3
import os
import blaze

from .. import SETTINGS, LOGGER
from ..taxonomy import NCBITree
from ..taxonomy.maps import RefseqAssemblyMap, RefseqCatalogMap


class RefSeqDatabase:
    def __init__(self, _path=os.path.join(SETTINGS.get_path('db_dir'), 'refseq.db')):
        self.path = _path
        if not os.path.exists(self.path):
            self._create()

    def _create(self):
        with sqlite3.connect(self.path) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS tree (ncbi_tid INTEGER, name TEXT, rank TEXT, parent_ncbi_tid INTEGER, assembly_version TEXT, refseq_version TEXT, ftp TEXT)')
            tree = NCBITree()
            assembly_map = RefseqAssemblyMap()
            refseq_catalog_map = RefseqCatalogMap()
            for ncbi_tid, rank, name, parent_ncbi_tid in tree.dfs_traversal():
                assembly_version = assembly_map.ncbi_tid2refseq_assembly_accession[ncbi_tid]
                refseq_version = refseq_catalog_map.ncbi_tid2refseq_accession[ncbi_tid]
                ftp_path = assembly_map.ncbi_tid2ftp_path[ncbi_tid]
                c.execute('INSERT INTO tree VALUES (?,?,?,?,?,?,?)', (ncbi_tid, name, rank, parent_ncbi_tid, assembly_version, refseq_version, ftp_path))

    def get_blaze(self):
        return blaze.data('sqlite:///%s' % self.path)
