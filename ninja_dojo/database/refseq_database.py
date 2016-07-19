import sqlite3
import os
import json

from ninja_utils.utils import reverse_dict

from .. import SETTINGS, LOGGER
from ..taxonomy import NCBITree
from ..taxonomy.maps import RefseqAssemblyMap, RefseqCatalogMap


class RefSeqDatabase:
    def __init__(self, _db_dir=SETTINGS.get_path('db_dir'), _ftp_prefix=SETTINGS.settings['refseq_ftp_prefix']):
        self.path = os.path.join(_db_dir, 'refseq.db')
        if not os.path.exists(self.path):
            self._create(_db_dir, _ftp_prefix)

        try:
            with open(os.path.join(_db_dir, 'metadata.json')) as data:
                metadata = json.load(data)
        except FileNotFoundError as e:
            raise e

        self.ftp_prefix = metadata['ftp_prefix']
        self.ncbi_rank_mapper = metadata['ncbi_rank_mapper']
        self.refseq_prefix_mapper = metadata['refseq_prefix_mapper']

        self.conn = sqlite3.connect(os.path.join(_db_dir, 'refseq.db'))
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()

    def query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        return cur

    def yield_ftp_links(self, ncbi_tid):
        cur = self.conn.cursor()

        # ncbi_tid, assembly_accession, assembly_version, ftp_suffix
        cur.execute('SELECT * FROM assembly WHERE ncbi_tid = ?', (ncbi_tid,))

        for row in cur:
            yield '%s%s_%s' % (self.ftp_prefix, '%s.%d' % (row[1], row[2]), row[3])

    def yield_ncbi_tid_and_ftp_links_from_name(self, query):
        ncbi_tids = set([row[0] for row in self.yield_ncbi_tid_row_from_name(query)])
        for ncbi_tid in ncbi_tids:
            for link in self.yield_ftp_links(ncbi_tid):
                yield ncbi_tid, link

    def yield_ncbi_tid_row_from_name(self, query):
        cur = self.conn.cursor()

        # ncbi_tid, name, rank, parent_ncbi_tid
        cur.execute("SELECT * FROM taxonomy WHERE name LIKE " + "'%" + query + "%'")

        for row in cur:
            yield row

    def yield_ncbi_tid_row_from_name_and_rank(self, query, rank):
        cur = self.conn.cursor()

        rank = self.ncbi_rank_mapper[rank]

        # ncbi_tid, name, rank, parent_ncbi_tid
        cur.execute("SELECT * FROM taxonomy WHERE name LIKE " + "'%" + query + "%'" + "AND rank = ?", (rank,))

        for row in cur:
            yield row

    def yield_ncbi_tid_and_refseq_accession_version_from_name(self, query):
        ncbi_tids = set([row[0] for row in self.yield_ncbi_tid_row_from_name(query)])

        cur = self.conn.cursor()

        for ncbi_tid in ncbi_tids:
            cur.execute('SELECT * FROM refseq WHERE ncbi_tid = ?', (ncbi_tid,))
            refseq_mapper = reverse_dict(self.refseq_prefix_mapper)

            # ncbi_tid, refseq_prefix, refseq_accession, refseq_version, gi, length
            for row in cur:
                yield row[0], '%s_%s.%d' % (refseq_mapper[1], row[2], row[3])

    def yield_ncbi_tid_and_refseq_accession_version_from_name_and_refseq_prefix(self, query, refseq_prefix):
        ncbi_tids = set([row[0] for row in self.yield_ncbi_tid_row_from_name(query)])
        refseq_mapper = reverse_dict(self.refseq_prefix_mapper)
        cur = self.conn.cursor()

        for ncbi_tid in ncbi_tids:
            cur.execute('SELECT * FROM refseq WHERE ncbi_tid = ? AND refseq_prefix = ?', (ncbi_tid, self.refseq_prefix_mapper[refseq_prefix],))
            # ncbi_tid, refseq_prefix, refseq_accession, refseq_version, gi, length
            for row in cur:
                yield row[0], '%s_%s.%d' % (refseq_mapper[row[1]], row[2], row[3])




    #TODO: Do this later
    def get_ncbi_tid_from_gi(self, gi):
        cur = self.conn.cursor()

        # ncbi_tid, refseq_prefix, refseq_accession, refseq_version, gi, length
        cur.execute('SELECT ncbi_tid FROM refseq WHERE gi = ?',
                    (gi,))
        return cur.fetchone()

    def get_ncbi_tid_from_refseq_accession_version(self, refseq_accession_version):
        cur = self.conn.cursor()
        try:
            refseq_prefix = self.refseq_prefix_mapper[refseq_accession_version[:2]]
        except KeyError as e:
            raise e

        refseq_accession, refseq_version = refseq_accession_version[3:].split('.')

        # ncbi_tid, refseq_prefix, refseq_accession, refseq_version, gi, length
        cur.execute('SELECT ncbi_tid FROM refseq WHERE refseq_prefix = ? AND refseq_accession = ? AND refseq_version = ?',
                    (refseq_prefix, refseq_accession, int(refseq_version)))
        return cur.fetchone()

    def get_ncbi_tid_from_refseq_accession(self, refseq_accession):
        cur = self.conn.cursor()

        # ncbi_tid, refseq_prefix, refseq_accession, refseq_version, gi, length
        cur.execute('SELECT ncbi_tid FROM refseq WHERE refseq_accession = ?',
                    (refseq_accession,))
        return cur.fetchone()

    def get_ncbi_tid_row(self, ncbi_tid):
        cur = self.conn.cursor()

        # ncbi_tid, name, rank, parent_ncbi_tid
        cur.execute(
            'SELECT * FROM taxonomy WHERE ncbi_tid = ?',
            (ncbi_tid,))

        return cur.fetchone()

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
                # remove the underscore and start at the end
                ftp_suffix = row['ftp_path'][row['ftp_path'].find(row['assembly_accession'])+len(row['assembly_accession'])+1:]
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

    def __del__(self):
        self.conn.close()
