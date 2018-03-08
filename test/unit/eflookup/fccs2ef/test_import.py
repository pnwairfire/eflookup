"""test_import.py:  Functional tests for code that imports raw data from
scientists and writes data files formatted to be included in the package
distributions
"""

import re

__author__      = "Joel Dubowy"

from eflookup.fccs2ef.importer import (
    Fccs2CoverTypeImporter, CoverType2EfGroupImporter,
    EfGroup2EfImporter, CatPhase2EFGroupImporter
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
    importer_class(input_filename).write(output_file_name=output_filename)
    assert len(tmpdir.listdir()) == 2
    # TODO: assert that output_filename exists
    output_content = open(output_filename, 'r').read()
    var_name = re.compile('([^=]+)=').search(output_content).group(1).strip()
    exec(output_content)
    output = locals()[var_name]
    assert expected_output == output


class TestFccs2CoverTypeImporter(object):
    """Top level functional test for importing fccs id to cover type mappings
    """

    INPUT_CONTENT = """fccs_id,cover_type_id,,,
0,404,,,
1,13,,,
2,131,,,
3,136,,,
4,118,,,
"""
    EXPECTED_OUTPUT = {
        "0":"404",
        "1":"13",
        "2":"131",
        "3":"136",
        "4":"118"
    }

    def test_import(self, tmpdir):
        run_test(tmpdir, self.INPUT_CONTENT, Fccs2CoverTypeImporter,
            self.EXPECTED_OUTPUT)


class TestCoverType2EfGroupImporter(object):
    """Top level functional test for importing cover type to ef group mappings
    """

    INPUT_CONTENT = """MapID,Cover type,WF,Rx,RegionalRx
1,SRM 101: Bluebunch Wheatgrass,6: Grass,6: Grass,24-26: W Grass
2,SRM 102: Idaho Fescue,6: Grass,6: Grass,24-26: W Grass
3,SRM 103: Green Fescue,6: Grass,6: Grass,24-26: W Grass
4,SRM 104: Antelope Bitterbrush-Bluebunch Wheatgrass,6: Grass,6: Grass,24-26: W Grass
5,SRM 105: Antelope Bitterbrush-Idaho Fescue,6: Grass,6: Grass,24-26: W Grass
6,SRM 106: Bluegrass Scabland,6: Grass,6: Grass,24-26: W Grass
7,SRM 107: Western Juniper-Big Sagebrush-Bluebunch Wheatgrass,5: Shrub,5: Shrub,30-32: W Shrub
"""

    # Note: the output is ordered by FCCS Id
    EXPECTED_OUTPUT = {
        "1": {"wf": "6", "rx": "6", "regrx": "24-26"},
        "2": {"wf": "6", "rx": "6", "regrx": "24-26"},
        "3": {"wf": "6", "rx": "6", "regrx": "24-26"},
        "4": {"wf": "6", "rx": "6", "regrx": "24-26"},
        "5": {"wf": "6", "rx": "6", "regrx": "24-26"},
        "6": {"wf": "6", "rx": "6", "regrx": "24-26"},
        "7": {"wf": "5", "rx": "5", "regrx": "30-32"}
    }

    def test_import(self, tmpdir):
        run_test(tmpdir, self.INPUT_CONTENT, CoverType2EfGroupImporter,
            self.EXPECTED_OUTPUT)


class TestCatPhase2EFGroupImporter(object):
    """Top level functional test for importing
    """

    INPUT_CONTENT = """,,,,Note: This mapping should be used along with EF Group by FB to assign EFs.,,,,"CO2, CH4","CO, NOx, NH3, SO2, PM25","CO2, CO, CH4","NOx, NH3, SO2, PM25","CO2, CO, CH4, NH3, PM2.5","NOx, SO2","CO2, CO, CH4","NOx, NH3, SO2, PM25","CO2, CO, CH4, PM2.5","NOx, NH3, SO2","CO2, CO, CH4","NOx, NH3, SO2, PM25","CO2, CO, CH4, PM25","NOx, NH3, SO2","CO2, CO, CH4, NH3, PM25","NOx, SO2","CO2, CO, CH4, NH3, PM25","NOx, SO2","CO2, CO, CH4",,"Most of the time, the emissions module will use these rules (but see exceptions)",,,These are just for reference purposes.,,,,,,,,,,EF Group,CO2,CO,CH4,NOx,NH3,SO2,PM2.5,
"Duff = Ground fuels: upper duff, lower duff, basal accumulations (BA), squirrel middens (SM)",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
"CWD = Class 2 and 3 snags, coarse wood under woody",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
Follow this table for where residual emissions are expected (only N/A are not),,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
,,,Duff/CWD,Consume output variable,Category,CombustionPhase,Generic Assignment,9-11: SE Grass,9-11: SE Grass,12-14: SE Hdwd,12-14: SE Hdwd,15-17: SE Pine,15-17: SE Pine,18-20: SE Shrub,18-20: SE Shrub,21-23: W MC,21-23: W MC,24-26: W Grass,24-26: W Grass,27-29: W Hdwd,27-29: W Hdwd,30-32: W Shrub,30-32: W Shrub,30-32: W Shrub,30-32: W Shrub,33-35: Boreal,,Simplified Rules,EF Group,,Group #,# Cover Type,Note,,,,,,,SE grass F/S,9,1700,70.2,2.67,3.26,1.2,0.97,12.08,
C_over_crown,canopy,overstory,,C_over_crown_F,Overstory tree crowns,Flaming,General (1-6),10,9,13,12,16,15,19,18,22,21,25,24,28,27,31,30,31,30,33,,All outputs except for below:,Flaming/Short-term smoldering EF Groups 1-6,,1,Southeastern Forest,Assigned by fuelbed,,,,,,,SE Grass F,10,1710,,2.42,,,,,
,,,,C_over_crown_S,Overstory tree crowns,Smoldering,General (1-6),11,9,14,12,17,15,20,18,23,21,26,24,29,27,32,30,32,30,34,,,,,2,Boreal Forest,Assigned by fuelbed,,,,,,,SE Grass S,11,1538,,5.4,,,,,
,,,,C_over_crown_R,Overstory tree crowns,Residual,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,N/A,,C_wood_S1000hr_R,Woody RSC (7),,3,Western Forest - Rx,Assigned by fuelbed and burn type (prescribed or wildfire),,,,,,,SE Hdwd F/S,12,1688,78.9,2.42,2.43,1.79,0.63,14.32,
C_mid_crown,canopy,midstory,,C_mid_crown_F,Midstory tree crowns,Flaming,General (1-6),10,9,13,12,16,15,19,18,22,21,25,24,28,27,31,30,31,30,33,,C_wood_R1000hr_R,Woody RSC (7),,4,Western Forest - WF,Assigned by fuelbed and burn type (prescribed or wildfire),,,,,,,SE Hdwd F,13,1702,68.6,1.92,,,,,
,,,CWD,C_snagc3_R,Class 3 snag wood,Residual,Woody RSC (7),7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,,"SE Hdwd (F, S)","CO2, CO, CH4",,Shrub,,,,,,,,,,,,,,,,,,
"""

    EXPECTED_OUTPUT = {
        '9-11': {
            'canopy': {
                'overstory': {
                    'smoldering': {'CO': '9', 'NH3': '9', 'NOx': '9', 'PM25': '9', 'SO2': '9'},
                    'flaming': {'CO': '9', 'NH3': '9', 'NOx': '9', 'PM25': '9', 'SO2': '9'},
                    'residual': {'CO': None, 'NH3': None, 'NOx': None, 'PM25': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'CO': '9', 'NH3': '9', 'NOx': '9', 'PM25': '9', 'SO2': '9'}
                },
                'snags class 3': {
                    'residual': {'CO': '7', 'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'CO': '7', 'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            }
        },
        '12-14': {
            'canopy': {
                'overstory': {
                    'smoldering': {'NH3': '12', 'NOx': '12', 'PM25': '12', 'SO2': '12'},
                    'flaming': {'NH3': '12', 'NOx': '12', 'PM25': '12', 'SO2': '12'},
                    'residual': {'NH3': None, 'NOx': None, 'PM25': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'NH3': '12', 'NOx': '12', 'PM25': '12', 'SO2': '12'}
                },
                'snags class 3': {
                    'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            }
        },
        '15-17': {
            'canopy': {
                'overstory': {
                    'smoldering': {'NOx': '15', 'SO2': '15'},
                    'flaming': {'NOx': '15', 'SO2': '15'},
                    'residual': {'NOx': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'NOx': '15', 'SO2': '15'}
                },
                'snags class 3': {
                    'residual': {'NOx': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'NOx': '7', 'SO2': '7'}
                }
            }
        },
        '18-20': {
            'canopy': {
                'overstory': {
                    'smoldering': {'NH3': '18', 'NOx': '18', 'PM25': '18', 'SO2': '18'},
                    'flaming': {'NH3': '18', 'NOx': '18', 'PM25': '18', 'SO2': '18'},
                    'residual': {'NH3': None, 'NOx': None, 'PM25': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'NH3': '18', 'NOx': '18', 'PM25': '18', 'SO2': '18'}
                },
                'snags class 3': {
                    'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            }
        },
        '21-23': {
            'canopy': {
                'overstory': {
                    'smoldering': {'NH3': '21', 'NOx': '21', 'SO2': '21'},
                    'flaming': {'NH3': '21', 'NOx': '21', 'SO2': '21'},
                    'residual': {'NH3': None, 'NOx': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'NH3': '21', 'NOx': '21', 'SO2': '21'}
                },
                'snags class 3': {
                    'residual': {'NH3': '7', 'NOx': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'NH3': '7', 'NOx': '7', 'SO2': '7'}
                }
            }
        },
        '24-26': {
            'canopy': {
                'overstory': {
                    'smoldering': {'NH3': '24', 'NOx': '24', 'PM25': '24', 'SO2': '24'},
                    'flaming': {'NH3': '24', 'NOx': '24', 'PM25': '24', 'SO2': '24'},
                    'residual': {'NH3': None, 'NOx': None, 'PM25': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'NH3': '24', 'NOx': '24', 'PM25': '24', 'SO2': '24'}
                },
                'snags class 3': {
                    'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
                }
            }
        },
        '27-29': {
            'canopy': {
                'overstory': {
                    'smoldering': {'NH3': '27', 'NOx': '27', 'SO2': '27'},
                    'flaming': {'NH3': '27', 'NOx': '27', 'SO2': '27'},
                    'residual': {'NH3': None, 'NOx': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'NH3': '27', 'NOx': '27', 'SO2': '27'}
                },
                'snags class 3': {
                    'residual': {'NH3': '7', 'NOx': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'NH3': '7', 'NOx': '7', 'SO2': '7'}
                }
            }
        },
        '30-32': {
            'canopy': {
                'overstory': {
                    'smoldering': {'NOx': '30', 'SO2': '30'},
                    'flaming': {'NOx': '30', 'SO2': '30'},
                    'residual': {'NOx': None, 'SO2': None},
                },
                'midstory': {
                    'flaming': {'NOx': '30', 'SO2': '30'}
                },
                'snags class 3': {
                    'residual': {'NOx': '7', 'SO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'NOx': '7', 'SO2': '7'}
                }
            }
        },
        '33-35': {
            'canopy': {
                'overstory': {
                    'smoldering': {'CO': '34', 'CH4': '34', 'CO2': '34'},
                    'flaming': {'CO': '33', 'CH4': '33', 'CO2': '33'},
                    'residual': {'CO': None, 'CH4': None, 'CO2': None},
                },
                'midstory': {
                    'flaming': {'CO': '33', 'CH4': '33', 'CO2': '33'}
                },
                'snags class 3': {
                    'residual': {'CO': '7', 'CH4': '7', 'CO2': '7'}
                }
            },
            'nonwoody': {
                'primary live': {
                    'residual': {'CO': '7', 'CH4': '7', 'CO2': '7'}
                }
            }
        }
    }

    def test_import(self, tmpdir):
        run_test(tmpdir, self.INPUT_CONTENT, CatPhase2EFGroupImporter,
            self.EXPECTED_OUTPUT)

class TestEfGroup2EfImporter(object):
    """Top level functional test for importing ef group to emission factors mappings.
    """

    INPUT_CONTENT = """g/kg,,Urbanski + Liu (1-8),,,,,,,,Revised (9-32),,,,,,,,,,,,,,,,,,,,,,,,,,
,,SE pine,Boreal,Rx NW Conifer,WF NW Conifer,W Shrub,Grass,Residual CWD,Residual Duff,SE grass F/S,SE Grass F,SE Grass S,SE Hdwd F/S,SE Hdwd F,SE Hdwd S,SE Pine F/S,SE Pine F,SE Pine S,SE Shrub F/S,SE Shrub F,SE Shrub S,W MC F/S,W MC F,W MC S,W Grass F/S,W Grass F,W Grass S,W Hdwd F/S,W Hdwd F,W Hdwd S,W Shrub F/S,W Shrub F,W Shrub S,Boreal F/S,Boreal F,Boreal S
Pollutant,Formula,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35
Carbon Dioxide,CO2,1703,1641,1598,1454,1674,1705,1408,1371,1700,1710,1538,1688,1702,1580,1606,1677,1530,1703,1743,1461,1603.16,1665.93,1592.10,1531,1638,1102,1577,1711,1489,1570,1696,1549,1606,1690,1570
Carbon Monoxide,CO,76,95,105,89.3,74,61,229,257,70.2,,,78.9,68.6,129.5,94.6,72.4,156.2,74.3,72.4,93.8,108.47,83.61,139.83,55.8,45,115.3,109.3,55.3,150.6,107.2,66.4,101.6,117,73,154
Methane,CH4,2.32,3.38,4.86,4.9,3.69,1.95,13.94,7.945,2.67,2.42,5.4,2.42,1.92,5.9,3.74,2.38,8.72,2.44,2.24,3.3,5.63,3.88,7.58,1.98,1.67,4.2,5.79,1.89,6.85,2.51,2.02,4.44,5.25,2.19,7.9
Nitrogen Oxides,NOx,1.7,1,2.06,0.49,2.18,2.18,0,0.67,3.26,,,2.43,,,1.96,,,4.23,,,3.22,,,3.26,,,3.25,,,3.57,,,2.33,,
Ammonia,NH3,0.14,0.79,1.53,1.5,1.5,1.5,0.48,2.67,1.2,,,1.79,,,0.7,0.48,1.15,2.21,,,1.07,,,0.3,,,0.58,,,1.48,1.45,2.12,2.07,,
Sulfur Dioxide,SO2,1.06,1.06,1.06,0.32,0.68,0.68,0,1.76,0.97,,,0.63,,,0.79,,,0.87,,,0.88,,,0.97,,,0.52,,,0.53,,,0.15,,
PM2.5,PM2.5,12.58,21.5,17.57,26,7.06,8.51,33,35.3,12.08,,,14.32,,,29.43,17.56,49.72,12.03,,,15.30,13.73,25.38,9.89,,,10.77,6.36,11.54,7.99,6.97,9.39,21.5,,
"""

    EXPECTED_OUTPUT = """Pollutant,Formula,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35
Carbon Dioxide,CO2,1703,1641,1598,1454,1674,1705,1408,1371,1700,1710,1538,1688,1702,1580,1606,1677,1530,1703,1743,1461,1603.16,1665.93,1592.10,1531,1638,1102,1577,1711,1489,1570,1696,1549,1606,1690,1570
Carbon Monoxide,CO,76,95,105,89.3,74,61,229,257,70.2,,,78.9,68.6,129.5,94.6,72.4,156.2,74.3,72.4,93.8,108.47,83.61,139.83,55.8,45,115.3,109.3,55.3,150.6,107.2,66.4,101.6,117,73,154
Methane,CH4,2.32,3.38,4.86,4.9,3.69,1.95,13.94,7.945,2.67,2.42,5.4,2.42,1.92,5.9,3.74,2.38,8.72,2.44,2.24,3.3,5.63,3.88,7.58,1.98,1.67,4.2,5.79,1.89,6.85,2.51,2.02,4.44,5.25,2.19,7.9
Nitrogen Oxides,NOx,1.7,1,2.06,0.49,2.18,2.18,0,0.67,3.26,,,2.43,,,1.96,,,4.23,,,3.22,,,3.26,,,3.25,,,3.57,,,2.33,,
Ammonia,NH3,0.14,0.79,1.53,1.5,1.5,1.5,0.48,2.67,1.2,,,1.79,,,0.7,0.48,1.15,2.21,,,1.07,,,0.3,,,0.58,,,1.48,1.45,2.12,2.07,,
Sulfur Dioxide,SO2,1.06,1.06,1.06,0.32,0.68,0.68,0,1.76,0.97,,,0.63,,,0.79,,,0.87,,,0.88,,,0.97,,,0.52,,,0.53,,,0.15,,
PM2.5,PM2.5,12.58,21.5,17.57,26,7.06,8.51,33,35.3,12.08,,,14.32,,,29.43,17.56,49.72,12.03,,,15.30,13.73,25.38,9.89,,,10.77,6.36,11.54,7.99,6.97,9.39,21.5,,
"""

    def test_import(self, tmpdir):
        run_test(tmpdir, self.INPUT_CONTENT, EfGroup2EfImporter,
            self.EXPECTED_OUTPUT)

