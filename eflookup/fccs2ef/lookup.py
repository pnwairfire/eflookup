"""eflookup.fccs2ef.lookup:

@todo:
 - Refactor/Reorganize all classes in this module.  They've become convoluted
   after various refactoring due to changing requirements.
 - Update SingleCoverTypeEfLookup.get to support specifying 'fuel_category' without specifying
   'phase', and to suport specifying 'species' without specifying either
   'phase' or 'fuel_category' (ex. to get all CO2 EFs associated with a
    specific FCCS fuelbed) (?)
"""

__author__      = "Joel Dubowy"

import abc

from ..constants import Phase, CONSUME_FUEL_CATEGORY_TRANSLATIONS
from .load import (
    EFSetTypes,
    Fccs2CoverTypeLoader,
    CoverType2EfGroupLoader,
    CatPhase2EFGroupLoader,
    EfGroup2EfLoader
)

__all__ = [
    'Fccs2Ef',
    'CoverType2Ef'
]

# RSC_KEYS = {
#     # Accept 'woody' and 'duff' to be explicitly selected
#     "woody": FuelCategory.WOODY,
#     "duff": FuelCategory.DUFF,
#     # Consume fuel categories with residual emissions
#     # TODO: check these!!!
#     # TODO: expect different keys???
#     "100-hr fuels": FuelCategory.WOODY,
#     "1000-hr fuels sound": FuelCategory.WOODY,
#     "1000-hr fuels rotten": FuelCategory.WOODY,
#     "10k+-hr fuels rotten": FuelCategory.WOODY,
#     "10k+-hr fuels sound": FuelCategory.WOODY,
#     "10000-hr fuels rotten": FuelCategory.WOODY,
#     "-hr fuels sound": FuelCategory.WOODY,
#     "stumps rotten": FuelCategory.WOODY,
#     "stumps lightered": FuelCategory.WOODY,
#     "duff lower": FuelCategory.DUFF,
#     "duff upper": FuelCategory.DUFF,
#     "basal accumulations": FuelCategory.DUFF,
#     "squirrel middens": FuelCategory.DUFF
# }

_categorie_tuples = [
    e.split(':') for e in CONSUME_FUEL_CATEGORY_TRANSLATIONS.values()
]
VALID_FUEL_CATEGORIES = [e[0] for e in _categorie_tuples]
VALID_FUEL_SUB_CATEGORIES = [e[1] for e in _categorie_tuples]

