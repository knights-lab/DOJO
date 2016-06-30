#!/usr/bin/env python
import multiprocessing
import os
import click
from collections import Counter

from ninja_dojo.database import RefSeqDatabase
from ninja_dojo.taxonomy import NCBITree
from ninja_trebuchet.utils import download_txt_url


def yield_ftp_links(blaze, specified_kingdoms, tree):
    for i in blaze:
        # ncbi_id, name, rank, parent_ncbi_id, assembly_acc, refseq_version, ftp_link
        if i[5][:2] == 'NC':
            if i[2] == 'species':
                kingdom = tree.gg_lineage(i[0]).split(';')[0]
                if kingdom in specified_kingdoms:
                    ftp_link = i[-1]
                    yield ftp_link


def download_ftp_link(ftp_link):
    assembly_name = ftp_link.split('/')[-1]
    assembly_name += '_genomic.fna.gz'
    try:
        download_txt_url(os.path.join(os.getcwd(), assembly_name), ftp_link + '/' + assembly_name)
    except:
        print('FTP failed for some reason on this link: %s' % ftp_link + '/' + assembly_name)


@click.command()
# @click.argument('path', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True)
def download_refseq_all(verbose):
    pool = multiprocessing.Pool(processes=4)
    rf = RefSeqDatabase()
    data = rf.get_blaze()
    tree = NCBITree()
    specified_kingdoms = {'k__Bacteria', 'k__Viruses', 'k__Archaea'}
    kingdoms = []

    ftp_view = data.tree[data.tree.ftp != '' and data.tree.refseq_version != '']
    ftp_links = yield_ftp_links(ftp_view, specified_kingdoms, tree)
    # ftp_test = [next(ftp_links) for _ in range(10)]

    pool.map(download_ftp_link, ftp_links)
    print('Done')

    # c = Counter(kingdoms)
    # print(c)
    # Note: 17 Archaea, 208 Bacteria, 4982 Viruses

if __name__ == '__main__':
    download_refseq_all()
