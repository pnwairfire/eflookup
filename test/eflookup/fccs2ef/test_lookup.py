"""test_lookup.py:  tests for looking up EFs by FCCS id or cover type.
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2015, AirFire, PNW, USFS"

from eflookup.fccs2ef.lookup import LookUp, Fccs2Ef, CoverType2Ef
from py.test import raises

FCCS_2_COVER_TYPE_DATA="""fccs_id,cover_type_id
0,0
1,13
10,130
71,232
100,307
101,104
102,104
103,104
104,104
105,104
"""

COVER_TYPE_2_EF_GROUP_DATA="""cover_type_id,wf,rx
13,6,6
130,6,5
307,4,3
104,1,1
232,,
"""

EF_GROUP_2_EF_DATA="""Pollutant,Formula,1,2,3,4,5,6,7,8
Carbon Dioxide,CO2,,3282.0000,3196.0000,3200.0000,3348.0000,3410.0000,,2742.0000
Methane,CH4,4.6400,6.7600,9.7200,14.6400,7.3800,3.9000,27.8800,15.8900
Nitrogen Oxides,NOx,3.4000,2.0000,4.1200,4.0000,4.3600,4.3600,0.0000,1.3400
Sulfur Dioxide,SO2,2.1200,2.1200,2.1200,2.1200,1.3600,1.3600,0.0000,3.5200
PM2.5,PM2.5,25.1600,43.0000,35.1400,46.4000,14.1200,17.0200,66.0000,70.6000
Total non-methane VOCs,NMOC,32.0920,46.3040,53.9500,67.7480,34.9976,35.2902,90.3500,123.3910
MethylCyclopentadiene_i1,isomer1_C6H8,0.0120,0.0160,0.0200,0.0260,0.0115,0.0115,0.0380,0.0560
"1,3,5-Trimethylbenzene",C9H12,0.0400,0.0060,0.0300,0.0400,0.0286,0.0286,0.0500,0.0420
"""

##
## Base Classes
##

class LookUpTestBase(object):
    EXPECTED_FCCS_10_CT_130_WF = {
        'flaming': {  # 9
            'CO2': 3410.0000,
            'CH4': 3.9000,
            'NOx': 4.3600,
            'SO2': 1.3600,
            'PM2.5': 17.0200,
            'NMOC': 35.2902,
            "isomer1_C6H8": 0.0115,
            "C9H12": 0.0286
        },
        'smoldering': {  # 9
            'CO2': 3410.0000,
            'CH4': 3.9000,
            'NOx': 4.3600,
            'SO2': 1.3600,
            'PM2.5': 17.0200,
            'NMOC': 35.2902,
            "isomer1_C6H8": 0.0115,
            "C9H12": 0.0286
        },
        'residual': {
            'woody': {  # 3
                'CO2': None,
                'CH4': 27.8800,
                'NOx': 0.0000,
                'SO2': 0.0000,
                'PM2.5': 66.0000,
                'NMOC': 90.3500,
                "isomer1_C6H8": 0.0380,
                "C9H12": 0.0500
            },
            'duff': {  # 10
                'CO2': 2742.0000,
                'CH4': 15.8900,
                'NOx': 1.3400,
                'SO2': 3.5200,
                'PM2.5': 70.6000,
                'NMOC': 123.3910,
                "isomer1_C6H8": 0.0560,
                "C9H12": 0.0420
            }
        }
    }
    EXPECTED_FCCS_10_CT_130_RX = {
        'flaming': {  # 5
            'CO2': 3348.0000,
            'CH4': 7.3800,
            'NOx': 4.3600,
            'SO2': 1.3600,
            'PM2.5': 14.1200,
            'NMOC': 34.9976,
            "isomer1_C6H8": 0.0115,
            "C9H12": 0.0286,
        },
        'smoldering': {  # 5
            'CO2': 3348.0000,
            'CH4': 7.3800,
            'NOx': 4.3600,
            'SO2': 1.3600,
            'PM2.5': 14.1200,
            'NMOC': 34.9976,
            "isomer1_C6H8": 0.0115,
            "C9H12": 0.0286,
        },
        'residual': {
            'woody': {  # 3
                'CO2': None,
                'CH4': 27.8800,
                'NOx': 0.0000,
                'SO2': 0.0000,
                'PM2.5': 66.0000,
                'NMOC': 90.3500,
                "isomer1_C6H8": 0.0380,
                "C9H12": 0.0500
            },
            'duff': {  # 10
                'CO2': 2742.0000,
                'CH4': 15.8900,
                'NOx': 1.3400,
                'SO2': 3.5200,
                'PM2.5': 70.6000,
                'NMOC': 123.3910,
                "isomer1_C6H8": 0.0560,
                "C9H12": 0.0420
            }
        }
    }
    EXPECTED_FCCS_71_CT_232 = {
        'residual': {
            'woody': {  # 3
                'CO2': None,
                'CH4': 27.8800,
                'NOx': 0.0000,
                'SO2': 0.0000,
                'PM2.5': 66.0000,
                'NMOC': 90.3500,
                "isomer1_C6H8": 0.0380,
                "C9H12": 0.0500
            },
            'duff': {  # 10
                'CO2': 2742.0000,
                'CH4': 15.8900,
                'NOx': 1.3400,
                'SO2': 3.5200,
                'PM2.5': 70.6000,
                'NMOC': 123.3910,
                "isomer1_C6H8": 0.0560,
                "C9H12": 0.0420
            }
        }
    }

    def create_look_up_object(self, tmpdir, look_up_class, is_rx):
        f2c = tmpdir.join("f2c.csv")
        f2c.write(FCCS_2_COVER_TYPE_DATA)
        ct2efg = tmpdir.join("ct2efg.csv")
        ct2efg.write(COVER_TYPE_2_EF_GROUP_DATA)
        efg2ef = tmpdir.join("efg2ef.csv")
        efg2ef.write(EF_GROUP_2_EF_DATA)
        return look_up_class(
            is_rx,
            fccs_2_cover_type_file=str(f2c),
            cover_type_2_ef_group_file=str(ct2efg),
            ef_group_2_ef_file=str(efg2ef)
        )

    def raises_key_error(self, l):
        with raises(KeyError):
            l()

class Fccs2EfAndCoverType2EfBase(LookUpTestBase):

    def _test_load_and_getitem(self, tmpdir, lu, f_s_r_expected, f_s_r_id, r_id):
        # cases where FCCS id doesn't exist
        self.raises_key_error(lambda: lu[999])
        self.raises_key_error(lambda: lu[999]['flaming'])
        self.raises_key_error(lambda: lu[999]['flaming']['CO2'])
        # cases where phase doesn't exist
        self.raises_key_error(lambda: lu[f_s_r_id]['flamsdflkjsdf'])
        self.raises_key_error(lambda: lu[f_s_r_id]['flamsdflkjsdf']['CO2'])
        # residual cases where fuel category doesn't exist or doesn't have residual EFs
        self.raises_key_error(lambda: lu[f_s_r_id]['residual']['foo_bar'])
        # cases where chemical species doesn't exist
        self.raises_key_error(lambda: lu[f_s_r_id]['flaming']['sdfsdf'])
        # cases where ef set type isn't defined
        self.raises_key_error(lambda: lu[r_id]['flaming'])
        self.raises_key_error(lambda: lu[r_id]['flaming']['CO2'])
        # cases where species isn't defined
        assert None == lu[f_s_r_id]['residual']['woody']['CO2']

        assert f_s_r_expected == lu[f_s_r_id]
        assert f_s_r_expected['flaming'] == lu[f_s_r_id]['smoldering']
        assert f_s_r_expected['residual'] == lu[f_s_r_id]['residual']
        assert f_s_r_expected['residual']['duff'] == lu[f_s_r_id]['residual']['duff']
        assert f_s_r_expected['residual']['duff']['PM2.5'] == lu[f_s_r_id]['residual']['duff']['PM2.5']
        assert self.EXPECTED_FCCS_71_CT_232 == lu[r_id]
        assert self.EXPECTED_FCCS_71_CT_232['residual'] == lu[r_id]['residual']
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff'] == lu[r_id]['residual']['duff']
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff']['PM2.5'] == lu[r_id]['residual']['duff']['PM2.5']

    def _test_load_and_get(self, tmpdir, lu, f_s_r_expected, f_s_r_id, r_id):
        # cases where FCCS id doesn't exist
        assert None == lu.get(999)
        assert None == lu.get(999, phase='flaming')
        assert None == lu.get(999, phase='flaming', species='CO2')
        # cases where ef group type doesn't exist
        assert None == lu.get(f_s_r_id, phase='flamsdflkjsdf')
        assert None == lu.get(f_s_r_id, phase='flamsdflkjsdf', species='CO2')
        # residual cases where fuel category doesn't exist or doesn't have residual EFs
        assert None == lu.get(f_s_r_id, phase='residual', fuel_category='foo_bar')
        assert None == lu.get(f_s_r_id, phase='residual', fuel_category='foo_bar', species='PM2.5')
        # cases where chemical species doesn't exist
        assert None == lu.get(f_s_r_id, phase='flaming', species='sdfsdf')
        # cases where ef set type isn't defined
        assert None == lu.get(r_id, phase='flaming')
        assert None == lu.get(r_id, phase='flaming', species='CO2')
        # cases where species isn't defined
        assert None == lu.get(f_s_r_id, phase='residual', fuel_category="woody", species='CO2')

        assert f_s_r_expected == lu.get(f_s_r_id)
        assert f_s_r_expected['flaming'] == lu.get(f_s_r_id, phase='flaming')
        assert f_s_r_expected['residual'] == lu.get(f_s_r_id, phase='residual')
        assert f_s_r_expected['residual']['duff'] == lu.get(f_s_r_id, phase='residual', fuel_category='duff')
        assert f_s_r_expected['residual']['duff']['PM2.5'] == lu.get(f_s_r_id, phase='residual', fuel_category='duff', species='PM2.5')
        assert self.EXPECTED_FCCS_71_CT_232 == lu.get(r_id)
        assert self.EXPECTED_FCCS_71_CT_232['residual'] == lu.get(r_id, phase='residual')
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff'] == lu.get(r_id, phase='residual', fuel_category='duff')
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff']['PM2.5'] == lu.get(r_id, phase='residual', fuel_category='duff', species='PM2.5')

    def test_load_and_getitem_wf(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS, False)
        self._test_load_and_getitem(tmpdir, lu, self.EXPECTED_FCCS_10_CT_130_WF, self.F_S_R_ID, self.R_ID)

    def test_load_and_getitem_rx(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS, True)
        self._test_load_and_getitem(tmpdir, lu, self.EXPECTED_FCCS_10_CT_130_RX, self.F_S_R_ID, self.R_ID)

    def test_load_and_get_wf(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS, False)
        self._test_load_and_get(tmpdir, lu, self.EXPECTED_FCCS_10_CT_130_WF, self.F_S_R_ID, self.R_ID)

    def test_load_and_get_rx(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS, True)
        self._test_load_and_get(tmpdir, lu, self.EXPECTED_FCCS_10_CT_130_RX, self.F_S_R_ID, self.R_ID)

##
## Actual Tests
##

class TestLookUp(LookUpTestBase):
    LOOKUP_CLASS = LookUp

    def _test_load_and_get(self, tmpdir, lu, f_s_r_expected):

        # Neither fccs_fuelbed_id nor cover_type_id is specified
        with raises(LookupError):
            lu.get()
        # both fccs_fuelbed_id and cover_type_id is specified
        with raises(LookupError):
            lu.get(fccs_fuelbed_id=10, cover_type_id=130)

        # fuel category is specified without phase
        with raises(LookupError):
            lu.get(fuel_category='woody')
        # species is specified without phase
        with raises(LookupError):
            lu.get(species='CO2')
        # fuel category and species are specified without phase
        with raises(LookupError):
            lu.get(fuel_category='woody', species='CO2')
        # species is specified without fuel_category for residual phase
        with raises(LookupError):
            lu.get(phase='residual', species='CO2')

        # cases where FCCS id or cover type doesn't exist
        assert None == lu.get(fccs_fuelbed_id=999)
        assert None == lu.get(cover_type_id=999)
        assert None == lu.get(fccs_fuelbed_id=999, phase='flaming')
        assert None == lu.get(cover_type_id=999, phase='flaming')
        assert None == lu.get(fccs_fuelbed_id=999, phase='flaming', species='CO2')
        assert None == lu.get(cover_type_id=999, phase='flaming', species='CO2')
        # cases where phase type doesn't exist
        assert None == lu.get(fccs_fuelbed_id=10, phase='foo_bar_phase')
        assert None == lu.get(cover_type_id=130, phase='foo_bar_phase')
        assert None == lu.get(fccs_fuelbed_id=10, phase='foo_bar_phase', species='CO2')
        assert None == lu.get(cover_type_id=130, phase='foo_bar_phase', species='CO2')
        # residual cases where fuel category doesn't exist or doesn't have residual EFs
        assert None == lu.get(fccs_fuelbed_id=10, phase='residual', fuel_category='foo_bar')
        assert None == lu.get(cover_type_id=130, phase='residual', fuel_category='foo_bar')
        assert None == lu.get(fccs_fuelbed_id=10, phase='residual', fuel_category='foo_bar', species='CO2')
        assert None == lu.get(cover_type_id=130, phase='residual', fuel_category='foo_bar', species='CO2')
        # cases where chemical species doesn't exist
        assert None == lu.get(fccs_fuelbed_id=10, phase='flaming', species='sdfsdf')
        assert None == lu.get(cover_type_id=130, phase='flaming', species='sdfsdf')
        assert None == lu.get(fccs_fuelbed_id=10, phase='residual', fuel_category="duff", species='sdfsdf')
        assert None == lu.get(cover_type_id=130, phase='residual', fuel_category="duff", species='sdfsdf')
        # cases where ef set type isn't defined
        assert None == lu.get(fccs_fuelbed_id=71, phase='flaming')
        assert None == lu.get(cover_type_id=232, phase='flaming')
        assert None == lu.get(fccs_fuelbed_id=71, phase='flaming', species='CO2')
        assert None == lu.get(cover_type_id=232, phase='flaming', species='CO2')
        # cases where species isn't defined
        assert None == lu.get(fccs_fuelbed_id=10, phase='residual', fuel_category="woody", species='CO2')
        assert None == lu.get(cover_type_id=130, phase='residual', fuel_category="woody", species='CO2')

        assert f_s_r_expected == lu.get(fccs_fuelbed_id=10)
        assert f_s_r_expected == lu.get(cover_type_id=130)
        assert f_s_r_expected['flaming'] == lu.get(fccs_fuelbed_id=10, phase='flaming')
        assert f_s_r_expected['flaming'] == lu.get(cover_type_id=130, phase='flaming')
        assert f_s_r_expected['residual'] == lu.get(fccs_fuelbed_id=10, phase='residual')
        assert f_s_r_expected['residual'] == lu.get(cover_type_id=130, phase='residual')
        assert f_s_r_expected['residual']['duff'] == lu.get(fccs_fuelbed_id=10, phase='residual', fuel_category='duff')
        assert f_s_r_expected['residual']['duff'] == lu.get(cover_type_id=130, phase='residual', fuel_category='duff')
        assert f_s_r_expected['residual']['duff']['PM2.5'] == lu.get(fccs_fuelbed_id=10, phase='residual', fuel_category='duff', species='PM2.5')
        assert f_s_r_expected['residual']['duff']['PM2.5'] == lu.get(cover_type_id=130, phase='residual', fuel_category='duff', species='PM2.5')
        assert self.EXPECTED_FCCS_71_CT_232 == lu.get(fccs_fuelbed_id=71)
        assert self.EXPECTED_FCCS_71_CT_232 == lu.get(cover_type_id=232)
        assert self.EXPECTED_FCCS_71_CT_232['residual'] == lu.get(fccs_fuelbed_id=71, phase='residual')
        assert self.EXPECTED_FCCS_71_CT_232['residual'] == lu.get(cover_type_id=232, phase='residual')
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff'] == lu.get(fccs_fuelbed_id=71, phase='residual', fuel_category='duff')
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff'] == lu.get(cover_type_id=232, phase='residual', fuel_category='duff')
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff']['PM2.5'] == lu.get(fccs_fuelbed_id=71, phase='residual', fuel_category='duff', species='PM2.5')
        assert self.EXPECTED_FCCS_71_CT_232['residual']['duff']['PM2.5'] == lu.get(cover_type_id=232, phase='residual', fuel_category='duff', species='PM2.5')

    def test_load_and_get_wf(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS, False)
        self._test_load_and_get(tmpdir, lu, self.EXPECTED_FCCS_10_CT_130_WF)

    def test_load_and_get_rx(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS, True)
        self._test_load_and_get(tmpdir, lu, self.EXPECTED_FCCS_10_CT_130_RX)

class TestFccs2Ef(Fccs2EfAndCoverType2EfBase):
    # Fccs2EfAndCoverType2EfBase contains all of the test code, which uses
    # LOOKUP_CLASS and F_S_R_ID to trigger the correct test logic
    LOOKUP_CLASS = Fccs2Ef
    F_S_R_ID = 10
    R_ID = 71

class TestCoverType2Ef(Fccs2EfAndCoverType2EfBase):
    LOOKUP_CLASS = CoverType2Ef
    F_S_R_ID = 130
    R_ID = 232


class TestSpecies(LookUpTestBase):

    def test_wf_species(self, tmpdir):
        expected_flaming = {
            'CO2','CH4','NOx','SO2','PM2.5','NMOC',"isomer1_C6H8","C9H12"
        }
        expected_smoldering = {
            'CO2','CH4','NOx','SO2','PM2.5','NMOC',"isomer1_C6H8","C9H12"
        }
        expected_residual = {
            'CO2','CH4','NOx','SO2','PM2.5','NMOC',"isomer1_C6H8","C9H12"
        }

        lu = self.create_look_up_object(tmpdir, Fccs2Ef, False)
        assert expected_flaming == lu[10].species('flaming')
        assert expected_smoldering == lu[10].species('smoldering')
        assert expected_residual == lu[10].species('residual')

        lu = self.create_look_up_object(tmpdir, CoverType2Ef, False)
        assert expected_flaming == lu[130].species('flaming')
        assert expected_smoldering == lu[130].species('smoldering')
        assert expected_residual == lu[130].species('residual')

    def test_rx_species(self, tmpdir):
        expected_flaming = {
            'CO2','CH4','NOx','SO2','PM2.5','NMOC',"isomer1_C6H8","C9H12"
        }
        expected_smoldering = {
            'CO2','CH4','NOx','SO2','PM2.5','NMOC',"isomer1_C6H8","C9H12"
        }
        expected_residual = {
            'CO2','CH4','NOx','SO2','PM2.5','NMOC',"isomer1_C6H8","C9H12"
        }

        lu = self.create_look_up_object(tmpdir, Fccs2Ef, True)
        assert expected_flaming == lu[10].species('flaming')
        assert expected_smoldering == lu[10].species('smoldering')
        assert expected_residual == lu[10].species('residual')

        lu = self.create_look_up_object(tmpdir, CoverType2Ef, True)
        assert expected_flaming == lu[130].species('flaming')
        assert expected_smoldering == lu[130].species('smoldering')
        assert expected_residual == lu[130].species('residual')

    def test_residual_only_species(self, tmpdir):
        expected_flaming = set()
        expected_smoldering = set()
        expected_residual = {
            'CO2','CH4','NOx','SO2','PM2.5','NMOC',"isomer1_C6H8","C9H12"
        }

        lu = self.create_look_up_object(tmpdir, Fccs2Ef, True)
        assert expected_flaming == lu[71].species('flaming')
        assert expected_smoldering == lu[71].species('smoldering')
        assert expected_residual == lu[71].species('residual')

        lu = self.create_look_up_object(tmpdir, CoverType2Ef, True)
        assert expected_flaming == lu[232].species('flaming')
        assert expected_smoldering == lu[232].species('smoldering')
        assert expected_residual == lu[232].species('residual')
