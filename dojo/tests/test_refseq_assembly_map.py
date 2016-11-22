import unittest
from nose.tools import assert_equals

from dojo.taxonomy.maps import RefseqAssemblyMap


class RefseqAssemblyMapTest(unittest.TestCase):
    def test(self):
        refseq_map = RefseqAssemblyMap()
        assert_equals(None, None)
