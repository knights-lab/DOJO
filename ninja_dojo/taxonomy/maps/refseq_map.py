import bcolz
import os
import pandas as pd
from collections import defaultdict

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
        self.df = self.parse_df()
        # self.bcolz_path = os.path.join(self._downloader.path, 'assembly_summary_refseq.bcolz')
        # columns = list(self.df.columns)
        # columns[0] = 'assembly_instructions'
        # self.df.columns = columns
        # self.ct = bcolz.ctable.fromdataframe(df, rootdir=self.bcolz_path)
        # self.taxid2refseq_accession = defaultdict(set)
        self.taxid2refseq_accession = defaultdict(int)
        for ind, ser in self.df.iterrows():
            self.taxid2refseq_accession[ser['assembly_accession'][:ser['assembly_accession'].find('.')]] = ser['taxid']

    def parse_df(self):
        df = pd.read_csv(os.path.join(self._downloader.path, 'assembly_summary_refseq.txt'),
                         skiprows=[0], sep='\t')
        columns = list(df.columns)
        columns[0] = 'assembly_accession'
        df.columns = columns
        return df

    def __getstate__(self):
        d = dict(self.__dict__)
        del d['df']
        return d

    def __setstate__(self, d):
        # TODO add try/except
        self.__dict__.update(d)
        self.df = self.parse_df()

