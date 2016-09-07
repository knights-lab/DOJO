from ninja_utils.utils import find_between

from .annotater import Annotater


class RefSeqAnnotater(Annotater):
    def __init__(self, extract_refseq_accession_version, prefixes, db, tree, depth=7, depth_force=True):
        Annotater.__init__(self)

        self.begin, self.end = extract_refseq_accession_version.split(',')

        prefixes = prefixes.split(',')
        if '*' in prefixes:
            self.set_prefix = set([_ for _ in db.refseq_prefix_mapper.keys()])
        else:
            self.set_prefix = set([_ for _ in prefixes])

        self.tree = tree
        self.db = db
        self.depth = depth
        self.depth_force = depth_force

    def annotate(self, gen_fasta):
        print(gen_fasta)
        for title, seq in gen_fasta:
            title = '>' + title
            refseq_accession_version = find_between(title, self.begin, self.end)
            if refseq_accession_version[:2] in self.set_prefix:
                ncbi_tid = self.db.get_ncbi_tid_from_refseq_accession_version(refseq_accession_version)
                print(refseq_accession_version)
                print(ncbi_tid)
                if ncbi_tid:
                    gg = self.tree.green_genes_lineage(ncbi_tid[0], depth=self.depth, depth_force=self.depth_force)
                    print(gg)
                    if gg:
                        gg = '; '.join(gg.split(';'))
                        header = 'ncbi_tid|%d|%s' % (ncbi_tid[0], title[1:])
                        yield '>%s\n%s\n' % (header, seq), '%s\t%s\n' % (header.split()[0], gg)
