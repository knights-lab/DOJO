import urllib.request
import os
import re

from ninja_utils.factory import Downloadable
from ninja_utils.utils import line_bytestream_gzip

from .. import SETTINGS


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

        pref = {b'AC', b'NC', b'NG', b'NT', b'NW', b'NS', b'NZ', b'NM'}

        # Stream and extract
        with urllib.request.urlopen(req_file, 'rb') as ftp_stream:
            with open(os.path.join(self.path, 'refseq_catalog.csv'), 'wb') as out_fh:
                out_fh.write(b','.join([
                    b'ncbi_tid',
                    b'accession.version',
                    b'gi',
                    b'length'
                ]) + b'\n')
                for line in line_bytestream_gzip(ftp_stream):
                    row = line.split(b'\t')
                    if row[2][:2] in pref:
                        # ncbi_tid, accession.version, gi, length
                        out_fh.write(row[0] + b',' + row[2] + b',' + row[3] + b',' + row[6] + b'\n')
