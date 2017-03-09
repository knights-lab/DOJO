import unittest
from nose.tools import assert_equals

from dojo.taxonomy import NCBITree


class TestGGLineage(unittest.TestCase):
    ncbi_tree = NCBITree()

    def test(self):
        # 11788
        self.test_strains(11788)
        self.test_strains(391904)
        self.test_strains(-10)

    def test_strains(self, taxid):
        strain_name_1 = self.ncbi_tree.green_genes_lineage(taxid, depth=5, depth_force=True)
        strain_name_2 = self.ncbi_tree.green_genes_lineage(taxid, depth_force=True)

        strain_name_3 = self.ncbi_tree.green_genes_lineage(taxid, depth=5, depth_force=False)
        strain_name_4 = self.ncbi_tree.green_genes_lineage(taxid, depth_force=False)

        strain_name_5 = self.ncbi_tree.green_genes_lineage(taxid, depth=8, depth_force=True)
        strain_name_6 = self.ncbi_tree.green_genes_lineage(taxid, depth=8, depth_force=False)

        # Test the null pointer
        strain_name_7 = self.ncbi_tree.green_genes_lineage(taxid, depth=8)



class TestLCA(unittest.TestCase):
    def test(self):
        ncbi_tree = NCBITree()
        # Try LCA with a null-pointer
        lca = ncbi_tree.lowest_common_ancestor(391904, -10)
        print(lca)
