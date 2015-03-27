"""test_lookup.py:  tests for looking up EFs by FCCS id or cover type.
"""

#from py.test import raises

from eflookup.fepsef.lookup import FepsEFLookup

class TestLookup:
    def test_without_haps(self):
        expected = {
            # TODO: set correctly
        }
        assert expected == FepsEFLookup()

    def test_with_haps(self):
        expected = {
            # TODO: set correctly
        }
        assert expected == FepsEFLookup(include_haps=True)
