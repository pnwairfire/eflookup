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
        if lookup_class.__name__ == "Fccs2SeraEf" or lookup_class.__name__ == "CoverType2SeraEf":
            look_up = lookup_class(args.id)
        else:
            look_up = lookup_class(args.id, args.rx)
            
        r = look_up.get(
            phase=args.phase,
            fuel_category=args.fuel_category,
            fuel_sub_category=args.fuel_sub_category,
            species=args.species)

        sys.stdout.write(json.dumps(r) + '\n')

    except Exception as e:
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            scripting_utils.exit_with_msg(traceback.format_exc(), prefix="")
        else:
            scripting_utils.exit_with_msg(str(e))
