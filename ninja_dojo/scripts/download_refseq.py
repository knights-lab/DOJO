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


def binary_fasta(fh):
    """
    :return: tuples of (title, seq)
    """
    title = b''
    data = b''
    for line in fh:
        if line[:1] == b'>':
            if title:
                yield title.strip(), data
            line_split = line.split(b'|')
            if line_split[3][:2] in {b'NC', b'AC'}:
                title = line[1:]
                data = b''
            else:
                title = b''
        elif title:
            data += line.strip()
    if title:
        yield title.strip(), data


@click.command()
# @click.argument('path', type=click.Path(exists=True))
def download_refseq():
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
    blaze = db.get_blaze()

    for file in filelist:
        req_file = urllib.request.Request('%s/%s' % (url, file))
        with urllib.request.urlopen(req_file, 'rb') as ftp_stream:
            fasta_fh = line_bytestream_gzip(ftp_stream)
            for title, seq in binary_fasta(fasta_fh):
                print(title, seq)


if __name__ == '__main__':
    download_refseq()
