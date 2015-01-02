"""test_lookup.py:  Functional tests for code that loads FCCS fuelbed type to
urbanski group mappings and urbansku group emission factors, and returns data
structure for looking up EFs by FCCS.
"""

from fccs2ef.lookup import LookUp
from py.test import raises

class TestLookUp:

    FCCS2URBANSKI_DATA="""fccs_id,urbanski_flame_smold_wf,urbanski_residual,urbanski_duff,urbanski_flame_smold_rx
1,9,3,10,5
4,9,3,10,5
70,9,3,10,5
71,,,,
83,,,,
85,1,3,2,1
90,6,3,10,6
"""
    URBANSKIEF_DATA="""Pollutant,Formula,6,1,9,8,5,7,4,3,10,2
Carbon Dioxide,CO2,1703,1641,1600,1653,1598,1674,1705,1408,1305,1436
PM10,PM10,14.8,25.4,27.4,17.0,20.7,8.3,10.0,38.9,59.0,24.3
Total non-methane volatile organic compounds,NMOC,16.040,23.150,33.870,18.670,26.980,17.500,17.500,45.243,68.865,54.526
Hydrogen Cyanide ,HCN,0.613,0.890,0.540,,,0.749,0.749,0.723,1.519,2.457
C11 Aromatics ,C11,0.084,0.117,0.184,,,0.055,0.055,0.274,0.228,0.228
1-Undecene ,C11H22,0.014,0.019,0.030,,,0.014,0.014,0.045,0.036,0.036
Methylbenzofuran ,"isomer 1,C9H8O",0.008,0.011,0.018,,,0.012,0.012,0.027,0.024,0.024
"""

    def test_load_and_lookup(self, tmpdir):
        f2u = tmpdir.join("f2u.csv")
        f2u.write(self.FCCS2URBANSKI_DATA)
        uef = tmpdir.join("uef.csv")
        uef.write(self.URBANSKIEF_DATA)

        lu = LookUp(fccs_2_urbanski_file=str(f2u), urbanski_efs_file=str(uef))

        def raises_key_error(l):
            with raises(KeyError):
                l()

        raises_key_error(lambda: lu[2])                     # FCCS fuelbed id doesn't exist
        assert None == lu.get(2)                            # FCCS fuelbed id doesn't exist
        raises_key_error(lambda: lu[2]['duff'])             # FCCS fuelbed id doesn't exist
        assert None == lu.get(2, 'duff')                    # FCCS fuelbed id doesn't exist
        raises_key_error(lambda: lu[2]['duff']['CO2'])      # FCCS fuelbed id doesn't exist
        assert None == lu.get(2, 'duff', 'CO2')             # FCCS fuelbed id doesn't exist
        raises_key_error(lambda: lu[4]['duffsdf'])          # EF set type doesn't exist
        assert None == lu.get(4, 'duffsdf')                 # EF set type doesn't exist
        raises_key_error(lambda: lu[4]['duff']['sdfsdf'])   # Chemical species doesn't exist
        assert None == lu.get(4, 'duff', 'sdfsdf')          # Chemical species doesn't exist
        raises_key_error(lambda: lu[71]['duff']['CO2'])     # Chemical species not defined for this FCCS fuelbed id
        assert None == lu.get(71, 'duff', 'CO2')            # Chemical species not defined for this FCCS fuelbed id

        expected = {
            'flame_smold_wf': {  # 9
                'CO2': 1600,
                'PM10': 27.4,
                'NMOC': 33.870,
                'HCN': 0.540,
                'C11': 0.184,
                'C11H22': 0.030,
                "isomer 1,C9H8O": 0.018
            },
            'residual': {  # 3
                'CO2': 1408,
                'PM10': 38.9,
                'NMOC': 45.243,
                'HCN': 0.723,
                'C11': 0.274,
                'C11H22': 0.045,
                "isomer 1,C9H8O": 0.027
            },
            'duff': {  # 10
                'CO2': 1305,
                'PM10': 59.0,
                'NMOC': 68.865,
                'HCN': 1.519,
                'C11': 0.228,
                'C11H22': 0.036,
                "isomer 1,C9H8O": 0.024
            },
            'flame_smold_rx': {  # 5
                'CO2': 1598,
                'PM10': 20.7,
                'NMOC': 26.980,
                'HCN': None,
                'C11': None,
                'C11H22': None,
                "isomer 1,C9H8O": None
            }
        }
        assert expected == lu[4]
        assert expected == lu.get(4)
        assert expected['duff'] == lu[4]['duff']
        assert expected['duff'] == lu.get(4, 'duff')

        expected = {
            'flame_smold_wf': {},
            'residual': {},
            'duff': {},
            'flame_smold_rx': {}
        }
        assert expected == lu[71]
        assert expected == lu.get(71)
        assert expected['duff'] == lu[71]['duff']
        assert expected['duff'] == lu.get(71, 'duff')
