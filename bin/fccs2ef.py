#!/usr/bin/env python

"""fccs2ef.py: returns emissions factors associated with an FCCS fuelbed id

Example calls:
 > ./bin/fccs2ef.py -f 13
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import json
import sys
from optparse import OptionParser

from pyairfire import scripting

try:
    from fccs2ef.lookup import LookUp
except:
    import os
    root_dir = os.path.abspath(os.path.join(sys.path[0], '../'))
    sys.path.insert(0, root_dir)
    from fccs2ef.lookup import LookUp

# Note: though some argue that all required parameters should be specified as
# positional arguments, I prefer using 'options' flags, even though this
# means that there are required 'options', which is oxymoronic.

REQUIRED_OPTIONS = [
    {
        'short': "-f",
        'long': "--fccs-fuelbed-id",
        'dest': 'fccs_fuelbed_id',
        'help': "FCCS fuelbed id"
    }
]

def main():
    parser, options, args = scripting.options.parse_options(REQUIRED_OPTIONS, [])

    try:
        sys.stdout.write(json.dumps(LookUp()[options.fccs_fuelbed_id]))

    except Exception, e:
        scripting.utils.exit_with_msg(e.message)

if __name__ == "__main__":
    main()
