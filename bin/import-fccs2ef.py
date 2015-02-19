#!/usr/bin/env python

"""import-fccs-2-urbanski.py: reads file containing associations between FCCS
fuelbed ids and Urbanski group types, and then writes it out in more consise manner

Example calls:
 > ./bin/import-fccs-2-urbanski.py \
    -a ./input-data/fccs2safsrn2urbanskigroup.csv \
    -b ./input-data/urbanskiefs.csv \
    -y ./fccs2ef/data/fccs2urbanski.csv \
    -z ./fccs2ef/data/urbanskiefs.csv
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import logging
import sys
from optparse import OptionParser

from pyairfire import scripting

from fccs2ef.importer import (
    Fccs2CoverType, CoverType2EfGroupImporter, EfGroup2EfImporter
)

# Note: though some argue that all required parameters should be specified as
# positional arguments, I prefer using 'options' flags, even though this
# means that there are required 'options', which is oxymoronic.

REQUIRED_OPTIONS = [
    # Input files
    {
        'short': "-a",
        'long': "--fccs-2-cover-type-input",
        'help': "csv containing mapping of FCCS fuelbed id to cover type id",
        'metavar': "FILE"
    },
    {
        'short': "-b",
        'long': "--cover-type-2-ef-group-input",
        'help': "csv containing mapping of cover type id to Urbanski group sets",
        'metavar': "FILE"
    },
    {
        'short': "-c",
        'long': "--ef-group-2-efs-input",
        'help': "csv containing mapping of Urbanski group to emission factors set",
        'metavar': "FILE"
    },
    # output Files
    {
        'short': "-x",
        'long': "--fccs-2-cover-type-output",
        'help': "Name of new, pruned and encoded fccs-2-covert-type csv",
        'metavar': "FILE"
    },
    {
        'short': "-y",
        'long': "--cover-type-2-ef-group-output",
        'help': "Name of new, pruned and encoded cover-type-2-urbanski csv",
        'metavar': "FILE"
    },
    {
        'short': "-z",
        'long': "--ef-group-2-efs-output",
        'help': "Name of new, pruned and encoded ef-group-2-efs csv",
        'metavar': "FILE"
    }
]

def main():
    parser, options, args = scripting.options.parse_options(REQUIRED_OPTIONS, [])

    try:
        fccs2ct_import == Fccs2CoverType(options.fccs_2_cover_type_input)
        fccs2ct_import.write(options.fccs_2_cover_type_output)
        ct2efg_importer = CoverType2EfGroupImporter(options.cover_type_2_ef_group_input)
        ct2efg_importer.write(options.cover_type_2_ef_group_output)
        efg2efs_importer = EfGroup2EfsImporter(options.urbanski_2_ef_input)
        efg2efs_importer.write(options.urbanski_2_ef_output)

    except Exception, e:
        scripting.utils.exit_with_msg(e.message)

if __name__ == "__main__":
    main()
