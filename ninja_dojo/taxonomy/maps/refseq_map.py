import csv
import os

from ninja_trebuchet.utils import reverse_dict
from ninja_trebuchet.factory import Pickleable, download

from ... import SETTINGS, LOGGER
from ...downloaders import RefseqSummary


class RefseqMap(Pickleable):
    def __init__(self, _downloader=RefseqSummary()):
        self._downloader = _downloader
        super().__init__(SETTINGS, LOGGER)

    @download
    def _parse(self):
        # init variables
        with open(os.path.join(self._downloader.path, 'assembly_summary_refseq.txt'), 'r') as inf:
            csv_file = csv.reader(inf, delimiter='\t')

            # Checking for a header file
            for row in csv_file:
                print(row)

