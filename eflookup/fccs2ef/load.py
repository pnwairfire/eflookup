"""eflookup.fccs2ef.load:
"""

__author__      = "Joel Dubowy"

import abc
import copy
import csv
import os
import re

from .data.fccs2covertype import FCCS_2_COVERTYPE
from .data.covertype2efgroup import COVERTYPE_2_EF_GROUP
from .data.catphase2efgroup import CAT_PHASE_2_EF_GROUP
from .data.catphase2efgroup import EF_GROUP_2_EF

__all__ = [
    'EFSetTypes',
    'Fccs2CoverType',
    'CoverType2EfGroup',
    'EfGroup2Ef'
]

class MapperBase(object):

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
        self._data = FCCS_2_COVERTYPE

class CoverType2EfGroup(MapperBase):
    def __init__(self):
        self._data = COVERTYPE_2_EF_GROUP


class CatPhase2EFGroup(MapperBase):
    def __init__(self):
        self._data = CAT_PHASE_2_EF_GROUP


class EfGroup2Ef(MapperBase):

    def __init__(self):
        self._data = EF_GROUP_2_EF

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
