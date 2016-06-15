import urllib.request
import os
import re
import csv

from ninja_trebuchet.factory import Downloadable
from ninja_trebuchet.utils import line_bytestream_gzip

from .. import SETTINGS


def xx():
    while True:
        x = yield
        yield

@coroutine
def broadcast(targets):
    while True:
        item = yield
        for target in targets:
            target.send(item)

def xsftp(ftp_stream):
    x = xx()
    for ss in line_bytestream_gzip(ftp_stream):
        row = ss.split(b'\t')
        if row[2][:2] == b'NC':
            c_line = yield
            yield c_line


class RefseqCatalog(Downloadable):
    def __init__(self, _refseq_catalog_urls=SETTINGS.settings['refseq_catalog_urls'], _refseq_catalog_dir=SETTINGS.settings['refseq_catalog_dir']):
        super().__init__(_refseq_catalog_dir)
        self.urls = _refseq_catalog_urls

    def download(self):
        # Request the listing of the directory
        req = urllib.request.Request(self.urls[0])
        string = urllib.request.urlopen(req).read().decode('utf-8')

        # Grab the filename ending with catalog.gz
        pattern_cat = re.compile('[a-zA-Z0-9.-]*.catalog.gz')
        filelist = pattern_cat.findall(string)

        # Append the url and the filename
        req_file = urllib.request.Request(self.urls[0] + filelist[0])

        # pref = {b'NC', b'AC'}

        # Stream and extract
        with urllib.request.urlopen(req_file, 'rb') as ftp_stream:
            with open(os.path.join(self.path, 'refseq_catalog.txt'), 'wb') as out_fh:
                # out_fh.write(b'\t'.join([
                #     b'ncbi_tid',
                #     b'accession.version',
                #     b'gi',
                #     b'length'
                # ]) + b'\n')
                # for line in line_bytestream_gzip(ftp_stream):
                #     row = line.split(b'\t')
                #     if row[2][:2] == b'NC':
                #         # ncbi_tid, accession.version, gi, length
                #         out_fh.write(row[0] + b'\t' + row[2] + b'\t' + row[3] + b'\t' + row[6] + b'\n')
                out_fh.writelines(xsftp(ftp_stream))
