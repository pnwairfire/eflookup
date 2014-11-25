"""load.py:
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import abc
import copy
import csv

__all__ = [
    'Fccs2UrbanskiGroupMappingLoader',
    'UrbanskiGroup2EfMappingLoader'
]

class LoaderBase(object):
    def __init__(self, file_name=None):
        """Constructor

        Arguments:
        file_name -- name of file containing fccs -> SAF/SRM translation
        """
        self._file_name = file_name
        self._load()
        pass

    @abc.abstractmethod
    def _load(self):
        pass

    def get(self):
        return copy.deepcopy(self._data)

class Fccs2UrbanskiGroupMappingLoader(LoaderBase):
    FILENAME = './data/fccs2safsrn2urbanskigroup.csv'

    def _load(self):
        # TODO: read file and load into dict self._data
        pass


class UrbanskiGroup2EfMappingLoader(LoaderBase):
    FILENAME = './data/fccs2safsrn2urbanskigroup.csv'

    def _load(self):
        # TODO: read file and load into dict self._data
        pass
