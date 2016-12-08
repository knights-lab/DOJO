from nose.tools import assert_equals
import unittest

from dojo.downloaders import NucleotideCatalog


class NucleotideCatalogDownloadTest(unittest.TestCase):
    def test(self):
        downloader = NucleotideCatalog()
        downloader.run()
        assert_equals(None, None)
