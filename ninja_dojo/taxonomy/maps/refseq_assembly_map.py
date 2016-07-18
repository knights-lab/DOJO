import os
import pandas as pd
from collections import defaultdict

from ninja_utils.factory import Pickleable, download

from ... import SETTINGS, LOGGER
from ...downloaders import RefseqAssemblySummary


class RefseqAssemblyMap(Pickleable):
    def __init__(self, _downloaders=(RefseqAssemblySummary(),)):
        self._downloaders = _downloaders
        super().__init__(SETTINGS, LOGGER)

    @download
    def _parse(self):
        df = self.parse_df()
        self.refseq_assembly_accession2ncbi_tid = defaultdict(int)
        # self.ncbi_tid2ftp_path = defaultdict(str)
        for ind, ser in df.iterrows():
            self.refseq_assembly_accession2ncbi_tid[ser['assembly_accession'][:ser['assembly_accession'].find('.')]] = ser['taxid']
        #     self.ncbi_tid2ftp_path[ser['taxid']] = ser['ftp_path']
        # This is a one to many mapping
        # self.ncbi_tid2refseq_assembly_accession = defaultdict(str, reverse_dict(self.refseq_assembly_accession2ncbi_tid))

    def parse_df(self):
        df = pd.read_csv(os.path.join(self._downloaders[0].path, 'assembly_summary_refseq.txt'),
                         skiprows=[0], sep='\t')
        columns = list(df.columns)
        columns[0] = 'assembly_accession'
        df.columns = columns
        return df

    # There is no more need for this
    # def __getstate__(self):
    #     d = dict(self.__dict__)
    #     del d['df']
    #     return d
    #
    # def __setstate__(self, d):
    #     # TODO add try/except
    #     self.__dict__.update(d)
    #     self.df = self.parse_df()

