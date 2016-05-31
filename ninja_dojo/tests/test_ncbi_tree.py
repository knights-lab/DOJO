from nose.tools import assert_equals

from ninja_dojo.taxonomy import NCBITree


def test_homo_sapiens_gg_lineage_ncbi_tree():
    ncbi_tree = NCBITree()
    assert_equals(ncbi_tree.mp_lineage(9606), 'k__Eukaryota;p__Chordata;c__Mammalia;o__Primates;f__Hominidae;g__Homo;s__Homo_sapiens')
