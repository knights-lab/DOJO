from ninja_utils.utils import find_between

from .annotater import Annotater


class NCBIAnnotater(Annotater):
    def __init__(self, extraction_ncbi_tid, tree, depth=7, depth_force=True):
        Annotater.__init__(self)

        self.begin, self.end = extraction_ncbi_tid.split(',')

        self.tree = tree
        self.depth = depth
        self.depth_force = depth_force

    def annotate(self, gen_fasta):
        for title, seq in gen_fasta:
            title = '>' + title
            # Extract NCBI TID and Convert to INT
            ncbi_tid = int(find_between(title, self.begin, self.end))
            if ncbi_tid:
                gg = self.tree.green_genes_lineage(ncbi_tid, depth=self.depth, depth_force=self.depth_force)
                if gg:
                    gg = '; '.join(gg.split(';'))
                    header = 'ncbi_tid|%d|%s' % (ncbi_tid, title[1:])
                    yield '>%s\n%s\n' % (header, seq), '%s\t%s\n' % (header.split()[0], gg)
