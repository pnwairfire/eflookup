"""test_import.py:  Functional tests for code that imports raw data from
scientists and writes data files formatted to be included in the package
distributions
"""

from eflookup.fccs2ef.importer import (
    Fccs2CoverTypeImporter, CoverType2EfGroupImporter, EfGroup2EfImporter
)

# TODO: put this in base class, add base class 'test_import' method, remove
# each class' test_import method, and add IMPORTER_CLASS class variable to
# each child class.  This will only work if we can somehow tell py.test
# not to run test_import if the current class is the base class
def run_test(tmpdir, input_content, importer_class, expected_output):
    input_file = tmpdir.join("input.csv")
    input_file.write(input_content)
    input_filename = str(input_file)
    output_filename = input_filename.replace('input', 'output')
    importer_class(input_filename).write(output_filename)
    assert len(tmpdir.listdir()) == 2
    # TODO: assert that output_filename exists
    assert expected_output == open(output_filename, 'r').read()


class TestFccs2CoverTypeImporter:
    """Top level functional test for importing fccs id to cover type mappings
    """

    INPUT_CONTENT = """GeneratorName=FCCS 3.0,GeneratorVersion=3.0.0,DateCreated=11/14/2014
fuelbed_number,filename,cover_type,ecoregion,overstory_loading,midstory_loading,understory_loading,snags_c1_foliage_loading,snags_c1wo_foliage_loading,snags_c1_wood_loading,snags_c2_loading,snags_c3_loading,shrubs_primary_loading,shrubs_secondary_loading,shrubs_primary_perc_live,shrubs_secondary_perc_live,nw_primary_loading,nw_secondary_loading,nw_primary_perc_live,nw_secondary_perc_live,w_sound_0_quarter_loading,w_sound_quarter_1_loading,w_sound_1_3_loading,w_sound_3_9_loading,w_sound_9_20_loading,w_sound_gt20_loading,w_rotten_3_9_loading,w_rotten_9_20_loading,w_rotten_gt20_loading,w_stump_sound_loading,w_stump_rotten_loading,w_stump_lightered_loading,litter_depth,litter_loading,lichen_depth,lichen_loading,moss_depth,moss_loading,basal_accum_loading,squirrel_midden_loading,ladderfuels_loading,duff_lower_depth,duff_lower_loading,duff_upper_depth,duff_upper_loading,pile_clean_loading,pile_dirty_loading,pile_vdirty_loading,Total_available_fuel_loading,efg_natural,efg_activity
0,FB_0000_FCCS.xml,0,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,8,8
1,FB_0001_FCCS.xml,13,240.000000,19.441261,8.724524,0.513638,0.000000,1.304389,0.000000,0.250149,1.176212,2.695305,0.000000,95.000000,0.000000,0.200000,0.000000,90.000000,0.000000,0.200000,0.800000,3.500000,0.500000,0.500000,0.000000,3.000000,4.000000,5.000000,0.000000,0.029405,0.000000,0.500000,1.304750,0.100000,0.002500,0.500000,0.300000,0.000000,0.000000,0.000000,1.500000,33.000000,0.500000,4.000000,0.000000,0.000000,0.000000,60.458324,9,9
2,FB_0002_FCCS.xml,131,240.000000,13.562624,7.043651,0.355776,0.069598,0.000000,23.021986,12.864821,6.432411,1.869412,1.895328,90.000000,90.000000,0.150000,0.010000,85.000000,60.000000,1.000000,2.000000,4.000000,2.000000,3.000000,6.000000,1.000000,3.000000,4.000000,0.000000,0.091891,0.000000,0.500000,1.455970,0.100000,0.001500,0.500000,0.112500,0.000000,0.000000,0.500000,2.500000,42.750004,0.500000,3.000000,0.000000,0.000000,0.000000,98.703438,8,1
4,FB_0004_FCCS.xml,118,240.000000,3.503858,0.000000,0.249043,0.004194,0.000000,0.274071,0.000000,0.000000,5.400000,0.510363,70.000000,90.000000,0.500000,0.100000,90.000000,90.000000,0.200000,0.300000,3.800000,0.000000,0.000000,0.000000,12.000001,7.000000,4.500000,0.000000,13.232283,0.000000,0.750000,2.268750,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,0.000000,1.000000,9.000000,0.500000,2.000000,0.163028,0.000000,0.000000,60.978615,8,1
3,FB_0003_FCCS.xml,136,240.000000,8.566302,0.000000,0.585708,0.000000,0.000000,0.000000,2.297290,2.297290,1.419839,0.000000,85.000000,0.000000,0.300000,0.010000,90.000000,50.000000,2.500000,3.500000,3.600000,10.700001,0.000000,0.000000,2.500000,0.000000,0.000000,0.000000,6.616141,0.000000,0.750000,2.148187,0.000000,0.000000,0.500000,0.007500,0.000000,0.000000,0.500000,1.800000,30.779999,0.750000,5.940000,0.000000,1.775982,0.000000,76.892227,8,1
"""
    EXPECTED_OUTPUT = """fccs_id,cover_type_id
0,0
1,13
2,131
3,136
4,118
"""

    def test_import(self, tmpdir):
        run_test(tmpdir, self.INPUT_CONTENT, Fccs2CoverTypeImporter,
            self.EXPECTED_OUTPUT)


