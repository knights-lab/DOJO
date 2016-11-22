import unittest
from nose.tools import assert_equals

from ninja_dojo.taxonomy import NCBITree


class TestGGLineage(unittest.TestCase):
    def test(self):
        ncbi_tree = NCBITree()
        strain_name_1 = ncbi_tree.green_genes_lineage(391904, depth=5, depth_force=True)
        strain_name_2 = ncbi_tree.green_genes_lineage(391904, depth_force=True)

        strain_name_3 = ncbi_tree.green_genes_lineage(391904, depth=5, depth_force=False)
        strain_name_4 = ncbi_tree.green_genes_lineage(391904, depth_force=False)

        strain_name_5 = ncbi_tree.green_genes_lineage(391904, depth=8, depth_force=True)
        strain_name_6 = ncbi_tree.green_genes_lineage(391904, depth=8, depth_force=False)


        print(strain_name_6)
