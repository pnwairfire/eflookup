"""test_lookup.py:  tests for looking up EFs by FCCS id or cover type.
"""

__author__      = "Joel Dubowy"

from eflookup.fccs2ef.lookup import Fccs2Ef, CoverType2Ef
from eflookup.fccs2ef.data import (
    catphase2efgroup,
    covertype2efgroup,
    efgroup2ef,
    fccs2covertype,
)
from py.test import raises

FCCS_2_COVERTYPE = {
    "213":"1",
    "222":"10",
}

COVERTYPE_2_EF_GROUP = {
    "1":{"regrx":"24-26","rx":"6","wf":"5", "regwf": None},
    "10":{"regrx":"24-26","rx":"6","wf":"5", "regwf": "21-23"}
}

CAT_PHASE_2_EF_GROUP = {
    "24-26": {
        "canopy":{
            "ladder fuels":{
                "flaming":{"NH3":"24","PM2.5":"24"},
                "residual":{"NH3":None,"PM2.5":None},
                "smoldering":{"NH3":"24","PM2.5":"24"},
            }
        }
    },
    "21-23": {
        "canopy":{
            "ladder fuels":{
                "flaming":{"NH3":"24","PM2.5":"25"},
                "residual":{"NH3":None,"PM2.5":None},
                "smoldering":{"NH3":"24","PM2.5":"24"},
            }
        }
    }
}

EF_GROUP_2_EF = {
    "5": {
        "CH4":"2.95",
        "CO":"62",
        "CO2":"170",
        "PM10":"1.0418",
        "PM2.5":"9.51"
    },
    "6": {
        "CH4":"1.95",
        "CO2":"1705",
        "PM10":"10.0418",
        "PM2.5":"8.51"
    },
    "7": {
        "CH4":"3",
        "CO":"2",
        "CO2":"1",
        "PM10":"10.1",
        "PM2.5":"12.51"
    },
    "8": {
        "CH4":"33",
        "CO":"22",
        "CO2":"11",
        "PM10":"110.1",
        "PM2.5":"122.51"
    },
    "24":{
        "CH4":"1.98",
        "CO":"55.8",
        "CO2":"1531",
        "PM2.5":"9.89"
    },
    "25":{
        "CH4":"4",
        "CO":"3",
        "CO2":"2",
        "PM10":"1"
    },
}


##
## Base Classes
##

