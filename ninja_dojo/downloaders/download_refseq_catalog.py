import urllib.request
import tarfile
import re

from ninja_trebuchet.factory import Downloadable

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
        pattern = re.compile('[a-zA-Z0-9.-]*.catalog.gz')
        filelist = pattern.findall(string)

        # Append the url and the filename
        req_file = urllib.request.Request(self.urls[0] + filelist[0])

        # Stream and extract
        with urllib.request.urlopen(req_file, 'rb') as ftp_stream:
            tfile = tarfile.open(fileobj=ftp_stream, mode='r|gz')
            tfile.extractall(self.path)
