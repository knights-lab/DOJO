import multiprocessing
import click

from ninja_dojo.database import RefSeqDatabase
from ninja_trebuchet.utils import download_txt_url


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True)
def download_refseq_all(path):
    pool = multiprocessing.Pool(processes=4)
    rf = RefSeqDatabase()
    data = rf.get_blaze()

    ftp_view = data.tree[data.tree.ftp != '']
    for i in ftp_view:
        print(i)

if __name__ == '__main__':
    download_refseq_all()
