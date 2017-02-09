import unittest
from nose.tools import assert_equals

from dojo.taxonomy import NCBITree


class TestGGLineage(unittest.TestCase):
    def test(self):
        ncbi_tree = NCBITree()
        strain_name_1 = ncbi_tree.green_genes_lineage(391904, depth=5, depth_force=True)
        strain_name_2 = ncbi_tree.green_genes_lineage(391904, depth_force=True)

        strain_name_3 = ncbi_tree.green_genes_lineage(391904, depth=5, depth_force=False)
        strain_name_4 = ncbi_tree.green_genes_lineage(391904, depth_force=False)

        strain_name_5 = ncbi_tree.green_genes_lineage(391904, depth=8, depth_force=True)
        strain_name_6 = ncbi_tree.green_genes_lineage(391904, depth=8, depth_force=False)

        # Test the null pointer
        strain_name_7 = ncbi_tree.green_genes_lineage(-10, depth=8)


        print(strain_name_6)


class TestLCA(unittest.TestCase):
    def test(self):
        ncbi_tree = NCBITree()
        # Try LCA with a null-pointer
        lca = ncbi_tree.lowest_common_ancestor(391904, -10)
        print(lca)
