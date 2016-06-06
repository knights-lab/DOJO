from nose.tools import assert_equals

from ninja_dojo.downloaders import RefseqSummary


def test_homo_sapiens_gg_lineage_ncbi_tree():
    downloader = RefseqSummary()
    downloader.run()
    assert_equals(None, None)
