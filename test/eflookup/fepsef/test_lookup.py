"""test_lookup.py:  tests for looking up EFs by FCCS id or cover type.
"""

#from py.test import raises

from eflookup.fepsef.lookup import FepsEF

class TestLookup:
    def test_without_haps(self):
        expected = {
            # TODO: set correctly
        }
        assert expected == FepsEF()

    def test_with_haps(self):
        expected = {
            # TODO: set correctly
        }
        assert expected == FepsEF(include_haps=True)
