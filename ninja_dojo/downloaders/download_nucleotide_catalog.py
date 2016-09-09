import urllib.request
import os
import re

from ninja_utils.factory import Downloadable
from ninja_utils.utils import line_bytestream_gzip

from .. import SETTINGS


class NucleotideCatalog(Downloadable):
    def __init__(self, _nucleotide_catalog_urls=SETTINGS.settings['nucleotide_catalog_urls'], _nucleotide_catalog_dir=SETTINGS.settings['nucleotide_catalog_dir']):
        super().__init__(_nucleotide_catalog_dir)
        self.urls = _nucleotide_catalog_urls

    def download(self):
        # Request the listing of the directory
        req = urllib.request.Request(self.urls[0])
        string = urllib.request.urlopen(req).read().decode('utf-8')

        # Grab the filename ending with catalog.gz
        pattern_cat = re.compile('[a-zA-Z0-9.-]*nucl_[a-zA-Z0-9.-]*taxid.gz')
        filelist = pattern_cat.findall(string)

        # Stream and extract
        with open(os.path.join(self.path, 'nucleotide_catalog.tsv'), 'wb') as out_fh:
            out_fh.write(b'\t'.join([
                b'accession',
                b'accession.version',
                b'taxid',
                b'gi'
            ]) + b'\n')
            for base in set(filelist):
                url = self.urls[0] + base
                req_file = urllib.request.Request(url)
                with urllib.request.urlopen(req_file, 'rb') as ftp_stream:
                    gen = line_bytestream_gzip(ftp_stream)
                    next(gen)
                    for line in gen:
                        out_fh.write(line)
