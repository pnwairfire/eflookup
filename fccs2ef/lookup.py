"""lookup.py:
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

from io import Fccs2UrbanskiGroupMappingLoader, UrbanskiGroup2EfMappingLoader

__all__ = [
    'LookUp'
]

class LookUp(object):
    """Class for looking up emission factors for FCCS fuelbed types
    """

    def __init__(self, **options):
        """Constructor - reads FCCS-based emissions factors into dictionary
        for quick access.
        """
        self._fccs_2_urbanski_group = Fccs2UrbanskiGroupMappingLoader(file_name=options.get(
            'fccs_2_urbanski_map_file')).get()
        self._urbanski_group_2_efs = UrbanskiGroup2EfMappingLoader(file_name=options.get(
            'urbanski_group_2_efs')).get()

    def get(self):
        pass
    __getitem__ = get
