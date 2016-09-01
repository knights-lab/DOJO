from ninja_utils.utils import find_between

from ..database import RefSeqDatabase
from ..taxonomy import NCBITree


def refseq_annotater(gen_fasta, prefixes, extract_refseq_id, depth=7, depth_force=True):
    begin, end = extract_refseq_id.split(',')

    db = RefSeqDatabase()
    # check for the glob prefix
    prefixes = prefixes.split(',')
    if '*' in prefixes:
        set_prefix = set([_ for _ in db.refseq_prefix_mapper.keys()])
    else:
        set_prefix = set([_ for _ in prefixes])

    tree = NCBITree()
    for title, seq in gen_fasta:
        title = '>' + title
        refseq_accession_version = find_between(title, begin, end)
        if refseq_accession_version[:2] in set_prefix:
            ncbi_tid = db.get_ncbi_tid_from_refseq_accession_version(refseq_accession_version)
            if ncbi_tid:
                gg = tree.green_genes_lineage(ncbi_tid[0], depth=depth, depth_force=depth_force)
                if gg:
                    gg = '; '.join(gg.split(';'))
                    header = 'ncbi_tid|%d|%s' % (ncbi_tid[0], title[1:])
                    yield '>%s\n%s\n' % (header, seq), '%s\t%s\n' % (header.split()[0], gg)
