"""eflookup.fccs2ef.importer: Module for importing FCCS, covert type, and
emission factors data into format required by fccs2ef module.

Note that this module is only useful for a) creating the data files included
in this module, or b) creating custom data files.
"""

__author__      = "Joel Dubowy"

import abc
import csv
import logging
import re

__all__ = [
    'Fccs2CoverTypeImporter',
    'CoverType2EfGroupImporter',
    'EfGroup2EfImporter'
]

class ImporterBase(object):

    def __init__(self, input_file_name):
        self._unrecognized = set()
        self._load(input_file_name)

    def _load(self, input_file_name):
        self._mappings = []
        with open(input_file_name, 'rt') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',', skipinitialspace=True)
            self._process_headers(csv_reader)
            for row in csv_reader:
                self._process_row(row)

    def _process_headers(self, csv_reader):
        # Default is to through away header information
        next(csv_reader)

    # @property
    # def unrecognized(self):
    #     return list(self._unrecognized)

    @abc.abstractmethod
    def _process_row(self, row):
        pass

    @abc.abstractmethod
    def write(self, output_file_name):
        pass

class Fccs2CoverTypeImporter(ImporterBase):
    """Fccs2CoverType imports FCCS to cover type mappings

    Due to changes in the input file (orig-fccs2covertype.csv)
    which made it match the internal fccs2covertype.csv file,
    this class doesn't do anything other than clean up the csv data,
    removing any unused columns.
    """

    FCCS_ID_COLUMN_HEADER = 'fccs_id'
    COVER_TYPE_COLUMN_HEADER = 'cover_type_id'

    def _process_headers(self, csv_reader):
        header_row = next(csv_reader)
        self._headers = dict([(header_row[i], i) for i in range(len(header_row))])

    def _process_row(self, row):
        m = (
            row[self._headers[self.FCCS_ID_COLUMN_HEADER]],
            row[self._headers[self.COVER_TYPE_COLUMN_HEADER]],
        )
        self._mappings.append(m)

    def write(self, output_file_name):
        with open(output_file_name, 'wt') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            csv_writer.writerow([
                "fccs_id", "cover_type_id"
            ])
            for m in sorted(self._mappings, key=lambda a: a[0]):
                #logging.debug(str(m))
                csvfile.write("%s\n" % (','.join(m)))

class CoverType2EfGroupImporter(ImporterBase):

    EF_GROUP_EXTRACTOR = re.compile('^[ ]*(\d+(-\d+)?):')
    def _extract_ef_group_id(self, val):
        m = self.EF_GROUP_EXTRACTOR.search(val.strip())
        if m:
            return m.group(1)
        # else, returns None

    def _process_row(self, row):
        wf = self._extract_ef_group_id(row[2])
        rx = self._extract_ef_group_id(row[3])
        regionalrx = self._extract_ef_group_id(row[4])
        self._mappings.append((row[0], wf, rx, regionalrx))

    def write(self, output_file_name):
        with open(output_file_name, 'wt') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            csv_writer.writerow([
                'cover_type_id','wf','rx', 'regionalrx'
            ])
            for m in sorted(self._mappings, key=lambda a: a[0]):
                csvfile.write("%s\n" % (','.join([e or '' for e in m])))

class EfGroup2EfImporter(ImporterBase):
    """EfGroup2EfImporter: imports grouped emission factor
    """

    def _process_headers(self, csv_reader):
        # skip first line, which looks like:
        #  'g/kg,,Urbanski + Liu (1-8),,,,,,,,Revised (9-32),,,,,,,,,,,,,,,,,,,,,,,,,,'
        next(csv_reader)
        # skip second line, which looks like:
        #  ',,SE pine,Boreal,Rx NW Conifer,WF NW Conifer,W Shrub,Grass,Residual CWD,Residual Duff,SE grass F/S,SE Grass F,SE Grass S,SE Hdwd F/S,SE Hdwd F,SE Hdwd S,SE Pine F/S,SE Pine F,SE Pine S,SE Shrub F/S,SE Shrub F,SE Shrub S,W MC F/S,W MC F,W MC S,W Grass F/S,W Grass F,W Grass S,W Hdwd F/S,W Hdwd F,W Hdwd S,W Shrub F/S,W Shrub F,W Shrub S,Boreal F/S,Boreal F,Boreal S'
        next(csv_reader)
        # leave the third line, which looks like:
        #  'Pollutant,Formula,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35'
        # since it's the header we want

    def _process_row(self, row):
        self._mappings.append(row)

    def write(self, output_file_name):
        with open(output_file_name, 'wt') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            for m in self._mappings:
                m = [e.strip() for e in m]
                # TODO: confirm that the EFs are already in lbs/ton;
                #   otherwise, convert from g/kg to lbs/ton by
                #   multiplying by 2  (since 1 g/kg == 2 lbs/ton)
                #      m[2:] = [str(float(e) * 2.0) for e in m[2:]]
                csv_writer.writerow(m)
