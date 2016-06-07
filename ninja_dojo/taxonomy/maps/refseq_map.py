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
        with open(self._downloader.path, 'r') as inf:
            csv_file = csv.reader(inf, delimiter='\t')

            # Checking for a header file
            for row in csv_file:
                try:
                    ncbi_taxon_id = int(row[1])
                    self.img2taxon_id[int(row[0])] = ncbi_taxon_id
                except ValueError as e:
                    continue

        self.taxon_id2img = reverse_dict(self.img2taxon_id)
