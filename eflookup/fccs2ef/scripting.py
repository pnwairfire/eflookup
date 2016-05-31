"""eflookup.fccs2ef.scripting: contains common scripting code
"""

__author__      = "Joel Dubowy"

import json
import logging
import sys
import traceback
from optparse import OptionParser

from pyairfire import scripting as pya_scripting

from eflookup.fccs2ef.lookup import LookUp

# Note: required parameters are specified as positional arguments

OPTIONAL_OPTIONS = [
    {
        'short': '-p',
        'long': '--phase',
        'help': "combustion phase ('flaming','smoldering','residual')"
    },
    {
        'short': '-f',
        'long': '--fuel-category',
        'help': "fuel category (ex. '100-hr fuels', 'stumps rotten', etc.)"
    },
    {
        'short': '-s',
        'long': '--species',
        'help': "emissions species (e.g. 'CO2', 'PM2.5')"
    },
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
        'nargs': '*'
    }
]

def run(lookup_class):
    parser, args = pya_scripting.args.parse_args([], OPTIONAL_OPTIONS,
        positional_args=POSITIONAL_ARGS)
    if len(args.id) == 0:

        pya_scripting.utils.exit_with_msg(
            "Specify one or more %s ids" % (lookup_class.__name__.replace('2Ef','')),
            extra_output=lambda: parser.print_help())

    try:
        look_up = lookup_class(
            args.rx,
            fccs_2_cover_type_file=args.fccs_2_cover_type_file,
            cover_type_2_ef_group_file=args.cover_type_2_ef_group_file,
            ef_group_2_ef_file=args.ef_group_2_ef_file
        )
        data = {}
        for a in args.id:
            r = look_up.get(args.id[0], phase=args.phase,
                fuel_category=args.fuel_category, species=args.species)
            if args.phase is not None:
                if args.fuel_category is not None:
                    if args.species is not None:
                        r = {args.species: r}
                    r = {args.fuel_category: r}
                elif args.species: # non-residual
                    r = {args.species: r}
                r = {args.phase: r}
            data.update({a: r})
        sys.stdout.write(json.dumps(data))

    except Exception, e:
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            pya_scripting.utils.exit_with_msg(traceback.format_exc(), prefix="")
        else:
            pya_scripting.utils.exit_with_msg(e.message)
