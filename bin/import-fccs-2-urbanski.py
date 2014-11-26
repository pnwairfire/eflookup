#!/usr/bin/env python

"""import-fccs-2-urbanski.py: reads file containing associations between FCCS
fuelbed ids and Urbanski group types, and then writes it out in more consise manner

Example calls:
 > ./bin/import-fccs-2-urbanski.py -i ~/Downloads/fccs2safsrn2urbanskigroup.csv \
    ./fccs2ef/data/fccs2urbansky.csv
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import sys
from optparse import OptionParser

try:
    from fccs2ef.importer import Fccs2UrbanskiImporter, UrbanskiEfImporter
except:
    import os
    root_dir = os.path.abspath(os.path.join(sys.path[0], '../'))
    sys.path.insert(0, root_dir)
    from fccs2ef.importer import Fccs2UrbanskiImporter, UrbanskiEfImporter

def exit_with_msg(msg, extra_output=None):
    print "* Error: %s\n" % (msg)
    if extra_output:
        extra_output()
    sys.exit(1)

def parse_options():
    parser = OptionParser()
    parser.add_option("-a", "--fccs-2-urbanski-input",
        help="csv containing mapping of FCCS fuelbed id to Urbanski group set",
        metavar="FILE")
    parser.add_option("-b", "--urbanski-ef-input",
        help="csv containing mapping of Urbanski group to emission factors set",
        metavar="FILE")
    parser.add_option("-y", "--fccs-2-urbanski-output",
        help="Name of new, pruned and encoded fccs-2-urbanski csv",
        metavar="FILE")
    parser.add_option("-z", "--urbanski-ef-output",
        help="Name of new, pruned and encoded urbanski ef csv",
        metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose",
        help="to turn on extra output",
        action="store_true", default=False)

    options, args = parser.parse_args()

    if (not options.fccs_2_urbanski_input or not options.fccs_2_urbanski_output or
        not options.urbanski_ef_input or not options.urbanski_ef_output):
        exit_with_msg("specify input and out file names ('-a', '-b', '-y', & '-z')",
            lambda: parser.print_help())

    if options.verbose:
        print "FCCS-to-Urbanski Input: %s" % (options.fccs_2_urbanski_input)
        print "FCCS-to-Urbanski Output: %s" % (options.fccs_2_urbanski_output)
        print "Urbanski EF Input: %s" % (options.urbanski_ef_input)
        print "Urbanski EF Output: %s" % (options.urbanski_ef_output)

    return options

def main():
    options = parse_options()

    if options.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    try:
        Fccs2UrbanskiImporter(options.fccs_2_urbanski_input).write(
            options.fccs_2_urbanski_output)
        UrbanskiEfImporter(options.urbanski_ef_input).write(
            options.urbanski_ef_output)

    except Exception, e:
        raise
        exit_with_msg(e.message)

if __name__ == "__main__":
    main()
