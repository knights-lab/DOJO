#!/usr/bin/env python
import click
import re

from dojo.database import RefSeqDatabase
from dojo.taxonomy import NCBITree



@click.command()
@click.option('-i', '--input', type=click.File('r'))
@click.option('-o', '--output', type=click.File('w'), default='-')
def refseq_get_ftp_links_from_file(input, output):
    db = RefSeqDatabase()
    tree = NCBITree()

    ncbi_tid_set = set()
    for line in input:
        line = str.replace(line, ' unclassified', '')
        line = str.replace(line, 'cf', '')

        [ncbi_tid_set.add(_[0]) for _ in db.yield_ncbi_tid_row_from_name(line.strip())]

    ncbi_tid_successors = set()
    # How many total strains are there in HMP?
    #
    for ncbi_tid in ncbi_tid_set:
        #TODO Switch the tree around - predecessor and successors
        [ncbi_tid_successors.add(_) for _ in tree.tree.predecessors_iter(ncbi_tid) if not _ in ncbi_tid_set]

    ncbi_tid_set = set.union(ncbi_tid_set, ncbi_tid_successors)
    output.write('ncbi_tid,gg_lineage,ftp_link\n')
    for ncbi_tid in ncbi_tid_set:
        [output.write('%s,%s,%s\n' % (ncbi_tid, tree.gg_lineage(ncbi_tid), ftp_link)) for ftp_link in db.yield_ftp_links(ncbi_tid)]

if __name__ == '__main__':
    refseq_get_ftp_links_from_file()

