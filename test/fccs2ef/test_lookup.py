"""test_lookup.py:  tests for looking up EFs by FCCS id or cover type.
"""

from fccs2ef.lookup import LookUp, FCCSLookup, CoverTypeLookup
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

class LookUpTestBase(object):
    EXPECTED_FCCS_10_CT_130 = {
        'flame_smold_wf': {  # 9
            'CO2': 3410.0000,
            'CH4': 3.9000,
            'NOx': 4.3600,
            'SO2': 1.3600,
            'PM2.5': 17.0200,
            'NMOC': 35.2902,
            "isomer1_C6H8": 0.0115,
            "C9H12": 0.0286
        },
        'flame_smold_rx': {  # 5
            'CO2': 3348.0000,
            'CH4': 7.3800,
            'NOx': 4.3600,
            'SO2': 1.3600,
            'PM2.5': 14.1200,
            'NMOC': 34.9976,
            "isomer1_C6H8": 0.0115,
            "C9H12": 0.0286,
        },
        'woody_rsc': {  # 3
            'CO2': None,
            'CH4': 27.8800,
            'NOx': 0.0000,
            'SO2': 0.0000,
            'PM2.5': 66.0000,
            'NMOC': 90.3500,
            "isomer1_C6H8": 0.0380,
            "C9H12": 0.0500
        },
        'duff_rsc': {  # 10
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
    EXPECTED_FCCS_71_CT_232 = {
        'woody_rsc': {  # 3
            'CO2': None,
            'CH4': 27.8800,
            'NOx': 0.0000,
            'SO2': 0.0000,
            'PM2.5': 66.0000,
            'NMOC': 90.3500,
            "isomer1_C6H8": 0.0380,
            "C9H12": 0.0500
        },
        'duff_rsc': {  # 10
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

    def create_look_up_object(self, tmpdir, look_up_class):
        f2c = tmpdir.join("f2c.csv")
        f2c.write(FCCS_2_COVER_TYPE_DATA)
        ct2efg = tmpdir.join("ct2efg.csv")
        ct2efg.write(COVER_TYPE_2_EF_GROUP_DATA)
        efg2ef = tmpdir.join("efg2ef.csv")
        efg2ef.write(EF_GROUP_2_EF_DATA)
        return self.LOOKUP_CLASS(
            fccs_2_cover_type_file=str(f2c),
            cover_type_2_ef_group_file=str(ct2efg),
            ef_group_2_ef_file=str(efg2ef)
        )

    def raises_key_error(self, l):
        with raises(KeyError):
            l()

class TestLookUp(LookUpTestBase):
    LOOKUP_CLASS = LookUp

    def test_load_and_get(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS)
        # Neither fccs_fuel_bed_id nor cover_type_id is specified
        with raises(LookupError):
            lu.get()
        # both fccs_fuel_bed_id and cover_type_id is specified
        with raises(LookupError):
            lu.get(fccs_fuel_bed_id=10, cover_type_id=130)
        # cases where FCCS id or cover type doesn't exist
        assert None == lu.get(fccs_fuel_bed_id=999)
        assert None == lu.get(cover_type_id=999)
        assert None == lu.get(fccs_fuel_bed_id=999, ef_set_type='duff_rsc')
        assert None == lu.get(cover_type_id=999, ef_set_type='duff_rsc')
        assert None == lu.get(fccs_fuel_bed_id=999, ef_set_type='duff_rsc', species='CO2')
        assert None == lu.get(cover_type_id=999, ef_set_type='duff_rsc', species='CO2')
        # cases where ef group type doesn't exist
        assert None == lu.get(fccs_fuel_bed_id=10, ef_set_type='duffsdf')
        assert None == lu.get(cover_type_id=130, ef_set_type='duffsdf')
        assert None == lu.get(fccs_fuel_bed_id=10, ef_set_type='duffsdf', species='CO2')
        assert None == lu.get(cover_type_id=130, ef_set_type='duffsdf', species='CO2')
        # cases where chemical species doesn't exist
        assert None == lu.get(fccs_fuel_bed_id=10, ef_set_type='duff_rsc', species='sdfsdf')
        assert None == lu.get(cover_type_id=130, ef_set_type='duff_rsc', species='sdfsdf')
        # cases where ef set type isn't defined
        assert None == lu.get(fccs_fuel_bed_id=71, ef_set_type='flame_smold_wf')
        assert None == lu.get(cover_type_id=232, ef_set_type='flame_smold_wf')
        assert None == lu.get(fccs_fuel_bed_id=71, ef_set_type='flame_smold_wf', species='CO2')
        assert None == lu.get(cover_type_id=232, ef_set_type='flame_smold_wf', species='CO2')
        # cases where species isn't defined
        assert None == lu.get(fccs_fuel_bed_id=10, ef_set_type='woody_rsc', species='CO2')
        assert None == lu.get(cover_type_id=130, ef_set_type='woody_rsc', species='CO2')

        assert self.EXPECTED_FCCS_10_CT_130 == lu.get(fccs_fuel_bed_id=10)
        assert self.EXPECTED_FCCS_10_CT_130 == lu.get(cover_type_id=130)
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc'] == lu.get(fccs_fuel_bed_id=10, ef_set_type='duff_rsc')
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc'] == lu.get(cover_type_id=130, ef_set_type='duff_rsc')
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc']['PM2.5'] == lu.get(fccs_fuel_bed_id=10, ef_set_type='duff_rsc', species='PM2.5')
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc']['PM2.5'] == lu.get(cover_type_id=130, ef_set_type='duff_rsc', species='PM2.5')
        assert self.EXPECTED_FCCS_71_CT_232 == lu.get(fccs_fuel_bed_id=71)
        assert self.EXPECTED_FCCS_71_CT_232 == lu.get(cover_type_id=232)
        assert self.EXPECTED_FCCS_71_CT_232['duff_rsc'] == lu.get(fccs_fuel_bed_id=71, ef_set_type='duff_rsc')
        assert self.EXPECTED_FCCS_71_CT_232['duff_rsc'] == lu.get(cover_type_id=232, ef_set_type='duff_rsc')

class TestFCCSLookup(LookUpTestBase):
    LOOKUP_CLASS = FCCSLookup

    def test_load_and_getitem(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS)

        # cases where FCCS id doesn't exist
        self.raises_key_error(lambda: lu[999])
        self.raises_key_error(lambda: lu[999]['duff_rsc'])
        self.raises_key_error(lambda: lu[999]['duff_rsc']['CO2'])
        # cases where ef group type doesn't exist
        self.raises_key_error(lambda: lu[10]['duffsdf'])
        self.raises_key_error(lambda: lu[10]['duffsdf']['CO2'])
        # cases where chemical species doesn't exist
        self.raises_key_error(lambda: lu[10]['duff_rsc']['sdfsdf'])
        # cases where ef set type isn't defined
        self.raises_key_error(lambda: lu[71]['flame_smold_wf'])
        self.raises_key_error(lambda: lu[71]['flame_smold_wf']['CO2'])
        # cases where species isn't defined
        assert None == lu[10]['woody_rsc']['CO2']

        assert self.EXPECTED_FCCS_10_CT_130 == lu[10]
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc'] == lu[10]['duff_rsc']
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc']['PM2.5'] == lu[10]['duff_rsc']['PM2.5']
        assert self.EXPECTED_FCCS_71_CT_232 == lu[71]
        assert self.EXPECTED_FCCS_71_CT_232['duff_rsc'] == lu[71]['duff_rsc']


    def test_load_and_get(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS)
        # cases where FCCS id doesn't exist
        assert None == lu.get(999)
        assert None == lu.get(999, ef_set_type='duff_rsc')
        assert None == lu.get(999, ef_set_type='duff_rsc', species='CO2')
        # cases where ef group type doesn't exist
        assert None == lu.get(10, ef_set_type='duffsdf')
        assert None == lu.get(10, ef_set_type='duffsdf', species='CO2')
        # cases where chemical species doesn't exist
        assert None == lu.get(10, ef_set_type='duff_rsc', species='sdfsdf')
        # cases where ef set type isn't defined
        assert None == lu.get(71, ef_set_type='flame_smold_wf')
        assert None == lu.get(71, ef_set_type='flame_smold_wf', species='CO2')
        # cases where species isn't defined
        assert None == lu.get(10, ef_set_type='woody_rsc', species='CO2')

        assert self.EXPECTED_FCCS_10_CT_130 == lu.get(10)
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc'] == lu.get(10, ef_set_type='duff_rsc')
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc']['PM2.5'] == lu.get(10, ef_set_type='duff_rsc', species='PM2.5')
        assert self.EXPECTED_FCCS_71_CT_232 == lu.get(71)
        assert self.EXPECTED_FCCS_71_CT_232['duff_rsc'] == lu.get(71, ef_set_type='duff_rsc')

class TestCoverTypeLookup(LookUpTestBase):
    LOOKUP_CLASS = CoverTypeLookup

    def test_load_and_getitem(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS)

        # cases where FCCS id doesn't exist
        self.raises_key_error(lambda: lu[999])
        self.raises_key_error(lambda: lu[999]['duff_rsc'])
        self.raises_key_error(lambda: lu[999]['duff_rsc']['CO2'])
        # cases where ef group type doesn't exist
        self.raises_key_error(lambda: lu[130]['duffsdf'])
        self.raises_key_error(lambda: lu[130]['duffsdf']['CO2'])
        # cases where chemical species doesn't exist
        self.raises_key_error(lambda: lu[130]['duff_rsc']['sdfsdf'])
        # cases where ef set type isn't defined
        self.raises_key_error(lambda: lu[232]['flame_smold_wf'])
        self.raises_key_error(lambda: lu[232]['flame_smold_wf']['CO2'])
        # cases where species isn't defined
        assert None == lu[130]['woody_rsc']['CO2']

        assert self.EXPECTED_FCCS_10_CT_130 == lu[130]
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc'] == lu[130]['duff_rsc']
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc']['PM2.5'] == lu[130]['duff_rsc']['PM2.5']
        assert self.EXPECTED_FCCS_71_CT_232 == lu[232]
        assert self.EXPECTED_FCCS_71_CT_232['duff_rsc'] == lu[232]['duff_rsc']


    def test_load_and_get(self, tmpdir):
        lu = self.create_look_up_object(tmpdir, self.LOOKUP_CLASS)
        # cases where FCCS id doesn't exist
        assert None == lu.get(999)
        assert None == lu.get(999, ef_set_type='duff_rsc')
        assert None == lu.get(999, ef_set_type='duff_rsc', species='CO2')
        # cases where ef group type doesn't exist
        assert None == lu.get(130, ef_set_type='duffsdf')
        assert None == lu.get(130, ef_set_type='duffsdf', species='CO2')
        # cases where chemical species doesn't exist
        assert None == lu.get(130, ef_set_type='duff_rsc', species='sdfsdf')
        # cases where ef set type isn't defined
        assert None == lu.get(232, ef_set_type='flame_smold_wf')
        assert None == lu.get(232, ef_set_type='flame_smold_wf', species='CO2')
        # cases where species isn't defined
        assert None == lu.get(130, ef_set_type='woody_rsc', species='CO2')

        assert self.EXPECTED_FCCS_10_CT_130 == lu.get(130)
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc'] == lu.get(130, ef_set_type='duff_rsc')
        assert self.EXPECTED_FCCS_10_CT_130['duff_rsc']['PM2.5'] == lu.get(130, ef_set_type='duff_rsc', species='PM2.5')
        assert self.EXPECTED_FCCS_71_CT_232 == lu.get(232)
        assert self.EXPECTED_FCCS_71_CT_232['duff_rsc'] == lu.get(232, ef_set_type='duff_rsc')
