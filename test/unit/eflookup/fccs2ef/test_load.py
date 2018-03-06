__author__      = "Joel Dubowy"

from eflookup.fccs2ef.load import (
    Fccs2CoverTypeLoader, CoverType2EfGroupLoader,
    EfGroup2EfLoader, CatPhase2EFGroupLoader
)

# TODO: put this in base class, add base class 'test_load' method, remove
# each class' test_load method, and add LOADER_CLASS class variable to
# each child class.  This will only work if we can somehow tell py.test
# not to run test_load if the current class is the base class
def run_test(tmpdir, input_content, loader_class, expected_data):
    input_file = tmpdir.join("input.csv")
    input_file.write(input_content)
    input_filename = str(input_file)
    output_filename = input_filename.replace('input', 'output')
    loader = loader_class(file_name=input_filename)
    assert len(tmpdir.listdir()) == 1 # no additional file written
    assert expected_data == loader._data


class TestFccs2CoverTypeLoader(object):
    pass

class TestCoverType2EfGroupLoader(object):
    pass


class TestCatPhase2EFGroupLoader(object):
    """Top level functional test for importing
    """

    INPUT = """consume_output_variable,phase,generic_assignment,"9-11:CO2,CH4","9-11:CO,NOx,NH3,SO2,PM25","12-14:CO2,CO,CH4","12-14:NOx,NH3,SO2,PM25","15-17:CO2,CO,CH4,NH3,PM2.5","15-17:NOx,SO2","18-20:CO2,CO,CH4","18-20:NOx,NH3,SO2,PM25","21-23:CO2,CO,CH4,PM2.5","21-23:NOx,NH3,SO2","24-26:CO2,CO,CH4","24-26:NOx,NH3,SO2,PM25","27-29:CO2,CO,CH4,PM25","27-29:NOx,NH3,SO2","30-32:CO2,CO,CH4,NH3,PM25","30-32:NOx,SO2","30-32:CO2,CO,CH4,NH3,PM25","30-32:NOx,SO2","33-35:CO2,CO,CH4"
c_over_crown,flaming,1-6,10,9,13,12,16,15,19,18,22,21,25,24,28,27,31,30,31,30,33
c_over_crown,smoldering,1-6,11,9,14,12,17,15,20,18,23,21,26,24,29,27,32,30,32,30,34
c_over_crown,residual,,,,,,,,,,,,,,,,,,,,
c_mid_crown,flaming,1-6,10,9,13,12,16,15,19,18,22,21,25,24,28,27,31,30,31,30,33
c_snagc3,residual,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7
"""

    EXPECTED_DATA = {
        '9-11': {
            'c_over_crown': {
                'smoldering': {'CO': '9', 'NH3': '9', 'NOx': '9', 'PM25': '9', 'SO2': '9'},
                'flaming': {'CO': '9', 'NH3': '9', 'NOx': '9', 'PM25': '9', 'SO2': '9'}
            },
            'c_mid_crown': {
                'flaming': {'CO': '9', 'NH3': '9', 'NOx': '9', 'PM25': '9', 'SO2': '9'}
            },
            'c_snagc3': {
                'residual': {'CO': '7', 'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
            }
        },
        '12-14': {
            'c_over_crown': {
                'smoldering': {'NH3': '12', 'NOx': '12', 'PM25': '12', 'SO2': '12'},
                'flaming': {'NH3': '12', 'NOx': '12', 'PM25': '12', 'SO2': '12'}
            },
            'c_mid_crown': {
                'flaming': {'NH3': '12', 'NOx': '12', 'PM25': '12', 'SO2': '12'}
            },
            'c_snagc3': {
                'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
            }
        },
        '15-17': {
            'c_over_crown': {
                'smoldering': {'NOx': '15', 'SO2': '15'},
                'flaming': {'NOx': '15', 'SO2': '15'}
            },
            'c_mid_crown': {
                'flaming': {'NOx': '15', 'SO2': '15'}
            },
            'c_snagc3': {
                'residual': {'NOx': '7', 'SO2': '7'}
            }
        },
        '18-20': {
            'c_over_crown': {
                'smoldering': {'NH3': '18', 'NOx': '18', 'PM25': '18', 'SO2': '18'},
                'flaming': {'NH3': '18', 'NOx': '18', 'PM25': '18', 'SO2': '18'}
            },
            'c_mid_crown': {
                'flaming': {'NH3': '18', 'NOx': '18', 'PM25': '18', 'SO2': '18'}
            },
            'c_snagc3': {
                'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
            }
        },
        '21-23': {
            'c_over_crown': {
                'smoldering': {'NH3': '21', 'NOx': '21', 'SO2': '21'},
                'flaming': {'NH3': '21', 'NOx': '21', 'SO2': '21'}
            },
            'c_mid_crown': {
                'flaming': {'NH3': '21', 'NOx': '21', 'SO2': '21'}
            },
            'c_snagc3': {
                'residual': {'NH3': '7', 'NOx': '7', 'SO2': '7'}
            }
        },
        '24-26': {
            'c_over_crown': {
                'smoldering': {'NH3': '24', 'NOx': '24', 'PM25': '24', 'SO2': '24'},
                'flaming': {'NH3': '24', 'NOx': '24', 'PM25': '24', 'SO2': '24'}
            },
            'c_mid_crown': {
                'flaming': {'NH3': '24', 'NOx': '24', 'PM25': '24', 'SO2': '24'}
            },
            'c_snagc3': {
                'residual': {'NH3': '7', 'NOx': '7', 'PM25': '7', 'SO2': '7'}
            }
        },
        '27-29': {
            'c_over_crown': {
                'smoldering': {'NH3': '27', 'NOx': '27', 'SO2': '27'},
                'flaming': {'NH3': '27', 'NOx': '27', 'SO2': '27'}
            },
            'c_mid_crown': {
                'flaming': {'NH3': '27', 'NOx': '27', 'SO2': '27'}
            },
            'c_snagc3': {
                'residual': {'NH3': '7', 'NOx': '7', 'SO2': '7'}
            }
        },
        '30-32': {
            'c_over_crown': {
                'smoldering': {'NOx': '30', 'SO2': '30'},
                'flaming': {'NOx': '30', 'SO2': '30'}
            },
            'c_mid_crown': {
                'flaming': {'NOx': '30', 'SO2': '30'}
            },
            'c_snagc3': {
                'residual': {'NOx': '7', 'SO2': '7'}
            }
        },
        '33-35': {
            'c_over_crown': {
                'smoldering': {'CO': '34', 'CH4': '34', 'CO2': '34'},
                'flaming': {'CO': '33', 'CH4': '33', 'CO2': '33'}
            },
            'c_mid_crown': {
                'flaming': {'CO': '33', 'CH4': '33', 'CO2': '33'}
            },
            'c_snagc3': {
                'residual': {'CO': '7', 'CH4': '7', 'CO2': '7'}
            }
        }
    }

    def test_load(self, tmpdir):
        run_test(tmpdir, self.INPUT, CatPhase2EFGroupLoader,
            self.EXPECTED_DATA)


class TestEFGroup2EFLoader(object):
    pass
