import unittest
from nose.tools import assert_equals

from ninja_dojo.downloaders import RefseqCatalog


class RefseqMapTest(unittest.TestCase):
    def test(self):
        refseq_catalog = RefseqCatalog().download()
        assert_equals(None, None)
