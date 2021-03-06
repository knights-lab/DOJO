#!/usr/bin/env python
import click
import urllib.request
import re

from collections import defaultdict
from ninja_utils.utils import line_bytestream_gzip, find_between

from dojo.database import RefSeqDatabase


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
                ncbi_tid = db.get_ncbi_tid_from_refseq_accession_version(refseq_accession_version.decode())
                if ncbi_tid:
                    title = b'ncbi_tid|%d|%s' % (ncbi_tid[0], line[1:])
                    data = b''
            else:
                title = b''
        elif title:
            data += line.strip()
    if title:
        yield title.strip(), data


@click.command()
@click.option('--output', type=click.Path(exists=False), default='-')
@click.option('--prefixes', default='*', help="Supply a comma-seperated list where the options are choices in ('AC', 'NC', 'NG', 'NM', 'NT', 'NW', 'NZ') e.g. NC,AC default=all")
@click.option('--kingdoms', default='*', help="Supply a comma-seperated list where the options are choices in ('archaea', 'bacteria', 'fungi', 'viral', 'protozoa') e.g. archaea,bacteria default=all")
def download_refseq(output, prefixes, kingdoms):
    url_dict = defaultdict(str,
        zip(('archaea', 'bacteria', 'fungi', 'viral', 'protozoa'), ('ftp://ftp.ncbi.nlm.nih.gov/refseq/release/archaea',
                                                                    'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/bacteria',
                                                                    'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/fungi',
                                                                    'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/viral',
                                                                    'ftp://ftp.ncbi.nlm.nih.gov/refseq/release/protozoa')))

    kingdoms = kingdoms.split(',')
    if '*' in kingdoms:
        urls = url_dict.values()
    else:
        urls = [url_dict[_] for _ in kingdoms]

    db = RefSeqDatabase()
    # check for the glob prefix
    prefixes = prefixes.split(',')
    if '*' in prefixes:
        prefix_set = set([str.encode(_) for _ in db.refseq_prefix_mapper.keys()])
    else:
        prefix_set = set([str.encode(_) for _ in prefixes])

    with click.open_file(output, 'wb') as outf:
        for url in urls:
            # Request the listing of the directory
            req = urllib.request.Request(url)
            string = urllib.request.urlopen(req).read().decode('utf-8')

            # Grab the filename ending with catalog.gz
            pattern_cat = re.compile('[a-zA-Z0-9.-]*.genomic.fna.gz')
            filelist = pattern_cat.findall(string)

            for file in filelist:
                req_file = urllib.request.Request('%s/%s' % (url, file))
                with urllib.request.urlopen(req_file, 'rb') as ftp_stream:
                    fasta_fh = line_bytestream_gzip(ftp_stream)
                    for title, seq in binary_fasta(fasta_fh, db, prefix_set):
                        outf.write(b'>%s\n%s\n' % (title, seq))


if __name__ == '__main__':
    download_refseq()
