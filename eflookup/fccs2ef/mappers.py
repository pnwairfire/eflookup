"""eflookup.fccs2ef.load:
"""

__author__      = "Joel Dubowy"

import abc
import copy
import csv
import os
import re

from .data import (
    fccs2covertype,
    covertype2efgroup,
    covertype2efgroupname,
    catphase2efgroup,
    efgroup2ef,
    efgroupname2seraef,
    fuelcategory2seraphaseexceptions
)

__all__ = [
    'Fccs2CoverType',
    'CoverType2EfGroup',
    'CoverType2EfGroupName',
    'EfGroup2Ef', 
    'EfGroupName2SeraEf', 
    'FuelCategory2SeraPhaseExceptions'
]

class MapperBase(object, metaclass=abc.ABCMeta):

    def __init__(self):
        self._data = {}

    def get(self, *keys, default=None):
        d = self._data
        for i, k in enumerate(keys):
            if i == len(keys) - 1:
                d = d.get(k, default)
            else:
                d = d.get(k, {})
        return copy.deepcopy(d)


class Fccs2CoverType(MapperBase):

    def __init__(self):
        self._data = fccs2covertype.FCCS_2_COVERTYPE
        
class FuelCategory2SeraPhaseExceptions(MapperBase):

    def __init__(self):
        self._data = fuelcategory2seraphaseexceptions.FUEL_CATEGORY_2_SERA_PHASE_EXCEPTIONS

class EfGroupName2SeraEf(MapperBase):

    def __init__(self):
        self._data = efgroupname2seraef.EF_GROUP_NAME_2_SERA_EF

class CoverType2EfGroup(MapperBase):

    def __init__(self):
        self._data = covertype2efgroup.COVERTYPE_2_EF_GROUP

class CoverType2EfGroupName(MapperBase):

    def __init__(self):
        self._data = covertype2efgroupname.COVERTYPE_2_EF_GROUP_NAME


class CatPhase2EFGroup(MapperBase):
    def __init__(self):
        self._data = catphase2efgroup.CAT_PHASE_2_EF_GROUP


class EfGroup2Ef(MapperBase):

    def __init__(self):
        self._data = efgroup2ef.EF_GROUP_2_EF

    WOODY_RSC_IDX = '7'
    DUFF_RSC_IDX = '8'

    def _process_headers(self,csv_reader):
        self._headers = next(csv_reader)[2:]
        self._data = dict([(e, {}) for e in self._headers])

    def _process_row(self, row):
        for header, val in zip(self._headers, row[2:]):
            self._data[header][row[1]] = float(val) if val else None

    def get_woody_rsc(self):
        return copy.deepcopy(self._data[self.WOODY_RSC_IDX])

    def get_duff_rsc(self):
        return copy.deepcopy(self._data[self.DUFF_RSC_IDX])
