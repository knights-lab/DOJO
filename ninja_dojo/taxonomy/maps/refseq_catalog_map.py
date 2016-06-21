import os
import pandas as pd
from collections import defaultdict
import csv

from ninja_trebuchet.factory import Pickleable, download

from ... import SETTINGS, LOGGER
from ...downloaders import RefseqCatalog


class RefseqCatalogMap(Pickleable):
    def __init__(self, _downloaders=(RefseqCatalog())):
        self._downloaders = _downloaders
        super().__init__(SETTINGS, LOGGER)

    @download
    def _parse(self):
        self.taxid2refseq_accession = defaultdict(int)
        with open(os.path.join(self._downloaders[0].path, 'refseq_catalog.csv')) as inf:
            reader = csv.reader(inf)
            next(reader)
            for row in reader:
                self.taxid2refseq_accession[row[1][:row[1].find('.')]] = row[0]

    def parse_df(self):
        df = pd.read_csv(os.path.join(self._downloaders[0].path, 'refseq_catalog.csv'), sep=',')
        return df

    # def __getstate__(self):
    #     d = dict(self.__dict__)
    #     del d['df']
    #     return d
    #
    # def __setstate__(self, d):
    #     # TODO add try/except
    #     self.__dict__.update(d)
    #     self.df = self.parse_df()
