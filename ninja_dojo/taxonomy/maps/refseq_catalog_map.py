import os
import pandas as pd
from collections import defaultdict
import csv

from ninja_trebuchet.factory import Pickleable, download
from ninja_trebuchet.utils import reverse_dict

from ... import SETTINGS, LOGGER
from ...downloaders import RefseqCatalog


class RefseqCatalogMap(Pickleable):
    def __init__(self, _downloaders=(RefseqCatalog(),)):
        self._downloaders = _downloaders
        super().__init__(SETTINGS, LOGGER)

    @download
    def _parse(self):
        self.refseq_accession2ncbi_tid = defaultdict(int)
        with open(os.path.join(self._downloaders[0].path, 'refseq_catalog.csv')) as inf:
            reader = csv.reader(inf)
            next(reader)
            for row in reader:
                self.refseq_accession2ncbi_tid[row[1][:row[1].find('.')]] = int(row[0])
        # self.ncbi_tid2refseq_accession = defaultdict(str, reverse_dict(self.refseq_accession2ncbi_tid))

    def parse_df(self):
        df = pd.read_csv(os.path.join(self._downloaders[0].path, 'refseq_catalog.csv'), sep=',')
        return df

    def __getstate__(self):
        d = dict(self.__dict__)
        # del d['ncbi_tid2refseq_accession']
        return d

    def __setstate__(self, d):
        # TODO add try/except
        # d['ncbi_tid2refseq_accession'] = defaultdict(str, reverse_dict(d['refseq_accession2ncbi_tid']))
        self.__dict__.update(d)
