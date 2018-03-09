"""eflookup.fepsef.lookup: provides class for looking up FEPS emissions factors

The emissions factors contained in FEPS_EFS are static. To generate them,
we first started with constants POLLUTANT_NAMES, CLEAN_EMI_FACTOR,
EMI_EFFIC_FACTOR, PHASE, and COMBUSTION_EFFIC, which were copied directly
(translated into python) from the FEPS emissions C module in BSF:

    POLLUTANT_NAMES = [
        "CO2", "CO", "CH4", "PM2.5", "PM10", "NOx", "SO2", "NH3", "VOC",
        # HAPS (hazardous air pollutants)
        "hap_106990" ,"hap_75070" ,"hap_107028" ,"hap_120127" ,"hap_56553" ,"hap_71432",
        "hap_203338" ,"hap_50328" ,"hap_195197" ,"hap_192972" ,"hap_191242" ,"hap_207089",
        "hap_56832736" ,"hap_463581" ,"hap_218019" ,"hap_206440" ,"hap_50000" ,"hap_193395",
        "hap_74873" ,"hap_26714181" ,"hap_247" ,"hap_248" ,"hap_2381217" ,"hap_110543",
        "hap_1330207" ,"hap_198550" ,"hap_85018" ,"hap_129000" ,"hap_108883"
    ]

    CLEAN_EMI_FACTOR = [
        0.000,0.961,0.0427,0.0674,0.079532,-0.0073,0.00098,0.015376,0.22103,
        # HAPS (hazardous air pollutants)
        0.405 / 2000.0,
        0.40825 / 2000.0,
        0.424 / 2000.0,
        0.005 / 2000.0,
        0.0062 / 2000.0,
        1.125 / 2000.0,
        0.0026 / 2000.0,
        0.00148 / 2000.0,
        0.0039 / 2000.0,
        0.00266 / 2000.0,
        0.00508 / 2000.0,
        0.0026 / 2000.0,
        0.00514 / 2000.0,
        0.000534 / 2000.0,
        0.0062 / 2000.0,
        0.00673 / 2000.0,
        2.575 / 2000.0,
        0.00341 / 2000.0,
        0.128325 / 2000.0,
        0.00823 / 2000.0,
        0.00296 / 2000.0,
        0.0079 / 2000.0,
        0.00905 / 2000.0,
        0.0164025 / 2000.0,
        0.242 / 2000.0,
        0.000856 / 2000.0,
        0.005 / 2000.0,
        0.00929 / 2000.0,
        0.56825 / 2000.0
    ]

    EMI_EFFIC_FACTOR = [
        -1.833,0.988,0.0432,0.0668,0.078824,-0.0108,0.00000,0.015744,0.22632
        # HAPS (hazardous air pollutants)
        ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0
        ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0 ,0.0
    ]

    class PHASE:
        FLM = 0 # flaming
        STS = 1 # short-term smoldering
        LTS = 2 # long-term smoldering

    COMBUSTION_EFFIC = [
        0.90,0.76,0.76
    ]

Next, to compute the emissions factors, we extracted logic from the
emissions computing code in the BSF FEPS module. In this C code,
flame, smold, and resid are the total flaming, smoldering, and residual
consumption values
  for(p=0; p < count; p++) {
      emis->emis[p].flm = (CLEAN_EMI_FACTOR[p] - EMI_EFFIC_FACTOR[p] * COMBUSTION_EFFIC[FLM]) * flame;
      emis->emis[p].sts = (CLEAN_EMI_FACTOR[p] - EMI_EFFIC_FACTOR[p] * COMBUSTION_EFFIC[STS]) * smold;
      emis->emis[p].lts = (CLEAN_EMI_FACTOR[p] - EMI_EFFIC_FACTOR[p] * COMBUSTION_EFFIC[LTS]) * resid;
  }
Here's the python emission factor generation logic:

    zipped_factors = zip(CLEAN_EMI_FACTOR, EMI_EFFIC_FACTOR)
    flm_factors = dict(zip(POLLUTANT_NAMES, [e[0]-e[1]*COMBUSTION_EFFIC[PHASE.FLM] for e in zipped_factors]))
    sts_factors = dict(zip(POLLUTANT_NAMES, [e[0]-e[1]*COMBUSTION_EFFIC[PHASE.STS] for e in zipped_factors]))
    lst_factors = dict(zip(POLLUTANT_NAMES, [e[0]-e[1]*COMBUSTION_EFFIC[PHASE.LTS] for e in zipped_factors]))
    EFS = {
        'flaming': flm_factors,
        'smoldering': sts_factors,
        'residual': lst_factors
    }

There's no need to compute EFS more than once, since it's static, so we
computed it manually and hardcoded EFS.
"""

__author__      = "Joel Dubowy"

import copy
import re

from . import Phase
from .lookup import BasicEFLookup

__all__ = [
    'FepsEFLookup'
]

FEPS_EFS = {
    Phase.FLAMING: {
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
    Phase.RESIDUAL: {
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
    Phase.SMOLDERING: {
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

HAP_MATCHER_RE = re.compile('hap_.*')
FEPS_EFS_NO_HAPS = copy.deepcopy(FEPS_EFS)
for phase in list(FEPS_EFS_NO_HAPS.keys()):
    FEPS_EFS_NO_HAPS[phase] = {
        k:v for k,v in list(FEPS_EFS_NO_HAPS[phase].items()) if not HAP_MATCHER_RE.match(k)
    }

class FepsEFLookup(BasicEFLookup):
    """Look-up object containing FEPS EFs
    """

    def __init__(self, **options):
        """Constructor

        Options:
        - include_haps -- include HAPS (hazardous air pollutants) chemical species
        """
        # TODO: only include 'hap_*' pollutants if  is True
        efs = FEPS_EFS if options.get('include_haps') else FEPS_EFS_NO_HAPS
        self.update(copy.deepcopy(efs))
