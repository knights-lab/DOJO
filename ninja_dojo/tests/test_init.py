# First unittest to test functioning of import
from nose.tools import assert_equal

_module_import_error = None

try:
    from ninja_dojo import *
except Exception as e:
    _module_import_error = e


def test_module_import():
    assert_equal(_module_import_error, None)
