"""io.py:
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import abc
import copy
import csv

__all__ = [
    'Fccs2SafSrmParser',
    'UrbanskiEfParser'
]

class ParserBase(object):
    def __init__(self, file_name):
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

class Fccs2SafSrmParser(ParserBase):
    def _load(self):
        # TODO: read file and load into dict self._data
        pass


class UrbanskiEfParser(ParserBase):
    def _load(self):
        # TODO: read file and load into dict self._data
        pass