class TestCoverType2EfGroupImporter:
    """Top level functional test for importing cover type to ef group mappings
    """

    INPUT_CONTENT = """MapID,Cover type,WF EF Assignment,RxBurn EF Assignment
1,SRM 101: Bluebunch Wheatgrass,6: Grassland,6: Grassland
2,SRM 102: Idaho Fescue,6: Grassland,6: Grassland
3,SRM 103: Green Fescue,6: Grassland,6: Grassland
4,SRM 104: Antelope Bitterbrush-Bluebunch Wheatgrass,6: Grassland,6: Grassland
5,SRM 105: Antelope Bitterbrush-Idaho Fescue,6: Grassland,6: Grassland
6,SRM 106: Bluegrass Scabland,6: Grassland,6: Grassland
7,SRM 107: Western Juniper-Big Sagebrush-Bluebunch Wheatgrass,5: Shrubland,5: Shrubland
"""

    # Note: the output is ordered by FCCS Id
    EXPECTED_OUTPUT = """cover_type_id,wf,rx
1,6,6
2,6,6
3,6,6
4,6,6
5,6,6
6,6,6
7,5,5
"""

    def test_import(self, tmpdir):
        run_test(tmpdir, self.INPUT_CONTENT, CoverType2EfGroupImporter,
            self.EXPECTED_OUTPUT)


class TestEfGroup2EfImporter:
    """Top level functional test for importing ef group to emission factors mappings.
    """

    INPUT_CONTENT = """Units = lb/ton,,Group 1,Group 2,Group 3,Group 4,Group 5,Group 6,Group 7,Group 8
Pollutant,Formula,Southeastern Forest,Boreal Forest,Western Forest - Rx,Western Forest - WF,Shrubland,Grassland,Woody RSC,Duff RSC
Carbon Dioxide,CO2,3406.0000,3282.0000,3196.0000,3200.0000,3348.0000,3410.0000,2816.0000,2742.0000
Carbon Monoxide,CO,152.0000,190.0000,210.0000,270.0000,148.0000,122.0000,458.0000,514.0000
Methane,CH4,4.6400,6.7600,9.7200,14.6400,7.3800,3.9000,27.8800,15.8900
Nitrogen Oxides,NOx,3.4000,2.0000,4.1200,4.0000,4.3600,4.3600,0.0000,1.3400
Ammonia,NH3,0.2800,1.5800,3.0600,3.0000,3.0000,3.0000,0.9600,5.3400
Sulfur Dioxide  ,SO2,2.1200, 2.1200,2.1200,2.1200,1.3600,1.3600,0.0000,3.5200
PM2.5 ,PM2.5 ,25.1600,43.0000 , 35.1400,46.4000,14.1200,17.0200,66.0000,70.6000
PM10,PM10,29.6888,50.7400,41.4652,54.7520,16.6616,20.0836,77.8800,83.3080
Total non-methane VOCs, NMOC,32.0920,46.3040,53.9500,67.7480,34.9976,35.2902,90.3500,123.3910
Hydrogen Cyanide ,HCN,1.2260,1.7800, 1.5300 ,1.0800,1.4980,1.4980,1.4460,3.9760
Formaldehyde ,HCHO,3.3620,3.9500,4.4700,4.4960,2.6600,2.6600,4.2480,4.9530
Methanol ,CH3OH,1.9720,2.6100,5.0300,4.1220,2.7000,2.7000,7.0340,9.3550
Isocyanic Acid ,HNCO,0.1800,0.2520,0.2940,0.3960,0.1630,0.1630,0.5860,0.5420
FormicAcid ,HCOOH,0.2320,0.9400,0.3680,1.0100,0.1550,0.1550,0.0000,2.1890
"""

    EXPECTED_OUTPUT = """Pollutant,Formula,1,2,3,4,5,6,7,8
Carbon Dioxide,CO2,3406.0000,3282.0000,3196.0000,3200.0000,3348.0000,3410.0000,2816.0000,2742.0000
Carbon Monoxide,CO,152.0000,190.0000,210.0000,270.0000,148.0000,122.0000,458.0000,514.0000
Methane,CH4,4.6400,6.7600,9.7200,14.6400,7.3800,3.9000,27.8800,15.8900
Nitrogen Oxides,NOx,3.4000,2.0000,4.1200,4.0000,4.3600,4.3600,0.0000,1.3400
Ammonia,NH3,0.2800,1.5800,3.0600,3.0000,3.0000,3.0000,0.9600,5.3400
Sulfur Dioxide,SO2,2.1200,2.1200,2.1200,2.1200,1.3600,1.3600,0.0000,3.5200
PM2.5,PM2.5,25.1600,43.0000,35.1400,46.4000,14.1200,17.0200,66.0000,70.6000
PM10,PM10,29.6888,50.7400,41.4652,54.7520,16.6616,20.0836,77.8800,83.3080
Total non-methane VOCs,NMOC,32.0920,46.3040,53.9500,67.7480,34.9976,35.2902,90.3500,123.3910
Hydrogen Cyanide,HCN,1.2260,1.7800,1.5300,1.0800,1.4980,1.4980,1.4460,3.9760
Formaldehyde,HCHO,3.3620,3.9500,4.4700,4.4960,2.6600,2.6600,4.2480,4.9530
Methanol,CH3OH,1.9720,2.6100,5.0300,4.1220,2.7000,2.7000,7.0340,9.3550
Isocyanic Acid,HNCO,0.1800,0.2520,0.2940,0.3960,0.1630,0.1630,0.5860,0.5420
FormicAcid,HCOOH,0.2320,0.9400,0.3680,1.0100,0.1550,0.1550,0.0000,2.1890
"""

    def test_import(self, tmpdir):
        run_test(tmpdir, self.INPUT_CONTENT, EfGroup2EfImporter,
            self.EXPECTED_OUTPUT)