class SingleCoverTypeEfLookup(object):
    """Lookup class containing EFs for a single FCCS or cover type id

    Objects of this class are passed to emissions
    """

    def __init__(self, cover_type_id, is_rx, cover_type_2_ef_group,
            cat_phase_2_ef_group, ef_group_2_ef_loader, ef_group_2_ef):
        """Constructor

        Args
         - cover_type_id
         - is_rx -- wether or not it's a prescribed burn
         - cover_type_2_ef_group
         - cat_phase_2_ef_group
         - ef_group_2_ef_loader
         - ef_group_2_ef
        """

        self.ef_groups = cover_type_2_ef_group[str(cover_type_id)]
        self.ef_flame_smold_set_type = EFSetTypes.FLAME_SMOLD_RX if is_rx else EFSetTypes.FLAME_SMOLD_WF
        self.ef_group_2_ef_loader = ef_group_2_ef_loader
        self.ef_group_2_ef = ef_group_2_ef
        self.cat_phase_2_ef_group = cat_phase_2_ef_group
        self.region = self.ef_groups[EFSetTypes.REGIONAL_RX]

        # self.update({
        #     Phase.RESIDUAL: {
        #         FuelCategory.WOODY: ef_group_2_ef_loader.get_woody_rsc(),
        #         FuelCategory.DUFF: ef_group_2_ef_loader.get_duff_rsc()
        #     }
        # })
        # ef_set_type = EFSetTypes.FLAME_SMOLD_RX if is_rx else EFSetTypes.FLAME_SMOLD_WF
        # if ef_groups[ef_set_type] in ef_group_2_ef:
        #     # flaming and smoldering have the same EFs
        #     self.update({
        #         Phase.FLAMING: ef_group_2_ef[ef_groups[ef_set_type]],
        #         Phase.SMOLDERING: ef_group_2_ef[ef_groups[ef_set_type]]
        #     })



    def get(self, phase, fuel_category, fuel_sub_category, species):
        """Looks up and returns cover type specific emission factors

        Lookup Keys:
         - phase -- emissions factor set identifier ('flaming', 'smoldering',
            'residual')
         - fuel_category -- fuel category (ex. 'woody fuels', 'canopy', etc.)
            phase must also be defined
         - fuel_sub_category -- fuel sub-category (ex. '100-hr fuels',
            'stumps rotten', etc.); phase and fuel_category must also be
            defined
         - species -- chemical species; phase, fuel_category, and
            if fuel_sub_category must also be defined

        Notes:
         - fuel_category is effectively ignored for 'flaming' and 'smoldering'
            (since the same EFs are used accross all fuel categories)
         - returns None if any of the arguments are invalid.

        Examples:
        >>> lu = LookUp()
        >>> lu.get(phase='residual', fuel_category='canopy',
                fuel_sub_category='overstory', species='CO2')
        """
        if any([not e for e in (phase, fuel_category, fuel_sub_category, species)]):
            raise LookupError("Specify phase, fuel_category, "
                "fuel_sub_category, and species")

        ef_group = self.cat_phase_2_ef_group.get(phase, fuel_category,
            fuel_sub_category, species, default=-1)
        if ef_group = None:
            # that indicates that there should be no emissions;
            # so, return 0
            return 0
        elif ef == -1:
            # Use non overrides
            try:
                if phase == Phase.RESIDUAL:
                    # TODO: return 0 unle it's woody or duff (based
                    #   on fuel catevory or sub category?) ???
                    pass
                else:
                    pass
            except KeyError:
                 return None
        else:
            try:
                # return override value
                return self.ef_group_2_ef[ef_group][species]
            except KeyError:
                 return None


    def species(self, phase):
        # if phase not in self:
        #     return set()

        if phase == Phase.RESIDUAL:
            woody_keys = self.ef_group_2_ef_loader.get_woody_rsc().keys()
            duff_keys = self.ef_group_2_ef_loader.get_duff_rsc().keys()
            return set(woody_keys).union(duff_keys)
        else:
            return set(self.ef_group_2_ef[ef_groups[ef_set_type]].keys())


