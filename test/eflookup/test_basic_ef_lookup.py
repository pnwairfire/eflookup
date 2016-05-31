__author__      = "Joel Dubowy"

from py.test import raises

from eflookup.lookup import BasicEFLookup

EFS = {
    'flaming': {
        'CH4': 0.003819999999999997,
        'CO': 0.07179999999999997,
        'VOC': 0.017341999999999996
    },
    'residual': {
        'NOx': 0.000908,
        'PM10': 0.01962576,
    },
    'smoldering': {
        'NH3': 0.00341056,
    }
}
class TestBasicEFLookup:

    def test_instantiation(self):
        with raises(ValueError) as e:
            BasicEFLookup()
        with raises(ValueError) as e:
            BasicEFLookup({})
        with raises(ValueError) as e:
            BasicEFLookup({'sdf':1})
        with raises(ValueError) as e:
            # each phase must be a dict
            BasicEFLookup({'flaming':12, 'smoldering': 34, 'residual': 12})
        with raises(ValueError) as e:
            # each EF must be numeric
            BasicEFLookup({'flaming':{'df':'234'}, 'smoldering': {'df':3}, 'residual': {'df':34.9}})

        BasicEFLookup({'flaming':{}, 'smoldering': {}, 'residual': {}})
        BasicEFLookup({'flaming':{'d':34}, 'smoldering': {'df':3}, 'residual': {'df':34.9}})


    def test_get(self):
        lu = BasicEFLookup(EFS)

        # species is specified without phase
        with raises(LookupError):
            lu.get(species='CO2')

        assert None == lu.get(phase='dfdf')
        assert None == lu.get(phase='flaming', species='sdf')
        assert None == lu.get(phase='sdfsdf', species='CO')

        assert EFS == lu.get()
        assert EFS['flaming'] == lu.get(phase='flaming')
        assert EFS['flaming']['CO'] == lu.get(phase='flaming', species='CO')

    def test_getitem(self):
        lu = BasicEFLookup(EFS)

        with raises(KeyError):
            assert None == lu['dfdf']

        with raises(KeyError):
            assert None == lu['flaming']['sdf']

        with raises(KeyError):
            assert None == lu['sdfsdf']['CO']

        assert EFS == lu
        assert EFS['flaming'] == lu['flaming']
        assert EFS['flaming']['CO'] == lu['flaming']['CO']

    def test_species(self):
        lu = BasicEFLookup(EFS)
        assert set(EFS['flaming'].keys()) == lu.species('flaming')
        assert set(EFS['smoldering'].keys()) == lu.species('smoldering')
        assert set(EFS['residual'].keys()) == lu.species('residual')
