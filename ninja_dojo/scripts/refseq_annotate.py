#!/usr/bin/env python
import click

from ninja_utils.parsers import FASTA
from ninja_utils.utils import find_between

from ninja_dojo.database import RefSeqDatabase


@click.command()
@click.option('-i', '--input', type=click.File('r'))
@click.option('-o', '--output', type=click.File('w'), default='-')
@click.option('--prefixes', default='*', help="Supply a comma-seperated list where the options are choices"
                                              " in ('AC', 'NC', 'NG', 'NM', 'NT', 'NW', 'NZ') e.g. NC,AC default=all")
def refseq_annotate(input, output, prefixes):
    db = RefSeqDatabase()

    # check for the glob prefix
    prefixes = prefixes.split(',')
    if '*' in prefixes:
        prefix_set = set([_ for _ in db.refseq_prefix_mapper.keys()])
    else:
        prefix_set = set([_ for _ in prefixes])

        inf_fasta = FASTA(input)
        for title, seq in inf_fasta.read():
            refseq_accession_version = find_between(title, 'ref|', '|')
            if refseq_accession_version[:2] in prefix_set:
                ncbi_tid = db.get_ncbi_tid_from_refseq_accession_version(refseq_accession_version)
                if ncbi_tid:
                    title = 'ncbi_tid|%d|%s' % (ncbi_tid[0], title)
                output.write('>%s\n%s\n' % (title, seq))


if __name__ == '__main__':
    refseq_annotate()
