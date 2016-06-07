from nose.tools import assert_equals

from ninja_dojo.downloaders import RefseqSummary


def test_refseq_download():
    downloader = RefseqSummary()
    downloader.run()
    assert_equals(None, None)
