from nose.tools import assert_equals

from ninja_dojo.taxonomy.maps import RefseqMap


def test_refseq_map():
    refseq_map = RefseqMap()
    assert_equals(None, None)
