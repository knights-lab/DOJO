#!/usr/bin/env python
import os
from collections import defaultdict
from glob import glob

import click
import csv

from ninja_utils.parsers import FASTQ

from ninja_dojo.taxonomy.maps import RefseqCatalogMap


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True)
def extract_ncbi_tid(path, verbose):
    rf = RefseqCatalogMap()
    for file in glob(os.path.join(os.path.abspath(path), '*.gold')):
        tid_counts = defaultdict(int)
        with open(os.path.join(path, '%s.fastq' % os.path.basename(file).split('.')[0])) as fastq_fh:
            with open(os.path.join(path, '%s.ninja.fastq') % os.path.basename(file).split('.')[0], 'w') as outf:
                for header, seq, qual in FASTQ(fastq_fh).read():
                    header_arr = header.split('|')
                    if len(header_arr) > 3:
                        refseq_acc = header_arr[3]
                        acc = refseq_acc[:refseq_acc.find('.')]
                        tid = rf.refseq_accession2ncbi_tid[acc]
                        if not tid == 0:
                            outf.write('@ncbi_tid|%s|%s\n' % (tid, header))
                            outf.write(seq + '\n')
                            outf.write('+\n%s\n' % qual)
                            tid_counts[tid] += 1

        with open(os.path.join(path, '%s.ninja.gold') % os.path.basename(file).split('.')[0], 'w') as outf:
            writer = csv.writer(outf)
            writer.writerow(('ncbi_tid', 'count'))
            for kv in tid_counts.items():
                writer.writerow(kv)


if __name__ == '__main__':
    extract_ncbi_tid()
