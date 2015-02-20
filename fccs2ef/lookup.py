"""lookup.py:

@todo:
 - Use something other than 'flame_smold_wf', 'woody_rsc', 'duff_rsc',
   'flame_smold_rx' for keys
 - Update LookUp.get to support specying 'species' without specying 'ef_set_type'
   (ex. to get all CO2 EFs associated with a specific FCCS fuelbed)
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

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

    def __init__(self, **options):
        """Constructor - reads FCCS-based emissions factors into dictionary
        for quick access.

        Options:
         - fccs_2_cover_type_file --
         - covertype_2_ef_group_file --
         - ef_group_2_ef_file --
        """
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
         - ef_set_type (optional) -- emissions factor set identifier
            ('flame_smold_wf', 'flame_smold_rx', 'woody_rsc', or 'duff_rsc')
         - specicies (optional) -- chemical species; is ignored if ef_set_type
            isn't also defined

        Notes:
         - Either 'fccs_fuelbed_id' or 'cover_type_id' must be specified, but
            not both
         - 'species' is ignored if 'ef_set_type' isn't specified

        Examples:
        >>> lu = LookUp
        >>> lu.get(fccs_fuelbed_id=4)
        >>> lu.get(fccs_fuelbed_id=4, ef_set_type='flame_smold_rx')
        >>> lu.get(fccs_fuelbed_id=4, ef_set_type='flame_smold_rx', species='CO2')
        >>> lu.get(cover_type_id=118)
        >>> lu.get(cover_type_id=118, ef_set_type='flame_smold_rx')
        >>> lu.get(cover_type_id=118, ef_set_type='flame_smold_rx', species='CO2')

        Note: returns None if any of the arguments are invalid.
        """
        fccs_fuelbed_id = keys.get('fccs_fuelbed_id')
        cover_type_id = keys.get('cover_type_id')
        ef_set_type = keys.get('ef_set_type')
        species = keys.get('species')

        if fccs_fuelbed_id is None and cover_type_id is None:
            raise LookupError("Specify either fccs_fuelbed_id or cover_type_id")
        elif fccs_fuelbed_id is not None and cover_type_id is not None:
            raise LookupError("Specify either fccs_fuelbed_id or cover_type_id, not both")

        try:
            if not cover_type_id:
                # fccs_fuelbed_id should be a string, since it's not necessary
                # numeric but cast to string in case user specified it as an integer
                cover_type_id = self._fccs_2_cover_type[str(fccs_fuelbed_id)]

            ef_groups = self._cover_type_2_ef_group[str(cover_type_id)]

            ef_sets = {
                'woody_rsc': self._ef_group_2_ef_loader.get_woody_rsc(),
                'duff_rsc': self._ef_group_2_ef_loader.get_duff_rsc()
            }
            fswf_key = ef_groups[EFSetTypes.FLAME_SMOLD_WF]
            if self._ef_group_2_ef.has_key(fswf_key):
                ef_sets.update(flame_smold_wf=self._ef_group_2_ef[fswf_key])
            fsrx_key = ef_groups[EFSetTypes.FLAME_SMOLD_RX]
            if self._ef_group_2_ef.has_key(fsrx_key):
                ef_sets.update(flame_smold_rx=self._ef_group_2_ef[fsrx_key])

            if ef_set_type:
                if species:
                    return ef_sets[ef_set_type][species]
                else:
                    return ef_sets[ef_set_type]
            else:
                return ef_sets
        except KeyError:
            return None

class Fccs2Ef(LookUp):
    def get(self, fccs_fuelbed_id, ef_set_type=None, species=None):
        """Looks up and returns emissions factor info for the fccs fuelbed type

        Args:
         - fccs_fuelbed_id -- FCCS fuelbed id
        Optional Args
         - ef_set_type -- emissions factor set identifier ('flame_smold_wf',
            'flame_smold_rx', 'woody_rsc', or 'duff_rsc')
         - specicies -- chemical species; is ignored if ef_set_type isn't also
            defined

        Examples:
        >>> LookUp().get(fccs_fuelbed_id=4)
        >>> LookUp().get(fccs_fuelbed_id=4, 'flame_smold_rx')
        >>> LookUp().get(fccs_fuelbed_id=4, 'flame_smold_rx', 'CO2')

        Note: returns None if any of the arguments are invalid.
        """
        return super(Fccs2Ef, self).get(fccs_fuelbed_id=fccs_fuelbed_id,
            ef_set_type=ef_set_type, species=species)

    def __getitem__(self, fccs_fuelbed_id):
        """Enables bracket access, returning a dict containing emissions
        factors information for the specified fccs_fuelbed_id. The
        returned dict is of the form:

        {
            'flame_smold_wf': { 'CH3CH2OH': 123.23, ... },
            'flame_smold_rx': {...},
            'woody_rsc': {...},
            'duff_rsc': {...}
        }

        Args:
         - fccs_fuelbed_id -- FCCS fuelbed id

        Example:
        >>> LookUp()[4]
        >>> LookUp()[4]['flame_smold_rx']
        >>> LookUp()[4]['flame_smold_rx']['CO2']

        Note: raises KeyError if fccs_fuelbed_id is invalid.
        """
        key = str(fccs_fuelbed_id)
        if not self._fccs_2_cover_type.has_key(key):
            raise KeyError(key)
        return self.get(key)


class CoverType2Ef(LookUp):
    def get(self, cover_type_id, ef_set_type=None, species=None):
        """Looks up and returns emissions factor info for the cover type

        Args:
         - cover_type_id -- cover type id
        Optional Args
         - ef_set_type -- emissions factor set identifier ('flame_smold_wf',
            'flame_smold_rx', 'woody_rsc', or 'duff_rsc')
         - specicies -- chemical species; is ignored if ef_set_type isn't also
            defined

        Examples:
        >>> LookUp().get(cover_type_id=118)
        >>> LookUp().get(cover_type_id=118, 'flame_smold_rx')
        >>> LookUp().get(cover_type_id=118, 'flame_smold_rx', 'CO2')

        Note: returns None if any of the arguments are invalid.
        """
        return super(CoverType2Ef, self).get(cover_type_id=cover_type_id,
            ef_set_type=ef_set_type, species=species)

    def __getitem__(self, cover_type_id):
        """Enables bracket access, returning a dict containing emissions
        factors information for the specified covert_type_id. The
        returned dict is of the form:

        {
            'flame_smold_wf': { 'CH3CH2OH': 123.23, ... },
            'flame_smold_rx': {...},
            'woody_rsc': {...},
            'duff_rsc': {...}
        }

        Args:
         - cover_type_id -- FCCS fuelbed id

        Example:
        >>> LookUp()[118]
        >>> LookUp()[118]['flame_smold_rx']
        >>> LookUp()[118]['flame_smold_rx']['CO2']

        Note: raises KeyError if cover_type_id is invalid.
        """
        key = str(cover_type_id)
        if not self._cover_type_2_ef_group.has_key(key):
            raise KeyError(key)
        return self.get(key)