class TestFccs2EfAndCovertype2EF(object):

    def setup(self):
        fccs2covertype.FCCS_2_COVERTYPE = FCCS_2_COVERTYPE
        efgroup2ef.EF_GROUP_2_EF = EF_GROUP_2_EF
        covertype2efgroup.COVERTYPE_2_EF_GROUP = COVERTYPE_2_EF_GROUP
        catphase2efgroup.CAT_PHASE_2_EF_GROUP = CAT_PHASE_2_EF_GROUP

        self.lookups = {
            "fccs2ef_213_rx": Fccs2Ef('213', True),
            "fccs2ef_213_wf": Fccs2Ef('213', False),
            "ct2ef_1_rx": CoverType2Ef('1', True),
            "ct2ef_10_wf": CoverType2Ef('10', False)
        }

    def test_invalid_fccs_and_covertype_ids(self):
        # fccs id 1 isn't in ou
        with raises(ValueError) as e_info:
            Fccs2Ef("1", True)
        with raises(ValueError) as e_info:
            Fccs2Ef("1", False)
        with raises(ValueError) as e_info:
            CoverType2Ef("2", True)
        with raises(ValueError) as e_info:
            CoverType2Ef("2", False)

    def test_invalid_get(self):
        for l in self.lookups.values():
            # nothing specified
            with raises(LookupError) as e_info:
                l.get()
            # only phase is specified
            with raises(LookupError) as e_info:
                l.get(phase='phase')
            with raises(LookupError) as e_info:
                l.get(phase='phase', fuel_category='cat')
            with raises(LookupError) as e_info:
                l.get(phase='phase', fuel_category='cat',
                    fuel_sub_category='subcat')

    def test_get_nonexisting_phase(self):
        for l in self.lookups.values():
            # invalid phase
            assert None == l.get(phase='foo', fuel_category='canopy', fuel_sub_category='ladder fuels', species='NH3')
            assert None == l.get(phase='foo', fuel_category='canopy', fuel_sub_category='overstory', species='NH3')

    def test_get_nonexisting_species(self):
        for l in self.lookups.values():
            # invalid species
            assert None == l.get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='foo')
            assert None == l.get(phase='phase', fuel_category='cat',
                fuel_sub_category='subcat', species='species')

    def test_get_existing_no_override(self):
        ## neither 'nonwoody' nor 'primary live' is in the overrides
        for l in self.lookups.values():
            # NH3 isn't specified
            assert None == l.get(phase='flaming', fuel_category='nonwoody', fuel_sub_category='primary live', species='NH3')
        # rx is EFG 6
        assert 8.51 == self.lookups['fccs2ef_213_rx'].get(phase='flaming', fuel_category='nonwoody', fuel_sub_category='primary live', species='PM2.5')
        assert 8.51 == self.lookups['ct2ef_1_rx'].get(phase='flaming', fuel_category='nonwoody', fuel_sub_category='primary live', species='PM2.5')
        # ef is EFG 5
        assert 9.51 == self.lookups['fccs2ef_213_wf'].get(phase='flaming', fuel_category='nonwoody', fuel_sub_category='primary live', species='PM2.5')
        assert 9.51 == self.lookups['ct2ef_10_wf'].get(phase='flaming', fuel_category='nonwoody', fuel_sub_category='primary live', species='PM2.5')

        ## 'canopy' is in overrides, but 'overstory' isn't
        for l in self.lookups.values():
            # NH3 isn't specified
            assert None == l.get(phase='flaming', fuel_category='canopy', fuel_sub_category='overstory', species='NH3')
        # rx is EFG 6
        assert 8.51 == self.lookups['fccs2ef_213_rx'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='overstory', species='PM2.5')
        assert 8.51 == self.lookups['ct2ef_1_rx'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='overstory', species='PM2.5')
        # ef is EFG 5
        assert 9.51 == self.lookups['fccs2ef_213_wf'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='overstory', species='PM2.5')
        assert 9.51 == self.lookups['ct2ef_10_wf'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='overstory', species='PM2.5')

        ## 'ladder fuels' is in overrides, but woody fuels isn't
        for l in self.lookups.values():
            assert None == l.get(phase='flaming', fuel_category='woody fuels', fuel_sub_category='ladder fuels', species='NH3') # woody fuels > ladder fuels would never really happen
        # rx is EFG 6
        assert 8.51 == self.lookups['fccs2ef_213_rx'].get(phase='flaming', fuel_category='woody fuels', fuel_sub_category='ladder fuels', species='PM2.5') # woody fuels > ladder fuels would never really happen
        assert 8.51 == self.lookups['ct2ef_1_rx'].get(phase='flaming', fuel_category='woody fuels', fuel_sub_category='ladder fuels', species='PM2.5') # woody fuels > ladder fuels would never really happen
        # wf is EFG 5
        assert 9.51 == self.lookups['fccs2ef_213_wf'].get(phase='flaming', fuel_category='woody fuels', fuel_sub_category='ladder fuels', species='PM2.5') # woody fuels > ladder fuels would never really happen
        assert 9.51 == self.lookups['ct2ef_10_wf'].get(phase='flaming', fuel_category='woody fuels', fuel_sub_category='ladder fuels', species='PM2.5') # woody fuels > ladder fuels would never really happen

        ## 'canopy' > 'ladder fuels' is in overrides, but C02 isn't
        for l in self.lookups.values():
            assert None == l.get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='C11H22')
        # rx is EFG 6
        assert 1705 == self.lookups['fccs2ef_213_rx'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='CO2')
        assert 1705 == self.lookups['ct2ef_1_rx'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='CO2')
        assert None == self.lookups['ct2ef_1_rx'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='CO')
        # wf is EFG 5
        assert 170 == self.lookups['fccs2ef_213_wf'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='CO2')
        assert 170 == self.lookups['ct2ef_10_wf'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='CO2')

        ## Other
        for l in self.lookups.values():
            assert None == l.get(phase='residual', fuel_category='canopy', fuel_sub_category='ladder fuels', species='CO2') # no residual emissions
            assert 1 == l.get(phase='residual', fuel_category='woody fuels', fuel_sub_category='1000-hr fuels rotten', species='CO2') #CWD - EFG 7
            assert 11 == l.get(phase='residual', fuel_category='ground fuels', fuel_sub_category='duff upper', species='CO2') #duff - EFG 8

    def test_get_existing_w_None_override(self):
        for l in self.lookups.values():
            assert None == l.get(phase='residual', fuel_category='canopy', fuel_sub_category='ladder fuels', species='NH3')

    def test_get_existing_w_float_override_for_rx_only(self):
        assert 9.89 == self.lookups['fccs2ef_213_rx'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='PM2.5')
        assert 9.51 == self.lookups['fccs2ef_213_wf'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='PM2.5')
        assert 9.89 == self.lookups['ct2ef_1_rx'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='PM2.5')
        assert None == self.lookups['ct2ef_10_wf'].get(phase='flaming', fuel_category='canopy', fuel_sub_category='ladder fuels', species='PM2.5')

    def test_species(self):
        pass
