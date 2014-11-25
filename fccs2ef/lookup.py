"""lookup.py:
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

from io import Fccs2SafSrmParser, UrbanskiEfParser

__all__ = [
    'LookUp'
]

class LookUp(object):
    """Class for looking up emission factors for FCCS fuelbed types
    """

    def __init__(self):
        """Constructor - reads FCCS-based emissions factors into dictionary
        for quick access.
        """
        self._fccs_2_saf_srms = Fccs2SafSrmParser().get()
        self._urbanskpo_efs = UrbanskiEfParser().get()

    def get(self):
        pass
    __getitem__ = get
