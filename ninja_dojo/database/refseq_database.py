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
            c.execute('CREATE TABLE IF NOT EXISTS taxonomy('
                          'ncbi_tid INTEGER UNIQUE NOT NULL PRIMARY KEY,'
                          'name TEXT,'
                          'rank TEXT,'
                          'parent_ncbi_tid INTEGER'
                      ')')
            c.execute('CREATE TABLE IF NOT EXISTS refseq_version('
                          'ncbi_tid INTEGER,'
                          'refseq_version TEXT,'
                          'gi INTEGER,'
                          'length INTEGER,'
                          'FOREIGN KEY(ncbi_tid) REFERENCES taxonomy(ncbi_tid) ON DELETE CASCADE ON UPDATE CASCADE'
                      ')')
            c.execute('CREATE TABLE IF NOT EXISTS assembly_version('
                          'ncbi_tid INTEGER,'
                          'assembly_version TEXT,'
                          'ftp_path TEXT,'
                          'FOREIGN KEY(ncbi_tid) REFERENCES taxonomy(ncbi_tid) ON DELETE CASCADE ON UPDATE CASCADE'
                      ')')
            tree = NCBITree()
            assembly_map = RefseqAssemblyMap()
            refseq_catalog_map = RefseqCatalogMap()
            for ncbi_tid, rank, name, parent_ncbi_tid in tree.dfs_traversal():
                c.execute('INSERT INTO taxonomy VALUES (?,?,?,?)', (ncbi_tid, name, rank, parent_ncbi_tid,))
            conn.commit()
            for index, row in refseq_catalog_map.parse_df().iterrows():
                c.execute('INSERT INTO refseq_version VALUES (?,?,?,?)',
                          (row['ncbi_tid'], row['accession.version'], row['gi'], row['length'],))
            conn.commit()
            for index, row in assembly_map.df.iterrows():
                c.execute('INSERT INTO assembly_version VALUES (?,?,?)',
                          (row['taxid'], row['assembly_accession'], row['ftp_path'],))
            conn.comit()

    def get_blaze(self):
        return blaze.data('sqlite:///%s' % self.path)
