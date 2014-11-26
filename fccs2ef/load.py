"""load.py:
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import abc
import copy
import csv
import os

# TODO: Replace classes with 3 that load:
#  1) FCCS to SAF/SRM (s)
#  2) SAF/SRM to Urbanski Group
#  3) Urbanski Group to EF set

__all__ = [
    'Fccs2UrbanskiGroupMappingLoader',
    'UrbanskiGroup2EfMappingLoader'
]

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
        csv_reader.next()

    def _load(self):
        with open(self._file_name, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            self._process_headers(csv_reader)
            for row in csv_reader:
                self._process_row(row)

    @abc.abstractmethod
    def _process_row(self):
        pass

    def get(self):
        return copy.deepcopy(self._data)

class Fccs2UrbanskiLoader(LoaderBase):
    """Fccs2UrbanskiLoader: loads from file the mappings of FCCS fuelbed ids
    to Urbanski groups
    """
    FILE_NAME = os.path.dirname(__file__) + '/data/fccs2urbanski.csv'

    def _process_row(self, row):
        self._data[row[0]] = {
            'urbanski_flame_smold_wf': row[1],
            'urbanski_residual': row[2],
            'urbanski_duff': row[3],
            'urbanski_flame_smold_rx': row[4]
        }

class EFMappingLoader(LoaderBase):
    """EFMappingLoader: loads from file the emission factors associated with
    Urbanski Group
    """

    FILE_NAME = os.path.dirname(__file__) + '/data/urbanskiefs.csv'

    def _process_headers(self,csv_reader):
        self._data = dict([(e, {}) for e in csv_reader.next() if e not in ['Pollutant', 'Formula']])

    def _process_row(self, row):
        for header, val in zip(self._data.keys(), row[2:]):
            self._data[header][row[1]] = val
