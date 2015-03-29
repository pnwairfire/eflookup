"""eflookup.constants: defines constants used throughout eflookup package

TODO: Make these immutable
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2015, AirFire, PNW, USFS"

class Phase:
    FLAMING = 'flaming'
    SMOLDERING = 'smoldering'
    RESIDUAL = 'residual'

class FuelCategory:
    WOODY = 'woody'
    DUFF = 'duff'

class BasicEFLookup(dict):
    """Look-up object containing FEPS EFs
    """

    def get(self, **keys):
        """Looks up and returns emission factors

        Lookup Keys:
         - phase -- emissions factor set identifier ('flaming', 'smoldering',
            'residual')
         - species -- chemical species; phase (and fuel_category if phase is
            'residual') must also be defined

        Notes:
         - ignores any other keys
         - returns None if any of the arguments are invalid.

        Examples:
        >>> lu = LookUp
        >>> lu.get(fccs_fuelbed_id=4)
        >>> lu.get(fccs_fuelbed_id=4, phase='flaming')
        >>> lu.get(fccs_fuelbed_id=4, phase='flaming', species='CO2')
        >>> lu.get(cover_type_id=118)
        >>> lu.get(cover_type_id=118, phase='flaming')
        >>> lu.get(cover_type_id=118, phase='flaming', species='CO2')
        """
        phase = keys.get('phase')
        species = keys.get('species')

        if not phase and species:
            raise LookupError("Specify phase when also specifying species")

        try:
            if phase:
                if species:
                    return self[phase][species]
                return self[phase]
            return self

        except KeyError:
            return None

    def species(self, phase):
        return set(self[phase].keys())
