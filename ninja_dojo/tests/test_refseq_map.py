import unittest
from nose.tools import assert_equals

from ninja_dojo.taxonomy.maps import RefseqMap


class RefseqMapTest(unittest.TestCase):
    def test(self):
        refseq_map = RefseqMap()
        assert_equals(None, None)
