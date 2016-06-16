import unittest
from nose.tools import assert_equals

from ninja_dojo.taxonomy.maps import RefseqCatalogMap


class RefseqCatalogMapTest(unittest.TestCase):
    def test(self):
        refseq_catalog_map = RefseqCatalogMap()
        assert_equals(None, None)
