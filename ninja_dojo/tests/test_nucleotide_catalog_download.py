from nose.tools import assert_equals
import unittest

from ninja_dojo.downloaders import NucleotideCatalog


class NucleotideCatalogDownloadTest(unittest.TestCase):
    def test(self):
        downloader = NucleotideCatalog()
        downloader.run()
        assert_equals(None, None)
