import unittest
from nose.tools import assert_equals

from ninja_dojo.taxonomy.maps import RefseqAssemblyMap


class RefseqMapTest(unittest.TestCase):
    def test(self):
        refseq_map = RefseqAssemblyMap()
        assert_equals(None, None)
