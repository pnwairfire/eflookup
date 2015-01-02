"""test_import.py:  Functional tests for code that imports raw data from
scientists and writes data files formatted to be included in the package
distributions

@todo:
 - add base class to remove redundant code currently in each class'
   test_import method
"""

from fccs2ef.importer import Fccs2UrbanskiImporter, UrbanskiEfImporter

class TestFccs2UrbanskiImporter:
    """Top level functional test for importing FCCS-to-Urbanski group mappings
    """

    INPUT_CONTENT = """FCCS fuelbedID,FCCS fuelbed_name ,  site_description, SAF/SRM MapID ,SAF/SRM MapID,SAF/SRM MapID,SAF/SRM MapID,SAF/SRM MapID,SAF/SRM Description,Urbanski Flame/Smold WF,Urbanski Residual,Urbanski Duff,Urbanski Flame/Smold Rx (CHECK),FINN Cover Type (CHECK)
 57,Wheatgrass - Cheatgrass grassland,"Native bunchgrass communities once dominated the Great Basin. Overgrazing, agriculture and other disturbances have significantly altered these grasslands, which are now dominated by non-native grass species. Data from John Day Fossil Beds National Monument.",1,2,,,,SRM 101: Bluebunch Wheatgrass,Grass,CWD residual,Temperate residual,Grass,Savanna/Grassland
66 ,Bluebunch wheatgrass - Bluegrass grassland,Prairie grasslands occur throughout the Midwest.  This prairie is a mixed-grass prairie that is transitional between short and tall grass prairies in South Dakota.  Fire has occurred at intervals of less than 35 years.,1,173,182,223,,SRM 101: Bluebunch Wheatgrass,Grass,CWD residual, Temperate residual, Grass ,Savanna/Grassland
 240 ,Saw palmetto / Three-awned grass shrubland,Dry to mesic shrublands in Florida dominated by saw palmetto and mixed grasses typical of flatwoods.  Natural occurrences are maintained by periodic fire.  Unnatural occurrences of similar vegetation composition can develop following logging in pine and palmetto flatwoods.  Fire exclusion in natural occurrences leads to more dense saw palmetto and tree encroachment.,293,,,,,SRM 816: Cabbage Palm Hammocks,SE forest,CWD residual,Temperate residual,SE forest,Temperate Forest
98, Marsh Labrador tea - Lingonberry tundra shrubland,"Low ericaceous shrub tundra dominated by Labrador tea, lingonberry, and blueberry.  Found on uplands in interior, western and northern Alaska.  Comparable to Viereck's &quot;Vaccinium dwarf shrub tundra&quot; vegetation type.",310,311,,,,SRM 911: Lichen Tundra,Boreal residual,CWD residual,Boreal residual,Boreal residual,Boreal Forest
83,Molasses grass grassland, "This Hawaiian submontane grassland is dominated by the coarse non-native sod grass, molasses grass (Melinis minutiflora).  Molasses grass is found in dry and mesic environments from sea level to 4500 feet throughout the Hawaiian Islands." ,,,,,,,,,,,
"""

    # Note: the output is ordered by FCCS Id
    EXPECTED_OUTPUT = """fccs_id,urbanski_flame_smold_wf,urbanski_residual,urbanski_duff,urbanski_flame_smold_rx
57,4,3,10,4
66,4,3,10,4
83,,,,
98,2,3,2,2
240,6,3,10,6
"""

    def test_import(self, tmpdir):
        input_file = tmpdir.join("input.csv")
        input_file.write(self.INPUT_CONTENT)
        input_filename = str(input_file)
        output_filename = input_filename.replace('input', 'output')
        Fccs2UrbanskiImporter(input_filename).write(output_filename)

        assert len(tmpdir.listdir()) == 2
        # TODO: assert that output_filename exists
        assert open(output_filename, 'r').read() == self.EXPECTED_OUTPUT

class TestUrbanskiEfImporter:
    """Top level functional test for importing Urbanski emission factors.
    """

    INPUT_CONTENT = """Units = g/kg,,,,,,,,,,,
 Pollutant, Formula,SE Forest, Boreal Forest ,Western Forest (WF),SW Forest (Rx),NW Forest (Rx),Shrub,Grass,CWD Residual,Temperate Residual,Boreal Residual
Carbon Dioxide,CO2,1703,1641,1600,1653,1598,1674,1705,1408,1305,1436
Carbon Monoxide,CO,76,95,135,87,105,74,61,229,271,244
 Ammonia,NH3,0.14,0.79,1.50,0.50,1.53,1.50,1.50,0.48,2.67,2.67
PM10 ,PM10 ,14.8,25.4,27.4,17.0,20.7,8.3,10.0,38.9,59.0,24.3
Total non-methane volatile organic compounds,NMOC,16.040,23.150,33.870,18.670,26.980,17.500,17.500,45.243,68.865,54.526
Ethene , C2H4,1.090,1.310,1.825,,,1.010,1.010,1.398,1.683,1.246
1-Butenylbenzene ,C10H14,0.002,0.002,0.004,,,0.002,0.002,0.005,0.002,0.002
 Camphene , C10H16 ,0.008,0.024,0.038,,,0.009,0.009,0.361,0.081,0.081
iso-Limonene ,C10H16, 0.003 ,0.005,0.008,,,0.000,0.000,0.011,0.002,0.002
n-Decane ,C10H22,0.019,0.012,0.018,,,0.015,0.015,0.027,0.027,0.027
C11 Aromatics ,C11,   0.084,0.117,0.184,,,0.055,0.055,0.274,0.228,0.228
"1,2-Butadiene ",C4H6,0.001,0.002,0.003,,,0.003,0.003,0.004,0,0
"""

    EXPECTED_OUTPUT = """Pollutant,Formula,6,1,9,8,5,7,4,3,10,2
Carbon Dioxide,CO2,1703,1641,1600,1653,1598,1674,1705,1408,1305,1436
Carbon Monoxide,CO,76,95,135,87,105,74,61,229,271,244
Ammonia,NH3,0.14,0.79,1.50,0.50,1.53,1.50,1.50,0.48,2.67,2.67
PM10,PM10,14.8,25.4,27.4,17.0,20.7,8.3,10.0,38.9,59.0,24.3
Total non-methane volatile organic compounds,NMOC,16.040,23.150,33.870,18.670,26.980,17.500,17.500,45.243,68.865,54.526
Ethene,C2H4,1.090,1.310,1.825,,,1.010,1.010,1.398,1.683,1.246
1-Butenylbenzene,C10H14,0.002,0.002,0.004,,,0.002,0.002,0.005,0.002,0.002
Camphene,C10H16,0.008,0.024,0.038,,,0.009,0.009,0.361,0.081,0.081
iso-Limonene,C10H16,0.003,0.005,0.008,,,0.000,0.000,0.011,0.002,0.002
n-Decane,C10H22,0.019,0.012,0.018,,,0.015,0.015,0.027,0.027,0.027
C11 Aromatics,C11,0.084,0.117,0.184,,,0.055,0.055,0.274,0.228,0.228
"1,2-Butadiene",C4H6,0.001,0.002,0.003,,,0.003,0.003,0.004,0,0
"""

    def test_import(self, tmpdir):
        input_file = tmpdir.join("input.csv")
        input_file.write(self.INPUT_CONTENT)
        input_filename = str(input_file)
        output_filename = input_filename.replace('input', 'output')
        UrbanskiEfImporter(input_filename).write(output_filename)

        assert len(tmpdir.listdir()) == 2
        # TODO: assert that output_filename exists
        assert open(output_filename, 'r').read() == self.EXPECTED_OUTPUT
