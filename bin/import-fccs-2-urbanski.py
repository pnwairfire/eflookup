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
    from fccs2ef.importer import Fccs2UrbanskiImporter
except:
    import os
    root_dir = os.path.abspath(os.path.join(sys.path[0], '../'))
    sys.path.insert(0, root_dir)
    from fccs2ef.importer import Fccs2UrbanskiImporter

def exit_with_msg(msg, extra_output=None):
    print "* Error: %s\n" % (msg)
    if extra_output:
        extra_output()
    sys.exit(1)

def parse_options():
    parser = OptionParser()
    parser.add_option("-i", "--input",
        help="csv containing mapping of FCCS fuelbed id to Urbanski group set",
        metavar="FILE")
    parser.add_option("-o", "--output", help="Name of new, pruned csv", metavar="FILE")
    parser.add_option("-v", "--verbose", dest="verbose", help="to turn on extra output",
        action="store_true", default=False)

    options, args = parser.parse_args()

    if not options.input or not options.output:
        exit_with_msg("specify input and out file names ('-i' & '-o')",
            lambda: parser.print_help())

    if options.verbose:
        print "Input: %s" % (options.input)
        print "Output: %s" % (options.output)

    return options

def main():
    options = parse_options()

    if options.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    try:
        Fccs2UrbanskiImporter(options.input).write(options.output)

    except Exception, e:
        raise
        exit_with_msg(e.message)

if __name__ == "__main__":
    main()
