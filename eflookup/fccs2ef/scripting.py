"""eflookup.fccs2ef.scripting: contains common scripting code
"""

__author__      = "Joel Dubowy"

import json
import logging
import sys
import traceback
from optparse import OptionParser

from afscripting import (
    args as scripting_args,
    utils as scripting_utils
)

# Note: required parameters are specified as positional arguments
REQUIRED_OPTIONS = []
OPTIONAL_OPTIONS = [
    {
        'long': '--rx',
        'help': "Is a prescribed burn",
        'action': 'store_true',
        'default': False
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

POSITIONAL_ARGS = [
    {
        'long': 'id',
    },
    {
        'long': 'phase',
        'help': "combustion phase ('flaming','smoldering','residual')"
    },
    {
        'long': 'fuel_category',
        'help': "fuel category (ex. 'woody fuels', 'ground fuels')"
    },
    {
        'long': 'fuel_sub_category',
        'help': "fuel sub-category (ex. '100-hr fuels', 'stumps rotten', etc.)"
    },
    {
        'long': 'species',
        'help': "emissions species (e.g. 'CO2', 'PM2.5')"
    }
]

def run(lookup_class, examples_string=None):
    parser, args = scripting_args.parse_args(REQUIRED_OPTIONS, OPTIONAL_OPTIONS,
        positional_args=POSITIONAL_ARGS, epilog=examples_string)
    if len(args.id) == 0:

        scripting_utils.exit_with_msg(
            "Specify one or more %s ids" % (lookup_class.__name__.replace('2Ef','')),
            extra_output=lambda: parser.print_help())

    try:
        look_up = lookup_class(args.id,args.rx,
            fccs_2_cover_type_file=args.fccs_2_cover_type_file,
            cover_type_2_ef_group_file=args.cover_type_2_ef_group_file,
            ef_group_2_ef_file=args.ef_group_2_ef_file
        )
        r = look_up.get(
            phase=args.phase,
            fuel_category=args.fuel_category,
            fuel_sub_category=args.fuel_sub_category,
            species=args.species)

        sys.stdout.write(json.dumps(r))

    except Exception as e:
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            scripting_utils.exit_with_msg(traceback.format_exc(), prefix="")
        else:
            scripting_utils.exit_with_msg(str(e))
