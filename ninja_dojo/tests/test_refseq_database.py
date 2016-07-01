import unittest
from nose.tools import assert_equals

from ninja_dojo.database import RefSeqDatabase


class RefseqSQLITEDatabaseTest(unittest.TestCase):
    def test(self):
        rfd = RefSeqDatabase()
        rfd._create()
        assert_equals(None, None)
