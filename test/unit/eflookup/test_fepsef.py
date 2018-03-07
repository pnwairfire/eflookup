"""test_lookup.py:  tests for looking up EFs by FCCS id or cover type.
"""

__author__      = "Joel Dubowy"

from py.test import raises

from eflookup.fepsef import FepsEFLookup, FEPS_EFS_NO_HAPS

WITH_HAPS = {
    'flaming': {
        'CH4': 0.003819999999999997,
        'CO': 0.07179999999999997,
        'CO2': 1.6497,
        'NH3': 0.0012063999999999998,
        'NOx': 0.002420000000000001,
        'PM10': 0.008590399999999998,
        'PM2.5': 0.007280000000000002,
        'SO2': 0.00098,
        'VOC': 0.017341999999999996,
        'hap_106990': 0.00020250000000000002,
        'hap_107028': 0.000212,
        'hap_108883': 0.00028412500000000004,
        'hap_110543': 8.20125e-06,
        'hap_120127': 2.5e-06,
        'hap_129000': 4.6449999999999996e-06,
        'hap_1330207': 0.000121,
        'hap_191242': 2.5400000000000002e-06,
        'hap_192972': 1.33e-06,
        'hap_193395': 1.705e-06,
        'hap_195197': 1.95e-06,
        'hap_198550': 4.28e-07,
        'hap_203338': 1.2999999999999998e-06,
        'hap_206440': 3.365e-06,
        'hap_207089': 1.2999999999999998e-06,
        'hap_218019': 3.1e-06,
        'hap_2381217': 4.525000000000001e-06,
        'hap_247': 1.48e-06,
        'hap_248': 3.95e-06,
        'hap_26714181': 4.1149999999999996e-06,
        'hap_463581': 2.67e-07,
        'hap_50000': 0.0012875,
        'hap_50328': 7.4e-07,
        'hap_56553': 3.1e-06,
        'hap_56832736': 2.57e-06,
        'hap_71432': 0.0005625,
        'hap_74873': 6.41625e-05,
        'hap_75070': 0.000204125,
        'hap_85018': 2.5e-06
    },
    'residual': {
        'CH4': 0.009868000000000002,
        'CO': 0.21011999999999997,
        'CO2': 1.39308,
        'NH3': 0.00341056,
        'NOx': 0.000908,
        'PM10': 0.01962576,
        'PM2.5': 0.016632,
        'SO2': 0.00098,
        'VOC': 0.04902680000000001,
        'hap_106990': 0.00020250000000000002,
        'hap_107028': 0.000212,
        'hap_108883': 0.00028412500000000004,
        'hap_110543': 8.20125e-06,
        'hap_120127': 2.5e-06,
        'hap_129000': 4.6449999999999996e-06,
        'hap_1330207': 0.000121,
        'hap_191242': 2.5400000000000002e-06,
        'hap_192972': 1.33e-06,
        'hap_193395': 1.705e-06,
        'hap_195197': 1.95e-06,
        'hap_198550': 4.28e-07,
        'hap_203338': 1.2999999999999998e-06,
        'hap_206440': 3.365e-06,
        'hap_207089': 1.2999999999999998e-06,
        'hap_218019': 3.1e-06,
        'hap_2381217': 4.525000000000001e-06,
        'hap_247': 1.48e-06,
        'hap_248': 3.95e-06,
        'hap_26714181': 4.1149999999999996e-06,
        'hap_463581': 2.67e-07,
        'hap_50000': 0.0012875,
        'hap_50328': 7.4e-07,
        'hap_56553': 3.1e-06,
        'hap_56832736': 2.57e-06,
        'hap_71432': 0.0005625,
        'hap_74873': 6.41625e-05,
        'hap_75070': 0.000204125,
        'hap_85018': 2.5e-06
    },
    'smoldering': {
        'CH4': 0.009868000000000002,
        'CO': 0.21011999999999997,
        'CO2': 1.39308,
        'NH3': 0.00341056,
        'NOx': 0.000908,
        'PM10': 0.01962576,
        'PM2.5': 0.016632,
        'SO2': 0.00098,
        'VOC': 0.04902680000000001,
        'hap_106990': 0.00020250000000000002,
        'hap_107028': 0.000212,
        'hap_108883': 0.00028412500000000004,
        'hap_110543': 8.20125e-06,
        'hap_120127': 2.5e-06,
        'hap_129000': 4.6449999999999996e-06,
        'hap_1330207': 0.000121,
        'hap_191242': 2.5400000000000002e-06,
        'hap_192972': 1.33e-06,
        'hap_193395': 1.705e-06,
        'hap_195197': 1.95e-06,
        'hap_198550': 4.28e-07,
        'hap_203338': 1.2999999999999998e-06,
        'hap_206440': 3.365e-06,
        'hap_207089': 1.2999999999999998e-06,
        'hap_218019': 3.1e-06,
        'hap_2381217': 4.525000000000001e-06,
        'hap_247': 1.48e-06,
        'hap_248': 3.95e-06,
        'hap_26714181': 4.1149999999999996e-06,
        'hap_463581': 2.67e-07,
        'hap_50000': 0.0012875,
        'hap_50328': 7.4e-07,
        'hap_56553': 3.1e-06,
        'hap_56832736': 2.57e-06,
        'hap_71432': 0.0005625,
        'hap_74873': 6.41625e-05,
        'hap_75070': 0.000204125,
        'hap_85018': 2.5e-06
    }
}

