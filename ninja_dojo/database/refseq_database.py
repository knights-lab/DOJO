import sqlite3
import os
import blaze
import json

from .. import SETTINGS, LOGGER
from ..taxonomy import NCBITree
from ..taxonomy.maps import RefseqAssemblyMap, RefseqCatalogMap


class RefSeqDatabase:
    def __init__(self, _db_dir=SETTINGS.get_path('db_dir'), _ftp_prefix=SETTINGS.settings['refseq_ftp_prefix']):
        self.path = os.path.join(_db_dir, 'refseq.db')
        if not os.path.exists(self.path):
            self._create(_db_dir, _ftp_prefix)
        # suffix
        self.refseq_prefix = {}
        self.assembly_prefix = {}
        self.blaze = blaze.data('sqlite:///%s' % self.path)

    def get_ftp_link(self, ncbi_tid):
        ftp_suffix = 's'
        assembly_accession_version = ncbi_tid
        for row in self.get_assembly_row(ncbi_tid):
            yield '%s%s_%s' % (self.ftp_prefix, assembly_accession_version, ftp_suffix)

    def get_assembly_row(self, ncbi_tid):
        pass

    @classmethod
    def _create(cls, db_dir, ftp_prefix):
        with sqlite3.connect(os.path.join(db_dir, 'refseq.db')) as conn:
            c = conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS taxonomy('
                      'ncbi_tid INTEGER UNIQUE NOT NULL PRIMARY KEY,'
                      'name TEXT,'
                      'rank INTEGER,'
                      'parent_ncbi_tid INTEGER'
                      ')')
            c.execute('CREATE TABLE IF NOT EXISTS refseq('
                      'ncbi_tid INTEGER,'
                      'refseq_prefix INTEGER,'
                      'refseq_accession TEXT,'
                      'refseq_version INTEGER,'
                      'gi INTEGER,'
                      'length INTEGER,'
                      'FOREIGN KEY(ncbi_tid) REFERENCES taxonomy(ncbi_tid) ON DELETE CASCADE ON UPDATE CASCADE'
                      ')')
            c.execute('CREATE TABLE IF NOT EXISTS assembly('
                      'ncbi_tid INTEGER,'
                      'assembly_accession TEXT,'
                      'assembly_version INTEGER,'
                      'ftp_suffix TEXT,'
                      'FOREIGN KEY(ncbi_tid) REFERENCES taxonomy(ncbi_tid) ON DELETE CASCADE ON UPDATE CASCADE'
                      ')')
            tree = NCBITree()
            assembly_map = RefseqAssemblyMap()
            refseq_catalog_map = RefseqCatalogMap()

            # prefix mapper
            refseq_prefix_counter = 0
            refseq_prefix_mapper = {}

            # rank mapper
            ncbi_rank_mapper = dict(zip(('superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'),
                    range(7)))
            ncbi_rank_counter = -1

            for ncbi_tid, rank, name, parent_ncbi_tid in tree.dfs_traversal():
                if rank not in ncbi_rank_mapper:
                    ncbi_rank_mapper[rank] = ncbi_rank_counter
                    ncbi_rank_counter -= 1
                c.execute('INSERT INTO taxonomy VALUES (?,?,?,?)', (ncbi_tid, name, ncbi_rank_mapper[rank], parent_ncbi_tid,))
            for index, row in refseq_catalog_map.parse_df().iterrows():
                refseq_accession_version = row['accession.version']
                refseq_prefix_accession, refseq_version = refseq_accession_version.split('.')
                refseq_prefix, refseq_accession = refseq_prefix_accession.split('_')
                if refseq_prefix not in refseq_prefix_mapper:
                    refseq_prefix_mapper[refseq_prefix] = refseq_prefix_counter
                    refseq_prefix_counter += 1
                c.execute('INSERT INTO refseq VALUES (?,?,?,?,?,?)',
                          (row['ncbi_tid'], refseq_prefix_mapper[refseq_prefix], refseq_accession, int(refseq_version), row['gi'], row['length'],))
            for index, row in assembly_map.parse_df().iterrows():
                assembly_accession, assembly_version = row['assembly_accession'].split('.')
                ftp_suffix = row['ftp_path'].split('_')[-1]
                c.execute('INSERT INTO assembly VALUES (?,?,?,?)',
                          (row['taxid'], assembly_accession, int(assembly_version), ftp_suffix,))
            c.execute('CREATE INDEX parent_ncbi_tid_index on taxonomy(parent_ncbi_tid)')
            c.execute('CREATE INDEX refseq_index on refseq(refseq_prefix, refseq_accession, refseq_version)')
            c.execute('CREATE INDEX gi_index on refseq(gi)')
            c.execute('CREATE INDEX assembly_index on assembly(assembly_accession, assembly_version)')
            metadata = dict(zip(('ncbi_rank_mapper', 'refseq_prefix_mapper', 'ftp_prefix'),
                                (ncbi_rank_mapper, refseq_prefix_mapper, ftp_prefix)))
            with open(os.path.join(db_dir, 'metadata.json'), 'w') as outfile:
                json.dump(metadata, outfile)

    def get_ncbi_tid(self, refseq_accession_version):
        return self.blaze.refseq_version[self.blaze.refseq_version.refseq_version == refseq_accession_version]
