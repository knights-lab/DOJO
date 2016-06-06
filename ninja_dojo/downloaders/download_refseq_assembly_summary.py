import os

from ninja_trebuchet.factory import Downloadable
from ninja_trebuchet.utils import download_txt_url

from .. import SETTINGS


class RefseqSummary(Downloadable):
    def __init__(self, _refseq_summary_url=SETTINGS.settings['refseq_summary_url'], _refseq_summary_dir=SETTINGS.settings['refseq_summary_dir']):
        super().__init__(_refseq_summary_dir)
        self.urls = _refseq_summary_url

    def download(self):
        for url in self.urls:
            file_name = url.split('/')[-1]
            download_txt_url(os.path.join(self.path, file_name), url)