class BaseLookUp(object):
    """Class for looking up emission factors for FCCS fuelbed types
    """

    def __init__(self, is_rx, **options):
        """Constructor - reads FCCS-based emissions factors into dictionary
        for quick access.

        Args:
         - is_rx - set to True if a prescribed burn

        Options:
         - fccs_2_cover_type_file --
         - cover_type_2_ef_group_file --
         - cat_phase_2_ef_group_file --
         - ef_group_2_ef_file --
        """
        self.is_rx = is_rx
        self._fccs_2_cover_type = Fccs2CoverTypeLoader(
            file_name=options.get('fccs_2_cover_type_file')).get()
        self._cover_type_2_ef_group = CoverType2EfGroupLoader(
            file_name=options.get('cover_type_2_ef_group_file')).get()
        self._cat_phase_2_ef_group = CatPhase2EFGroupLoader(
            file_name=options.get('cat_phase_2_ef_group_file')).get()
        self._ef_group_2_ef_loader = EfGroup2EfLoader(
            file_name=options.get('ef_group_2_ef_file'))
        self._ef_group_2_ef = self._ef_group_2_ef_loader.get()
        self.cover_type_look_ups = {}

    def _get(self, **keys):
        """Looks up and returns emissions factor info for the fccs fuelbed type
        or cover type.

        Delegates to SingleCoverTypeEfLookup, instantiated and memoized per
        distinct cover type, to do most of the work.

        Lookup Keys:
         - fccs_fuelbed_id -- FCCS fuelbed id
         - cover_type_id -- Cover Type id
         (see SingleCoverTypeEfLookup.get helpstring for other lookup keys)

        Notes:
         - Either 'fccs_fuelbed_id' or 'cover_type_id' must be specified, but
            not both
         - returns None if any of the arguments are invalid.

        Examples:
        >>> lu = LookUp
        >>> lu.get(fccs_fuelbed_id=4)
        >>> lu.get(cover_type_id=118, phase='residual', fuel_category='woody', species='CO2')
        """
        fccs_fuelbed_id = keys.get('fccs_fuelbed_id')
        cover_type_id = keys.get('cover_type_id')

        if fccs_fuelbed_id is None and cover_type_id is None:
            raise LookupError("Specify either fccs_fuelbed_id or cover_type_id")
        elif fccs_fuelbed_id is not None and cover_type_id is not None:
            raise LookupError("Specify either fccs_fuelbed_id or cover_type_id, not both")

        try:
            if not cover_type_id:
                # fccs_fuelbed_id should be a string, since it's not necessary
                # numeric but cast to string in case user specified it as an integer
                cover_type_id = self._fccs_2_cover_type[str(fccs_fuelbed_id)]

            if cover_type_id not in self.cover_type_look_ups:
                self.cover_type_look_ups[cover_type_id] = SingleCoverTypeEfLookup(
                    cover_type_id,
                    self.is_rx,
                    self._cover_type_2_ef_group,
                    self._cat_phase_2_ef_group,
                    self._ef_group_2_ef_loader,
                    self._ef_group_2_ef)

        except KeyError:
            return None

        return self.cover_type_look_ups[cover_type_id].get(**keys)

    @abc.abstractmethod
    def get(self, identifier, phase=None, fuel_category=None,
            fuel_sub_category=None, species=None):
        pass

    # TODO: can we make this an abstract @property?
    @abc.abstractmethod
    def _top_level_mapping(self):
        pass

    def __getitem__(self, identifier):
        """Enables bracket access, returning a dict containing emissions
        factors information for the specified id (fccs_fuelbed_id
        or cover_type_id, depending on the subclass).

        The returned dict is of the form:

            {
                'flaming': {
                    'shrub': {
                        'secondary dead': {
                            'CH3CH2OH': 123.23,
                            ...
                        },
                        ...
                    },
                    ...
                },
                ...
            }

        Args:
         - identifier -- FCCS fuelbed id or CoverType id

        Example:
        >>> LookUp()[118]
        >>> LookUp()[121]['residual']['shrub']['secondary dead']['CO2']

        Note: raises KeyError if cover_type_id is invalid.
        """
        key = str(identifier)
        if key not in self._top_level_mapping():
            raise KeyError(key)
        return self.get(key)


class Fccs2Ef(BaseLookUp):

    def _top_level_mapping(self):
        return self._fccs_2_cover_type

    def get(self, fccs_fuelbed_id, phase, fuel_category,
            fuel_sub_category, species):
        """Looks up and returns emissions factor info for the fccs fuelbed type

        Args:
         - fccs_fuelbed_id -- FCCS fuelbed id
        Optional Args
         (See LookUp.get helpstring, above.)

        Examples:
        >>> Fccs2Ef().get(4, 'flaming', 'shrub', 'secondary dead', 'CO2')

        Note: returns None if any of the arguments are invalid.
        """
        return super(Fccs2Ef, self)._get(fccs_fuelbed_id=fccs_fuelbed_id,
            phase=phase, fuel_category=fuel_category,
            fuel_sub_category=fuel_sub_category, species=species)


class CoverType2Ef(BaseLookUp):

    def _top_level_mapping(self):
        return self._cover_type_2_ef_group

    def get(self, cover_type_id, phase, fuel_category,
            fuel_sub_category, species):
        """Looks up and returns emissions factor info for the cover type

        Args:
         - cover_type_id -- cover type id
         - phase
         - fuel_category
         - fuel_sub_category
         - species

        Examples:
        >>> CoverType2Ef().get(121, 'flaming', 'shrub', 'secondary dead', 'CO2')

        Note: returns None if any of the arguments are invalid.
        """
        return super(CoverType2Ef, self)._get(cover_type_id=cover_type_id,
            phase=phase, fuel_category=fuel_category,
            fuel_sub_category=fuel_sub_category, species=species)

