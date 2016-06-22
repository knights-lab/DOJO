import unittest
from nose.tools import assert_equals

from ninja_dojo.database import RefSeqDatabase


class RefseqCatalogDatabaseTest(unittest.TestCase):
    def test(self):
        rfd = RefSeqDatabase()
        rfd._parse()
        assert_equals(None, None)
