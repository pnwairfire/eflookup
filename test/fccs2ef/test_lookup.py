"""test_lookup.py:  Functional tests for code that loads FCCS fuelbed type to
urbanski group mappings and urbansku group emission factors, and returns data
structure for looking up EFs by FCCS.
"""

from fccs2ef.importer import Fccs2UrbanskiImporter, UrbanskiEfImporter

class TestLookUp:

    FCCS2URBANSKI_DATA="""fccs_id,urbanski_flame_smold_wf,urbanski_residual,urbanski_duff,urbanski_flame_smold_rx
1,9,3,10,5
4,9,3,10,5
69,7,3,10,7
70,9,3,10,5
71,,,,
83,,,,
85,1,3,2,1
88,1,3,2,1
90,6,3,10,6
"""
    URBANSKIEF_DATA="""Pollutant,Formula,6,1,9,8,5,7,4,3,10,2Carbon Dioxide,CO2,1703,1641,1600,1653,1598,1674,1705,1408,1305,1436
PM10,PM10,14.8,25.4,27.4,17.0,20.7,8.3,10.0,38.9,59.0,24.3
Total non-methane volatile organic compounds,NMOC,16.040,23.150,33.870,18.670,26.980,17.500,17.500,45.243,68.865,54.526
Hydrogen Cyanide ,HCN,0.613,0.890,0.540,,,0.749,0.749,0.723,1.519,2.457
C11 Aromatics ,C11,0.084,0.117,0.184,,,0.055,0.055,0.274,0.228,0.228
1-Undecene ,C11H22,0.014,0.019,0.030,,,0.014,0.014,0.045,0.036,0.036
n-Undecane ,C11H24,0.016,0.022,0.034,,,0.019,0.019,0.05,0.043,0.043
"""

    def test_load_and_lookup(self, tmpdir):
        pass
