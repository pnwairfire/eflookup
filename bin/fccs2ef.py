#!/usr/bin/env python

"""fccs2ef.py: returns emissions factors associated with an FCCS fuelbed id

Example calls:
 > ./bin/fccs2ef.py -f
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import json
import sys
from optparse import OptionParser

try:
    from fccs2ef.lookup import LookUp
except:
    import os
    root_dir = os.path.abspath(os.path.join(sys.path[0], '../'))
    sys.path.insert(0, root_dir)
    from fccs2ef.lookup import LookUp

def exit_with_msg(msg, extra_output=None):
    print "* Error: %s\n" % (msg)
    if extra_output:
        extra_output()
    sys.exit(1)

def parse_options():
    parser = OptionParser()
    parser.add_option("-f", "--fccs-fuelbed-id", help="FCCS fuelbed id")
    parser.add_option("-v", "--verbose", dest="verbose",
        help="to turn on extra output", action="store_true", default=False)

    options, args = parser.parse_args()

    if not options.fccs_fuelbed_id:
        exit_with_msg("specify FCCS fuelbed id ('-f')",
            lambda: parser.print_help())

    if options.verbose:
        print "FCCS fuelbed id: %s" % (options.fccs_fuelbed_id)

    return options

def main():
    options = parse_options()

    if options.verbose:
        import logging
        logging.basicConfig(level=logging.DEBUG)

    try:
        print json.dumps(LookUp()[options.fccs_fuelbed_id])

    except Exception, e:
        raise
        exit_with_msg(e.message)

if __name__ == "__main__":
    main()
