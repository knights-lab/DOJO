#!/usr/bin/env python
import click
import urllib.request
import re
import os

from ninja_trebuchet.utils import line_bytestream_gzip

from ninja_dojo.taxonomy import NCBITree
from ninja_dojo.database import RefSeqDatabase

#
# #!/usr/bin/env bash
#
# #wget "ftp://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt"
# #awk -F "\t" '$12=="Complete Genome" && $11=="latest"{print $20}' assembly_summary.txt > ftpdirpaths
# #awk 'BEGIN{FS=OFS="/";filesuffix="genomic.fna.gz"}{ftpdir=$0;asm=$6;file=asm"_"filesuffix;print ftpdir,file}' ftpdirpaths > ftpfilepaths
#
# #wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/archaea/*.genomic.fna.gz"
# #wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/bacteria/*.genomic.fna.gz"
# #wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/fungi/*.genomic.fna.gz"
# #wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral/*.genomic.fna.gz"
# #wget "ftp://ftp.ncbi.nlm.nih.gov/refseq/release/protozoa/*.genomic.fna.gz"
#
# zcat *.gz > ncbi_cat.refseq.fna
# #project/flatiron/ben/bin/blast/dustmasker -in ncbi.fna -infmt fasta -outfmt fasta -out ncbi.masked.fna


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def binary_fasta(fh, db, prefix_set):
    """
    :return: tuples of (title, seq)
    """
    title = b''
    data = b''
    for line in fh:
        if line[:1] == b'>':
            if title:
                yield title.strip(), data
            # line_split = line.split(b'|')
            refseq_accession_version = find_between(line, b'ref|', b'|')
            if refseq_accession_version[:2] in prefix_set:
                ncbi_tid = db.get_ncbi_tid_from_refseq_accession(find_between(refseq_accession_version, b'_', b'.').decode())
                if ncbi_tid:
                    title = b'nbci_tid|%d|%s' % (ncbi_tid[0], line[1:])
                    data = b''
            else:
                title = b''
        elif title:
            data += line.strip()
    if title:
        yield title.strip(), data


@click.command()
@click.argument('output', type=click.Path(exists=False), default='-')
@click.argument('prefixes', default='NC,AC')
def download_refseq(output, prefixes):
    urls = ['ftp://ftp.ncbi.nlm.nih.gov/refseq/release/archaea',
            'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/bacteria',
            'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/fungi',
            'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral',
            'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/protozoa']
    url = urls[0]
    # Request the listing of the directory
    req = urllib.request.Request(url)
    string = urllib.request.urlopen(req).read().decode('utf-8')

    # Grab the filename ending with catalog.gz
    pattern_cat = re.compile('[a-zA-Z0-9.-]*.genomic.fna.gz')
    filelist = pattern_cat.findall(string)

    db = RefSeqDatabase()

    prefix_set = set([str.encode(_) for _ in prefixes.split(',')])

    with click.open_file(output, 'wb') as outf:
        for file in filelist:
            req_file = urllib.request.Request('%s/%s' % (url, file))
            with urllib.request.urlopen(req_file, 'rb') as ftp_stream:
                fasta_fh = line_bytestream_gzip(ftp_stream)
                for title, seq in binary_fasta(fasta_fh, db, prefix_set):
                    outf.write(b'>%s/n%s/n' % (title, seq))


if __name__ == '__main__':
    download_refseq()
