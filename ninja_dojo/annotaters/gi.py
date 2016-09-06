from ninja_utils.utils import find_between

from .annotater import Annotater
from ..database import RefSeqDatabase
from ..taxonomy import NCBITree


class GIAnnotater(Annotater):
    def __init__(self, extract_gi, db: RefSeqDatabase, tree: NCBITree, depth=7, depth_force=True):
        Annotater.__init__(self)

        self.begin, self.end = extract_gi.split(',')

        self.tree = tree
        self.db = db
        self.depth = depth
        self.depth_force = depth_force

    def annotate(self, gen_fasta):
        for title, seq in gen_fasta:
            title = '>' + title
            gi = find_between(title, self.begin, self.end)
            ncbi_tid = self.db.get_ncbi_tid_from_gi(gi)
            if ncbi_tid:
                gg = self.tree.green_genes_lineage(ncbi_tid[0], depth=self.depth, depth_force=self.depth_force)
                if gg:
                    gg = '; '.join(gg.split(';'))
                    header = 'ncbi_tid|%d|%s' % (ncbi_tid[0], title[1:])
                    yield '>%s\n%s\n' % (header, seq), '%s\t%s\n' % (header.split()[0], gg)
