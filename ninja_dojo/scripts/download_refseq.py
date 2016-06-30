#!/usr/bin/env python
import click
import urllib.request
import re

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


@click.command()
# @click.argument('path', type=click.Path(exists=True))
def download_refseq():
    print('Hello, World!')
    # Request the listing of the directory
    req = urllib.request.Request('ftp://ftp.ncbi.nlm.nih.gov/refseq/release/archaea')
    string = urllib.request.urlopen(req).read().decode('utf-8')

    # Grab the filename ending with catalog.gz
    pattern_cat = re.compile('[a-zA-Z0-9.-]*.genomic.fna.gz')
    filelist = pattern_cat.findall(string)
    print(filelist)


if __name__ == '__main__':
    download_refseq()
