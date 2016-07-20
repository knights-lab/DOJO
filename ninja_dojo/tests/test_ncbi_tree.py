import unittest
from nose.tools import assert_equals

from ninja_dojo.taxonomy import NCBITree


class TestGGLineage(unittest.TestCase):
    def test(self):
        ncbi_tree = NCBITree()
        assert_equals(ncbi_tree.gg_lineage(9606),
                      'k__Eukaryota;p__Chordata;c__Mammalia;o__Primates;f__Hominidae;g__Homo;s__Homo_sapiens')
