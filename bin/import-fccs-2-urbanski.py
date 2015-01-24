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

try:
    from fccs2ef.importer import Fccs2UrbanskiImporter, UrbanskiEfImporter
except:
    import os
    root_dir = os.path.abspath(os.path.join(sys.path[0], '../'))
    sys.path.insert(0, root_dir)
    from fccs2ef.importer import Fccs2UrbanskiImporter, UrbanskiEfImporter

# Note: though some argue that all required parameters should be specified as
# positional arguments, I prefer using 'options' flags, even though this
# means that there are required 'options', which is oxymoronic.

REQUIRED_OPTIONS = [
    {
        'short': "-a",
        'long': "--fccs-2-urbanski-input",
        'help': "csv containing mapping of FCCS fuelbed id to Urbanski group set",
        'metavar': "FILE"
    },
    {
        'short': "-b",
        'long': "--urbanski-ef-input",
        'help': "csv containing mapping of Urbanski group to emission factors set",
        'metavar': "FILE"
    },
    {
        'short': "-y",
        'long': "--fccs-2-urbanski-output",
        'help': "Name of new, pruned and encoded fccs-2-urbanski csv",
        'metavar': "FILE"
    },
    {
        'short': "-z",
        'long': "--urbanski-ef-output",
        'help': "Name of new, pruned and encoded urbanski ef csv",
        'metavar': "FILE"
    }
]

def main():
    parser, options, args = scripting.options.parse_options(REQUIRED_OPTIONS, [])

    try:
        f2u_importer = Fccs2UrbanskiImporter(options.fccs_2_urbanski_input)
        f2u_importer.write(options.fccs_2_urbanski_output)
        uef_importer = UrbanskiEfImporter(options.urbanski_ef_input)
        uef_importer.write(options.urbanski_ef_output)

        logging.info("Unrecognized Urbanski groups in fccs2urbansku file: %s" % (
            f2u_importer.unrecognized or '(None)'))
        logging.info("Unrecognized Urbanski groups in EF file header: %s" % (
            uef_importer.unrecognized or '(None)'))

    except Exception, e:
        scripting.utils.exit_with_msg(e.message)

if __name__ == "__main__":
    main()
