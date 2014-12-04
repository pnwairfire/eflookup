"""importer.py: Module for importing FCCS, SAF/SRM, Urbanski data
into format required by fccs2ef module.

Note that this is module is only useful for a) creating the data
files included in this module, or b) creating custom data files.
"""

import abc
import csv
import logging

class UrbanskiGroups(object):
    """Enumeration representing Urbansnki cover type groups.

    @note: Future versions of python have an Enum class build in, added by
    https://www.python.org/dev/peps/pep-0435/.  It's not worth requiring the
    backport (https://pypi.python.org/pypi/enum34) here, though.
    """
    BOREAL_FOREST = 1
    BOREAL_RESIDUAL = 2
    CWD_RESIDUAL = 3
    GRASS = 4
    NW_FOREST_RX = 5
    SE_FOREST = 6
    SHRUB = 7
    SW_FOREST_RX = 8
    WESTERN_FOREST_WF = 9
    TEMPERATE_RESIDUAL = 10

class ImporterBase(object):

    GROUP_IDS = {
        'boreal forest': UrbanskiGroups.BOREAL_FOREST,
        'boreal residual': UrbanskiGroups.BOREAL_RESIDUAL,
        'cwd residual': UrbanskiGroups.CWD_RESIDUAL,
        'grass': UrbanskiGroups.GRASS,
        'nw forest (rx)': UrbanskiGroups.NW_FOREST_RX,
        'se forest': UrbanskiGroups.SE_FOREST,
        'shrub': UrbanskiGroups.SHRUB,
        'sw forest (rx)': UrbanskiGroups.SW_FOREST_RX,
        'temperate residual': UrbanskiGroups.TEMPERATE_RESIDUAL,
        'western forest (wf)': UrbanskiGroups.WESTERN_FOREST_WF
    }

    def __init__(self, input_file_name):
        self._load(input_file_name)

    def _str_to_group_id(self, val):
        gid = self.GROUP_IDS.get(val.lower())
        if not gid:
            logging.error("Failed to look up urbanski group '%s'", val)
        return gid

    def _load(self, input_file_name):
        self._mappings = []
        with open(input_file_name, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            self._process_headers(csv_reader)
            for row in csv_reader:
                self._process_row(row)

    def _process_headers(self, csv_reader):
        # Default is to through away header information
        csv_reader.next()

    @abc.abstractmethod
    def _process_row(self, row):
        pass

    @abc.abstractmethod
    def write(self, output_file_name):
        pass

class Fccs2UrbanskiImporter(ImporterBase):
    """Fccs2UrbanskiImporter: imports associations between FCCS fuelbed ids
    and Urbanski cover types.
    """

    def _process_row(self, row):
        self._mappings.append({
            'fccs_id': int(row[0]),
            'urbanski_flame_smold_wf': self._str_to_group_id(row[9]),  # row 'J'
            'urbanski_residual': self._str_to_group_id(row[10]),  # row 'K'
            'urbanski_duff': self._str_to_group_id(row[11]),  # row 'L'
            'urbanski_flame_smold_rx': self._str_to_group_id(row[12])  # row 'M'
        })

    def write(self, output_file_name):
        with open(output_file_name, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            csv_writer.writerow([
                "fccs_id", "urbanski_flame_smold_wf", "urbanski_residual",
                "urbanski_duff", "urbanski_flame_smold_rx"
            ])
            for m in sorted(self._mappings, lambda a,b: cmp(a['fccs_id'], b['fccs_id'])):
                #logging.debug(str(m))
                csvfile.write("%s\n" % (','.join([str(e or '') for e in [
                    m['fccs_id'],
                    m['urbanski_flame_smold_wf'],
                    m['urbanski_residual'],
                    m['urbanski_duff'],
                    m['urbanski_flame_smold_rx']
                ]])))

class UrbanskiEfImporter(ImporterBase):
    """UrbanskiEfImporter: imports urbanski group based emission factor sets.
    """

    def _process_headers(self, csv_reader):
        csv_reader.next() # first line is 'Units = g/kg'
        self._headers = [self._str_to_group_id(e) if e not in ['Pollutant', 'Formula'] else e for e in csv_reader.next()]

    def _process_row(self, row):
        self._mappings.append(row)

    def write(self, output_file_name):
        with open(output_file_name, 'wb') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            csv_writer.writerow([str(e) for e in self._headers])
            for m in self._mappings:
                csv_writer.writerow(m)
