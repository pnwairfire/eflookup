"""importer.py: Module for importing FCCS, SAF/SRM, Urbanski data
into format required by fccs2ef module.

Note that this is module is only useful for a) creating the data
files included in this module, or b) creating custom data files.
"""

import csv
import logging

class Fccs2UrbanskiImporter(object):

    def __init__(self, input_file_name):
        self._load(input_file_name)

    def _load(self, input_file_name):
        self._mappings = []
        with open(input_file_name, 'rb') as csvfile:
            csvfile.next() # header
            for row in csv.reader(csvfile, delimiter=',', skipinitialspace=True):
                #logging.debug(str(row))
                self._mappings.append({
                    'fccs_id': int(row[0]),
                    'urbanski_flame_smold_wf': row[9],  # row 'J'
                    'urbanski_residual': row[10],  # row 'K'
                    'urbanski_duff': row[11],  # row 'L'
                    'urbanski_flame_smold_rx': row[12]  # row 'M'
                })

    def write(self, output_file_name):
        with open(output_file_name, 'wb') as csvfile:
            csvfile.write("fccs_id,urbanski_flame_smold_wf,urbanski_residual,"
                "urbanski_duff,urbanski_flame_smold_rx\n")
            for m in sorted(self._mappings, lambda a,b: cmp(a['fccs_id'], b['fccs_id'])):
                #logging.debug(str(m))
                csvfile.write(','.join([
                    str(m['fccs_id']),
                    m['urbanski_flame_smold_wf'],
                    m['urbanski_residual'],
                    m['urbanski_duff'],
                    m['urbanski_flame_smold_rx'],
                    '\n'
                ]))