WITHOUT_HAPS = {
'flaming': {
        'CH4': 0.003819999999999997,
        'CO': 0.07179999999999997,
        'CO2': 1.6497,
        'NH3': 0.0012063999999999998,
        'NOx': 0.002420000000000001,
        'PM10': 0.008590399999999998,
        'PM2.5': 0.007280000000000002,
        'SO2': 0.00098,
        'VOC': 0.017341999999999996
    },
    'residual': {
        'CH4': 0.009868000000000002,
        'CO': 0.21011999999999997,
        'CO2': 1.39308,
        'NH3': 0.00341056,
        'NOx': 0.000908,
        'PM10': 0.01962576,
        'PM2.5': 0.016632,
        'SO2': 0.00098,
        'VOC': 0.04902680000000001
    },
    'smoldering': {
        'CH4': 0.009868000000000002,
        'CO': 0.21011999999999997,
        'CO2': 1.39308,
        'NH3': 0.00341056,
        'NOx': 0.000908,
        'PM10': 0.01962576,
        'PM2.5': 0.016632,
        'SO2': 0.00098,
        'VOC': 0.04902680000000001
    }
}

class TestLookup:

    def test_without_haps(self):
        assert WITHOUT_HAPS == FepsEFLookup()
        assert WITHOUT_HAPS == FepsEFLookup(include_haps=False)

    def test_with_haps(self):
        assert WITH_HAPS == FepsEFLookup(include_haps=True)

    def test_get(self):
        lu = FepsEFLookup()

        # species is specified without phase
        with raises(LookupError):
            lu.get(species='CO2')

        assert None == lu.get(phase='dfdf')
        assert None == lu.get(phase='flaming', species='sdf')
        assert None == lu.get(phase='sdfsdf', species='CO')

        assert WITHOUT_HAPS == lu.get()
        assert WITHOUT_HAPS['flaming'] == lu.get(phase='flaming')
        assert WITHOUT_HAPS['flaming']['CO'] == lu.get(phase='flaming', species='CO')

    def test_getitem(self):
        lu = FepsEFLookup()

        with raises(KeyError):
            assert None == lu['dfdf']

        with raises(KeyError):
            assert None == lu['flaming']['sdf']

        with raises(KeyError):
            assert None == lu['sdfsdf']['CO']

        assert WITHOUT_HAPS['flaming'] == lu['flaming']
        assert WITHOUT_HAPS['flaming']['CO'] == lu['flaming']['CO']

    def test_modifying_efs_does_not_affect_module_copy(self):
        lu = FepsEFLookup()
        lu = {'dsf':123}
        assert FEPS_EFS_NO_HAPS == WITHOUT_HAPS

    def test_species(self):
        lu = FepsEFLookup()
        assert set(WITHOUT_HAPS['flaming'].keys()) == lu.species('flaming')
        assert set(WITHOUT_HAPS['smoldering'].keys()) == lu.species('smoldering')
        assert set(WITHOUT_HAPS['residual'].keys()) == lu.species('residual')
        lu = FepsEFLookup(include_haps=True)
        assert set(WITH_HAPS['flaming'].keys()) == lu.species('flaming')
        assert set(WITH_HAPS['smoldering'].keys()) == lu.species('smoldering')
        assert set(WITH_HAPS['residual'].keys()) == lu.species('residual')
