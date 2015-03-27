"""eflookup.fccs2ef.lookup:

@todo:
 - Update LookUp.get to support specifying 'fuel_category' without specifying
   'phase', and to suport specifying 'species' without specifying either
   'phase' or 'fuel_category' (ex. to get all CO2 EFs associated with a
    specific FCCS fuelbed) (?)
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

from ..constants import Phase, FuelCategory
from .load import (
    EFSetTypes, Fccs2CoverTypeLoader, CoverType2EfGroupLoader, EfGroup2EfLoader
)

__all__ = [
    'LookUp',
    'Fccs2Ef',
    'CoverType2Ef'
]

class LookUp(object):
    """Class for looking up emission factors for FCCS fuelbed types
    """

    RSC_KEYS = {
        # Accept 'woody' and 'duff' to be explicitly selected
        "woody": FuelCategory.WOODY,
        "duff": FuelCategory.DUFF,
        # Consume fuel categories with residual emissions
        # TODO: check these!!!
        # TODO: expect different keys???
        "100-hr fuels": FuelCategory.WOODY,
        "1000-hr fuels sound": FuelCategory.WOODY,
        "1000-hr fuels rotten": FuelCategory.WOODY,
        "10k+-hr fuels rotten": FuelCategory.WOODY,
        "10k+-hr fuels sound": FuelCategory.WOODY,
        "10000-hr fuels rotten": FuelCategory.WOODY,
        "-hr fuels sound": FuelCategory.WOODY,
        "stumps rotten": FuelCategory.WOODY,
        "stumps lightered": FuelCategory.WOODY,
        "duff lower": FuelCategory.DUFF,
        "duff upper": FuelCategory.DUFF,
        "basal accumulations": FuelCategory.DUFF,
        "squirrel middens": FuelCategory.DUFF
    }

    def __init__(self, is_rx, **options):
        """Constructor - reads FCCS-based emissions factors into dictionary
        for quick access.

        Args:
         - is_rx - set to True if a prescribed burn

        Options:
         - fccs_2_cover_type_file --
         - cover_type_2_ef_group_file --
         - ef_group_2_ef_file --
        """
        self.is_rx = is_rx
        self._fccs_2_cover_type = Fccs2CoverTypeLoader(file_name=options.get(
            'fccs_2_cover_type_file')).get()
        self._cover_type_2_ef_group = CoverType2EfGroupLoader(file_name=options.get(
            'cover_type_2_ef_group_file')).get()
        self._ef_group_2_ef_loader = EfGroup2EfLoader(file_name=options.get(
            'ef_group_2_ef_file'))
        self._ef_group_2_ef = self._ef_group_2_ef_loader.get()

    def get(self, **keys):
        """Looks up and returns emissions factor info for the fccs fuelbed type
        or cover type

        Lookup Keys:
         - fccs_fuelbed_id -- FCCS fuelbed id
         - cover_type_id -- FCCS fuelbed id
         - phase -- emissions factor set identifier ('flaming', 'smoldering',
            'residual')
         - fuel_category -- fuel category (ex. '100-hr fuels',
            'stumps rotten', etc.); only relevant if phase is 'residual';
            phase must also be defined
         - species -- chemical species; phase (and fuel_category if phase is
            'residual') must also be defined

        Notes:
         - Either 'fccs_fuelbed_id' or 'cover_type_id' must be specified, but
            not both
         - fuel_category is effectively ignored for 'flaming' and 'smoldering'
            (since the same EFs are used accross all fuel categories)

        Examples:
        >>> lu = LookUp
        >>> lu.get(fccs_fuelbed_id=4)
        >>> lu.get(fccs_fuelbed_id=4, phase='flaming')
        >>> lu.get(fccs_fuelbed_id=4, phase='flaming', species='CO2')
        >>> lu.get(cover_type_id=118)
        >>> lu.get(cover_type_id=118, phase='flaming')
        >>> lu.get(cover_type_id=118, phase='flaming', species='CO2')

        Note: returns None if any of the arguments are invalid.
        """
        fccs_fuelbed_id = keys.get('fccs_fuelbed_id')
        cover_type_id = keys.get('cover_type_id')
        phase = keys.get('phase')
        fuel_category = keys.get('fuel_category')
        species = keys.get('species')

        if fccs_fuelbed_id is None and cover_type_id is None:
            raise LookupError("Specify either fccs_fuelbed_id or cover_type_id")
        elif fccs_fuelbed_id is not None and cover_type_id is not None:
            raise LookupError("Specify either fccs_fuelbed_id or cover_type_id, not both")

        if not phase and (fuel_category or species):
            raise LookupError("Specify phase when also specifying fuel_category or species")
        if not fuel_category and species and Phase.RESIDUAL == phase:
            raise LookupError("Specify fuel_category when also specifying species if phase is 'residual'")

        try:
            if not cover_type_id:
                # fccs_fuelbed_id should be a string, since it's not necessary
                # numeric but cast to string in case user specified it as an integer
                cover_type_id = self._fccs_2_cover_type[str(fccs_fuelbed_id)]

            ef_groups = self._cover_type_2_ef_group[str(cover_type_id)]

            ef_sets = {
                Phase.RESIDUAL: {
                    FuelCategory.WOODY: self._ef_group_2_ef_loader.get_woody_rsc(),
                    FuelCategory.DUFF: self._ef_group_2_ef_loader.get_duff_rsc()
                }
            }
            ef_set_type = EFSetTypes.FLAME_SMOLD_RX if self.is_rx else EFSetTypes.FLAME_SMOLD_WF
            if self._ef_group_2_ef.has_key(ef_groups[ef_set_type]):
                # flaming and smoldering have the same EFs
                ef_sets.update({
                    Phase.FLAMING: self._ef_group_2_ef[ef_groups[ef_set_type]],
                    Phase.SMOLDERING: self._ef_group_2_ef[ef_groups[ef_set_type]]
                })

            if phase:
                if Phase.RESIDUAL == phase and fuel_category:
                    rsc_k = self.RSC_KEYS[fuel_category]
                    if species:
                        return ef_sets[phase][rsc_k][species]
                    else:
                        return ef_sets[phase][rsc_k]
                else:
                    if species:
                        return ef_sets[phase][species]
                    else:
                        return ef_sets[phase]
            else:
                return ef_sets
        except KeyError:
            return None

    def species(self, phase):
        # TODO: implement
        return []

class Fccs2Ef(LookUp):
    def get(self, fccs_fuelbed_id, phase=None, fuel_category=None, species=None):
        """Looks up and returns emissions factor info for the fccs fuelbed type

        Args:
         - fccs_fuelbed_id -- FCCS fuelbed id
        Optional Args
         - phase -- emissions factor set identifier ('flaming', 'smoldering',
            'residual')
         - fuel_category -- fuel category (ex. '100-hr fuels',
            'stumps rotten', etc.); only relevant if phase is 'residual';
            phase must also be defined
         - species -- chemical species; phase (and fuel_category if phase is
            'residual') must also be defined

        Examples:
        >>> LookUp().get(fccs_fuelbed_id=4)
        >>> LookUp().get(fccs_fuelbed_id=4, 'flaming')
        >>> LookUp().get(fccs_fuelbed_id=4, 'flaming', 'duff upper')
        >>> LookUp().get(fccs_fuelbed_id=4, 'flaming', species='CO2')
        >>> LookUp().get(fccs_fuelbed_id=4, 'flaming', 'duff upper', 'CO2')
        >>> LookUp().get(fccs_fuelbed_id=4, 'flaming', 'CO2')

        Note: returns None if any of the arguments are invalid.
        """
        return super(Fccs2Ef, self).get(fccs_fuelbed_id=fccs_fuelbed_id,
            phase=phase, fuel_category=fuel_category, species=species)

    def __getitem__(self, fccs_fuelbed_id):
        """Enables bracket access, returning a dict containing emissions
        factors information for the specified fccs_fuelbed_id. The
        returned dict is of the form:

        {
            'flaming': { 'CH3CH2OH': 123.23, ... },
            'smoldering': {...},
            'residual': {
                'woody': {...},
                'duff': {...}
            }
        }

        Args:
         - fccs_fuelbed_id -- FCCS fuelbed id

        Example:
        >>> LookUp()[4]
        >>> LookUp()[4]['flaming']
        >>> LookUp()[4]['flaming']['CO2']
        >>> LookUp()[118]['residual']
        >>> LookUp()[118]['residual']['woody']
        >>> LookUp()[118]['residual']['woody']['CO2']

        Note: raises KeyError if fccs_fuelbed_id is invalid.
        """
        key = str(fccs_fuelbed_id)
        if not self._fccs_2_cover_type.has_key(key):
            raise KeyError(key)
        return self.get(key)


class CoverType2Ef(LookUp):
    def get(self, cover_type_id, phase=None, fuel_category=None, species=None):
        """Looks up and returns emissions factor info for the cover type

        Args:
         - cover_type_id -- cover type id
        Optional Args
         - phase -- emissions factor set identifier ('flaming', 'smoldering',
            'residual')
         - fuel_category -- fuel category (ex. '100-hr fuels',
            'stumps rotten', etc.); only relevant if phase is 'residual';
            phase must also be defined
         - species -- chemical species; phase (and fuel_category if phase is
            'residual') must also be defined

        Examples:
        >>> LookUp().get(cover_type_id=118)
        >>> LookUp().get(cover_type_id=118, 'flaming')
        >>> LookUp().get(cover_type_id=118, 'flaming', 'duff upper')
        >>> LookUp().get(cover_type_id=118, 'flaming', species='CO2')
        >>> LookUp().get(cover_type_id=118, 'flaming', 'duff upper', 'CO2')

        Note: returns None if any of the arguments are invalid.
        """
        return super(CoverType2Ef, self).get(cover_type_id=cover_type_id,
            phase=phase, fuel_category=fuel_category, species=species)

    def __getitem__(self, cover_type_id):
        """Enables bracket access, returning a dict containing emissions
        factors information for the specified covert_type_id. The
        returned dict is of the form:

        {
            'flaming': { 'CH3CH2OH': 123.23, ... },
            'smoldering': {...},
            'residual': {
                'woody': {...},
                'duff': {...}
            }
        }

        Args:
         - cover_type_id -- FCCS fuelbed id

        Example:
        >>> LookUp()[118]
        >>> LookUp()[118]['flaming']
        >>> LookUp()[118]['flaming']['CO2']
        >>> LookUp()[118]['residual']
        >>> LookUp()[118]['residual']['woody']
        >>> LookUp()[118]['residual']['woody']['CO2']

        Note: raises KeyError if cover_type_id is invalid.
        """
        key = str(cover_type_id)
        if not self._cover_type_2_ef_group.has_key(key):
            raise KeyError(key)
        return self.get(key)
