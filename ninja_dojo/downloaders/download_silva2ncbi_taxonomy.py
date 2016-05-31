import os

from ninja_trebuchet.factory import Downloadable
from ninja_trebuchet.utils import download_txt_url

from .. import SETTINGS


class SilvaMapping(Downloadable):
    def __init__(self, _silva_taxdmp_urls=SETTINGS.settings['silva_taxdmp_urls'], _silva_taxdmp_dir=SETTINGS.settings['silva_taxdmp_dir']):
        super().__init__(_silva_taxdmp_dir)
        self.urls = _silva_taxdmp_urls

    def download(self):
        for url in self.urls:
            file_name = url.split('/')[-1]
            download_txt_url(os.path.join(self.path, file_name), url)


def main():
    SilvaMapping().run()

if __name__ == '__main__':
    main()
