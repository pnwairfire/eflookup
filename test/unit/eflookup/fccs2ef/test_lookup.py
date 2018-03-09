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
    "1":{"regrx":"24-26","rx":"6","wf":"5",},
    "10":{"regrx":"24-26","rx":"6","wf":"5",}
}

CAT_PHASE_2_EF_GROUP = {
    "24-26": {
        "canopy":{
            "ladder fuels":{
                "flaming":{"NH3":"24","NOx":"24","PM25":"24","SO2":"24",},
                "residual":{"NH3":None,"NOx":"25","PM25":None,"SO2":None,},
                "smoldering":{"NH3":"24","NOx":"24","PM25":"24","SO2":"24",},
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
        "CO":"61",
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
        "CH4":"3",
        "CO":"2",
        "CO2":"1",
        "PM10":"10.1",
        "PM2.5":"12.51"
    },
    "24":{
        "CH4":"1.98",
        "CO":"55.8",
        "CO2":"1531",
        "PM10":"",
        "PM2.5":"9.89"
    },
    "25":{
        "CH4":"4",
        "CO":"3",
        "CO2":"2",
        "PM10":"1",
        "PM2.5":""
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

        self.fccs2ef_213_rx = Fccs2Ef('213', True)
        self.fccs2ef_213_wf = Fccs2Ef('213', False)
        self.ct2ef_213_rx = CoverType2Ef('1', True)
        self.ct2ef_213_wf = CoverType2Ef('10', False)

    def test_invalid_get(self):
        # fccs id 1 isn't in ou
        with raises(KeyError) as e_info:
            Fccs2Ef("1", True)
        with raises(KeyError) as e_info:
            Fccs2Ef("1", False)
        with raises(KeyError) as e_info:
            CoverType2Ef("2", True)
        with raises(KeyError) as e_info:
            CoverType2Ef("2", False)

        with raises(LookupError) as e_info:
            self.fccs2ef_213_rx.get()
        with raises(LookupError) as e_info:
            self.fccs2ef_213_wf.get()
        with raises(LookupError) as e_info:
            self.ct2ef_213_rx.get()
        with raises(LookupError) as e_info:
            self.ct2ef_213_wf.get()
        with raises(LookupError) as e_info:
            self.fccs2ef_213_rx.get(phase='phase')
        with raises(LookupError) as e_info:
            self.fccs2ef_213_wf.get(phase='phase')
        with raises(LookupError) as e_info:
            self.ct2ef_213_rx.get(phase='phase')
        with raises(LookupError) as e_info:
            self.ct2ef_213_wf.get(phase='phase')
        with raises(LookupError) as e_info:
            self.fccs2ef_213_rx.get(phase='phase', fuel_category='cat')
        with raises(LookupError) as e_info:
            self.fccs2ef_213_wf.get(phase='phase', fuel_category='cat')
        with raises(LookupError) as e_info:
            self.ct2ef_213_rx.get(phase='phase', fuel_category='cat')
        with raises(LookupError) as e_info:
            self.ct2ef_213_wf.get(phase='phase', fuel_category='cat')
        with raises(LookupError) as e_info:
            self.fccs2ef_213_rx.get(phase='phase', fuel_category='cat',
                fuel_sub_category='subcat')
        with raises(LookupError) as e_info:
            self.fccs2ef_213_wf.get(phase='phase', fuel_category='cat',
                fuel_sub_category='subcat')
        with raises(LookupError) as e_info:
            self.ct2ef_213_rx.get(phase='phase', fuel_category='cat',
                fuel_sub_category='subcat')
        with raises(LookupError) as e_info:
            self.ct2ef_213_wf.get(phase='phase', fuel_category='cat',
                fuel_sub_category='subcat')

    def test_nonexisting_get(self):
        assert None == self.fccs2ef_213_rx.get(phase='phase',
            fuel_category='cat', fuel_sub_category='subcat', species='species')
        assert None == self.fccs2ef_213_wf.get(phase='phase',
            fuel_category='cat', fuel_sub_category='subcat', species='species')
        assert None == self.ct2ef_213_rx.get(phase='phase',
            fuel_category='cat', fuel_sub_category='subcat', species='species')
        assert None == self.ct2ef_213_wf.get(phase='phase',
            fuel_category='cat', fuel_sub_category='subcat', species='species')

    def test_get(self):
        # No override specified
        # 'None' override
        # float value override
        pass

    def test_species(self):
        pass
