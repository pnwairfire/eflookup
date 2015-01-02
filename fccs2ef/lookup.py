"""lookup.py:

@todo:
 - Use something other than 'flame_smold_wf', 'residual', 'duff',
   'flame_smold_rx' for keys
 - Update LookUp.get to support specying 'species' without specying 'ef_set_type'
   (ex. to get all CO2 EFs associated with a specific FCCS fuelbed)
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

from .load import Fccs2UrbanskiLoader, EFMappingLoader, EFSetTypes

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
            'fccs_2_urbanski_file')).get()
        self._urbanski_efs = EFMappingLoader(file_name=options.get(
            'urbanski_efs_file')).get()

    def get(self, fccs_fuel_bed_id, ef_set_type=None, species=None):
        """Looks up and returns emissions factor info for the fccs fuelbed type

        Args:
         - fccs_fuel_bed_id -- FCCS fuelbed id
        Optional Args
         - ef_set_type -- emissions factor set identifier ('flame_smold_wf',
            'residual', 'duff', or flame_smold_rx)
         - specicies -- chemical species; is ignored if ef_set_type isn't also
            defined

        Examples:
        >>> LookUp().get(4)
        >>> LookUp().get(4, 'flame_smold_rx')
        >>> LookUp().get(4, 'flame_smold_rx', 'CO2')

        Note: returns None if any of the arguments are invalid.
        """
        try:
            gs = self._fccs_2_urbanski_groups[str(fccs_fuel_bed_id)]
            ef_sets = {
                'flame_smold_wf': self._urbanski_efs.get(gs[EFSetTypes.FLAME_SMOLD_WF], {}),
                'residual': self._urbanski_efs.get(gs[EFSetTypes.RESIDUAL], {}),
                'duff': self._urbanski_efs.get(gs[EFSetTypes.DUFF], {}),
                'flame_smold_rx': self._urbanski_efs.get(gs[EFSetTypes.FLAME_SMOLD_RX], {})
            }
            if ef_set_type:
                if species:
                    return ef_sets[ef_set_type][species]
                else:
                    return ef_sets[ef_set_type]
            else:
                return ef_sets
        except KeyError:
            return None

    def __getitem__(self, fccs_fuel_bed_id):
        """Enables bracket access, returning a dict containing emissions
        factors information for the specified fccs_fuel_bed_id. The
        returned dict is of the form:

        {
            'flame_smold_wf': { 'CH3CH2OH': 123.23, ... },
            'residual': {...},
            'duff': {...},
            'flame_smold_rx': {...}
        }

        Args:
         - fccs_fuel_bed_id -- FCCS fuelbed id

        Example:
        >>> LookUp()[4]
        >>> LookUp()[4]['flame_smold_rx']
        >>> LookUp()[4]['flame_smold_rx']['CO2']

        Note: raises KeyError if fccs_fuel_bed_id is invalid.
        """
        if not self._fccs_2_urbanski_groups.has_key(str(fccs_fuel_bed_id)):
            raise KeyError(str(fccs_fuel_bed_id))
        return self.get(fccs_fuel_bed_id)
