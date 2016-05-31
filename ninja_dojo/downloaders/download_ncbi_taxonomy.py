import urllib.request
import tarfile

from ninja_trebuchet.factory import Downloadable

from .. import SETTINGS


class NCBITaxdmp(Downloadable):
    def __init__(self, _ncbi_taxdmp_url=SETTINGS.settings['ncbi_taxdmp_url'], _ncbi_taxdmp_dir=SETTINGS.settings['ncbi_taxdmp_dir']):
        super().__init__(_ncbi_taxdmp_dir)
        self.urls = [_ncbi_taxdmp_url]

    def download(self):
        req = urllib.request.Request(self.urls[0])
        with urllib.request.urlopen(req, 'rb') as ftp_stream:
            tfile = tarfile.open(fileobj=ftp_stream, mode='r|gz')
            tfile.extractall(self.path)


def main():
    NCBITaxdmp().run()

if __name__ == '__main__':
    main()
