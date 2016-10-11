import unittest
from nose.tools import assert_equals

from ninja_dojo.taxonomy import NCBITree


class TestGGLineage(unittest.TestCase):
    def test(self):
        ncbi_tree = NCBITree()
        strain_name = ncbi_tree.green_genes_lineage(391904, depth=8)
        print(strain_name)
