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

    INPUT_CONTENT = """FCCS fuelbedID,FCCS fuelbed_name,site_description,SAF/SRM MapID,SAF/SRM MapID,SAF/SRM MapID,SAF/SRM MapID,SAF/SRM MapID,SAF/SRM Description,Urbanski Flame/Smold WF,Urbanski Residual,Urbanski Duff,Urbanski Flame/Smold Rx (CHECK),FINN Cover Type (CHECK)
57,Wheatgrass - Cheatgrass grassland,"Native bunchgrass communities once dominated the Great Basin. Overgrazing, agriculture and other disturbances have significantly altered these grasslands, which are now dominated by non-native grass species. Data from John Day Fossil Beds National Monument.",1,2,,,,SRM 101: Bluebunch Wheatgrass,Grass,CWD residual,Temperate residual,Grass,Savanna/Grassland
66,Bluebunch wheatgrass - Bluegrass grassland,Prairie grasslands occur throughout the Midwest.  This prairie is a mixed-grass prairie that is transitional between short and tall grass prairies in South Dakota.  Fire has occurred at intervals of less than 35 years.,1,173,182,223,,SRM 101: Bluebunch Wheatgrass,Grass,CWD residual,Temperate residual,Grass,Savanna/Grassland
240,Saw palmetto / Three-awned grass shrubland,Dry to mesic shrublands in Florida dominated by saw palmetto and mixed grasses typical of flatwoods.  Natural occurrences are maintained by periodic fire.  Unnatural occurrences of similar vegetation composition can develop following logging in pine and palmetto flatwoods.  Fire exclusion in natural occurrences leads to more dense saw palmetto and tree encroachment.,293,,,,,SRM 816: Cabbage Palm Hammocks,SE forest,CWD residual,Temperate residual,SE forest,Temperate Forest
83,Molasses grass grassland,"This Hawaiian submontane grassland is dominated by the coarse non-native sod grass, molasses grass (Melinis minutiflora).  Molasses grass is found in dry and mesic environments from sea level to 4500 feet throughout the Hawaiian Islands.",,,,,,,,,,,
98,Marsh Labrador tea - Lingonberry tundra shrubland,"Low ericaceous shrub tundra dominated by Labrador tea, lingonberry, and blueberry.  Found on uplands in interior, western and northern Alaska.  Comparable to Viereck's &quot;Vaccinium dwarf shrub tundra&quot; vegetation type.",310,311,,,,SRM 911: Lichen Tundra,Boreal residual,CWD residual,Boreal residual,Boreal residual,Boreal Forest
"""

    EXPECTED_OUTPUT = """fccs_id,urbanski_flame_smold_wf,urbanski_residual,urbanski_duff,urbanski_flame_smold_rx
57,4,3,10,4
66,4,3,10,4
240,6,3,10,6
83,,,,
98,2,3,2,2
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

    INPUT_CONTENT = """
    """

    EXPECTED_OUTPUT = """
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
