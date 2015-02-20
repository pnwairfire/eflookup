"""lookup.py: contains common scripting code
"""

__author__      = "Joel Dubowy"
__copyright__   = "Copyright 2014, AirFire, PNW, USFS"

import json
import logging
import sys
import traceback
from optparse import OptionParser

from pyairfire import scripting as pya_scripting

from fccs2ef.lookup import LookUp

# Note: required parameters are specified as positional arguments

OPTIONAL_OPTIONS = [
    {
        'short': '-e',
        'long': '--ef-set',
        'help': "ef category ('flame_smold_wf','flame_smold_rx','woody_rsc', or 'duff_rsc')"
    },
    {
        'short': '-s',
        'long': '--species',
        'help': "emissions species (e.g. 'CO2', 'PM2.5')"
    },
    # Options to specify alternate data files
    {
        'long': '--fccs-2-cover-type-file',
        'help': "csv containing mappings of FCCS fuelbed id to cover type id",
        'metavar': "FILE"
    },
    {
        'long': '--cover-type-2-ef-group-file',
        'help': "csv containing mappings of cover type id to emission factor group",
        'metavar': "FILE"
    },
    {
        'long': "--ef-group-2-ef-file",
        'help': "csv containing mappings of emission factor group to emission factors set",
        'metavar': "FILE"
    }
]

USAGE = "usage: %prog [options] <id> [<id> ...]"

def run(lookup_class):
    parser, options, args = pya_scripting.options.parse_options([],
        OPTIONAL_OPTIONS, usage=USAGE)
    if len(args) == 0:

        pya_scripting.utils.exit_with_msg(
            "Specify one or more %s ids" % (lookup_class.__name__.replace('2Ef','')),
            extra_output=lambda: parser.print_help())

    try:
        look_up = lookup_class(
            fccs_2_cover_type_file=options.fccs_2_cover_type_file,
            cover_type_2_ef_group_file=options.cover_type_2_ef_group_file,
            ef_group_2_ef_file=options.ef_group_2_ef_file
        )
        data = {}
        for a in args:
            r = look_up.get(args[0], ef_set_type=options.ef_set,
                species=options.species)
            if options.ef_set is not None and options.species is not None:
                r = {options.ef_set: {options.species: r}}
            elif options.ef_set:
                r = {options.ef_set: r}
            data.update({a: r})
        sys.stdout.write(json.dumps(data))

    except Exception, e:
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            pya_scripting.utils.exit_with_msg(traceback.format_exc(), prefix="")
        else:
            pya_scripting.utils.exit_with_msg(e.message)
