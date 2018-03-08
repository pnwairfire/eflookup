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

from ..constants import CONSUME_FUEL_CATEGORY_TRANSLATIONS

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


##
## Fccs2CoverType
##

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


##
## CoverType2EfGroup
##

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


##
## CatPhase2EFGroup
##

class CatPhase2EFGroupImporter(ImporterBase):
    """CatPhase2EFGroupImporter: imports regional EF group assignments
    for specific chemical species + consume category combinations.

    TODO: skip 'Category' column, and maybe 'CombustionPhase' as well
    """

    HEADER_TRANSLATIONS = {
        "Consume output variable": "consume_output_variable",
        # ignore "Category" column
        "CombustionPhase": "phase",
        "Generic Assignment": "generic_assignment"
    }



    SECOND_ROW_HEADER_PROCESSOR = re.compile(':.*$')

    def _process_first_header_row(self, csv_reader):
        # First row, We need to grab up through the last species set column
        #  'Note: This mapping should be used along with EF Group by FB to assign EFs.,,,,"CO2, CH4","CO, NOx, NH3, SO2, PM25","CO2, CO, CH4","NOx, NH3, SO2, PM25","CO2, CO, CH4, NH3, PM2.5","NOx, SO2","CO2, CO, CH4","NOx, NH3, SO2, PM25","CO2, CO, CH4, PM2.5","NOx, NH3, SO2","CO2, CO, CH4","NOx, NH3, SO2, PM25","CO2, CO, CH4, PM25","NOx, NH3, SO2","CO2, CO, CH4, NH3, PM25","NOx, SO2","CO2, CO, CH4, NH3, PM25","NOx, SO2","CO2, CO, CH4",,"Most of the time, the emissions module will use these rules (but see exceptions)",,,These are just for reference purposes.,,,,,,,,,,EF Group,CO2,CO,CH4,NOx,NH3,SO2,PM2.5,'
        self._first_row = []
        self._first_chem_species_set_idx = None
        for i, e in enumerate(next(csv_reader)):
            if i == 0:
                # don't record the 'Note: ...'
                self._first_row.append('')
                continue

            if not e and self._first_chem_species_set_idx:
                # we've reaced the end of data that we want to record
                break

            self._first_row.append(e)
            if e and not self._first_chem_species_set_idx:
                self._first_chem_species_set_idx = i

        self._num_headers = len(self._first_row)

    def _process_second_header_row(self, csv_reader):
        # grab the same number of columns from second row
        #  'Consume output variable,Category,CombustionPhase,Generic Assignment,9-11: SE Grass,9-11: SE Grass,12-14: SE Hdwd,12-14: SE Hdwd,15-17: SE Pine,15-17: SE Pine,18-20: SE Shrub,18-20: SE Shrub,21-23: W MC,21-23: W MC,24-26: W Grass,24-26: W Grass,27-29: W Hdwd,27-29: W Hdwd,30-32: W Shrub,30-32: W Shrub,30-32: W Shrub,30-32: W Shrub,33-35: Boreal,,Simplified Rules,EF Group,,Group #,# Cover Type,Note,,,,,,,SE grass F/S,9,1700,70.2,2.67,3.26,1.2,0.97,12.08,'
        self._second_row = next(csv_reader)[:self._num_headers]

    def _combine_header_rows(self):
        # combine the two rows into single set of column headers
        self._headers = []
        self._col_idxs_to_skip = []
        for i in range(self._num_headers):

            if i < self._first_chem_species_set_idx:
                val = self._second_row[i]
                if val not in self.HEADER_TRANSLATIONS:
                    val = self._second_row[i].replace(' ', '_').lower()
                    if val not in self.HEADER_TRANSLATIONS.values():
                        # mark as column to skip
                        self._col_idxs_to_skip.append(i)
                        continue

                else:
                    val = self.HEADER_TRANSLATIONS[self._second_row[i]]

                self._headers.append(val)

            else:
                # This is the case where the first row column val is something
                # like "CO2, CH4", and the second column val is something
                # like "9-11: SE Grass"
                self._first_row_val = self._first_row[i].replace(' ', '')
                second_row_val = self.SECOND_ROW_HEADER_PROCESSOR.sub(
                    ':', self._second_row[i])
                self._headers.append(second_row_val + self._first_row_val)

    def _process_headers(self, csv_reader):
        self._process_first_header_row(csv_reader)
        self._process_second_header_row(csv_reader)
        self._combine_header_rows()

    def _process_row(self, row):
        self._mappings.append([row[i] for i in range(self._num_headers)
            if i not in self._col_idxs_to_skip])

    # extracts number range (e.g. "General (1-6)" -> '1-6')
    # and scalar number values (e.g. 'Woody RSC (7)' -> '7')
    NUMBER_RANGE_EXTRACTOR = m = re.compile('.*\(([0-9-]+)\)*')
    CONSUME_CATEGORY_PROCESSOR = re.compile('_[FSR]{1}$')
    def _process_value(self, idx, val):
        # convert 'N/A' values to empty strings
        if val == 'N/A':
            return ''

        # strip number range out of values like "General (1-6)"
        if self._headers[idx] == 'generic_assignment':
            m = self.NUMBER_RANGE_EXTRACTOR.search(val.strip())
            if m:
                return m.group(1).lower()

        if self._headers[idx] == 'consume_output_variable':
            k = self.CONSUME_CATEGORY_PROCESSOR.sub('', val).lower()
            return CONSUME_FUEL_CATEGORY_TRANSLATIONS[k]

        return val.lower()

    def write(self, output_file_name):
        with open(output_file_name, 'wt') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"',
                quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            csv_writer.writerow(self._headers)
            for m in self._mappings:
                m = [self._process_value(i, e) for i, e in enumerate(m)]
                csv_writer.writerow(m)


##
## EfGroup2Ef
##

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
