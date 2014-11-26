"""lookup.py:
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

from .load import Fccs2UrbanskiLoader, EFMappingLoader

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
        self._fccs_2_urbanski_groups = Fccs2UrbanskiLoader(file_name=options.get(
            'fccs_2_safsrm_file')).get()
        self._urbanski_efs = EFMappingLoader(file_name=options.get(
            'urbanski_efs_file')).get()

    def get(self, fccs_fuel_bed_id):
        gs = self._fccs_2_urbanski_groups[fccs_fuel_bed_id]
        return {
            'flame_smold_wf': self._urbanski_efs[gs['urbanski_flame_smold_wf']],
            'residual': self._urbanski_efs[gs['urbanski_residual']],
            'duff': self._urbanski_efs[gs['urbanski_duff']],
            'flame_smold_rx': self._urbanski_efs[gs['urbanski_flame_smold_rx']]
        }
    __getitem__ = get
