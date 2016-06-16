"""eflookup.fccs2ef.load:
"""

__author__      = "Joel Dubowy"

import abc
import copy
import csv
import os

__all__ = [
    'EFSetTypes',
    'Fccs2CoverTypeLoader',
    'CoverType2EfGroupLoader',
    'EfGroup2EfLoader'
]

class EFSetTypes(object):
    """Enumeration representing ....

    @note: only flaming/smoldering WF and Rx vary from cover type to cover type,
    so only these two set types are specied here

    @note: Future versions of python have an Enum class build in, added by
    https://www.python.org/dev/peps/pep-0435/.  It's not worth requiring the
    backport (https://pypi.python.org/pypi/enum34) here, though.
    """
    FLAME_SMOLD_WF = 1
    FLAME_SMOLD_RX = 2

class LoaderBase(object):
    def __init__(self, **kwargs):
        """Constructor

        Kwargs:
        file_name -- name of file containing fccs -> SAF/SRM translation
        """
        self._file_name = kwargs.get('file_name') or self.FILE_NAME
        self._data = {}
        self._load()

    def _process_headers(self, csv_reader):
        # Default is to through away header information
        next(csv_reader)

    def _load(self):
        with open(self._file_name, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            self._process_headers(csv_reader)
            for row in csv_reader:
                self._process_row(row)

    @abc.abstractmethod
    def _process_row(self):
        pass

    def get(self, key=None, default=None):
        return copy.deepcopy(self._data)

class Fccs2CoverTypeLoader(LoaderBase):
    FILE_NAME = os.path.dirname(__file__) + '/data/fccs2covertype.csv'

    def _process_row(self, row):
        self._data[row[0]] = row[1]

class CoverType2EfGroupLoader(LoaderBase):
    FILE_NAME = os.path.dirname(__file__) + '/data/covertype2efgroup.csv'


    def _process_row(self, row):
        self._data[row[0]] = {
            EFSetTypes.FLAME_SMOLD_WF: row[1],
            EFSetTypes.FLAME_SMOLD_RX: row[2]
        }

class EfGroup2EfLoader(LoaderBase):
    FILE_NAME = os.path.dirname(__file__) + '/data/efgroup2ef.csv'

    WOODY_RSC_IDX = '7'
    DUFF_RSC_IDX = '8'

    def _process_headers(self,csv_reader):
        self._headers = csv_reader.next()[2:]
        self._data = dict([(e, {}) for e in self._headers])

    def _process_row(self, row):
        for header, val in zip(self._headers, row[2:]):
            self._data[header][row[1]] = float(val) if val else None

    def get_woody_rsc(self):
        return copy.deepcopy(self._data[self.WOODY_RSC_IDX])

    def get_duff_rsc(self):
        return copy.deepcopy(self._data[self.DUFF_RSC_IDX])
