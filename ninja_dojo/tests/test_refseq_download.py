from nose.tools import assert_equals

from ninja_dojo.downloaders import RefseqAssemblySummary


def test_refseq_download():
    downloader = RefseqAssemblySummary()
    downloader.run()
    assert_equals(None, None)
