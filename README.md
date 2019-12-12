# eflookup

This package supports the look-up of emissions factors used to compute
emissions from wildland fires.  Multiple sets of EF are supported, including:

 - FCCS specific EFs, based on Prichard, S.J. and O'Neill, S. In prep. Wildland fire EFs in North America: summary of existing data, measurement needs and management applications. International Journal of Wildland Fire.
 - FEPS style EFs

***This software is provided for research purposes only. It's output may
not accurately reflect observed data due to numerous reasons. Data are
provisional; use at own risk.***




## Python 2 and 3 Support

This package was originally developed to support python 2.7, but has since
been refactored to support 3.5. Attempts to support both 2.7 and 3.5 have
been made but are not guaranteed.




## Development

### Clone Repo

Via ssh:

    git clone git@github.com:pnwairfire/eflookup.git

or http:

    git clone https://github.com/pnwairfire/eflookup.git

### Install Dependencies

Run the following to install dependencies:

    pip install -r requirements.txt

Run the following to install packages required for development and testing:

    pip install -r requirements-test.txt
    pip install -r requirements-dev.txt

#### Notes

##### pip issues

If you get an error like    ```AttributeError: 'NoneType' object has no
attribute 'skip_requirements_regex```, it means you need in upgrade
pip. One way to do so is with the following:

    pip install --upgrade pip

### Setup Environment

To import eflookup in development, you'll have to add the repo root directory
to the search path.




## Running tests

Use pytest:

    py.test
    py.test test/eflookup/test_lookup.py

You can also use the ```--collect-only``` option to see a list of all tests.

    py.test --collect-only

See [pytest](http://pytest.org/latest/getting-started.html#getstarted) for more information about




## Installing

### Installing With pip

First, install pip (with sudo if necessary):

    apt-get install python-pip

Then, to install, for example, v3.2.1, use the following (with
sudo if necessary):

    pip install --extra-index https://pypi.airfire.org/simple eflookup==3.2.1

See the Development > Install Dependencies > Notes section, above, for
notes on resolving pip and gdal issues.




## Usage:

### Using the Python Package

#### ```eflookup.lookup.BasicEFLookup```

```BasicEFLookup``` is look-up object for arbitrary, phase specific emission
factors.  Instantiated with a nested dict of phase-specific EFS:

    >>> EFS = {
        'flaming': {
            'CH4': 0.003819999999999997,
            'CO': 0.07179999999999997,
            'VOC': 0.017341999999999996
        },
        'residual': {
            'NOx': 0.000908,
            'PM10': 0.01962576,
        },
        'smoldering': {
            'NH3': 0.00341056,
        }
    }
    >>> from eflookup.lookup import BasicEFLookup
    >>> lu = BasicEFLookup(EFS)

And then access the EFs with ```get```:

    >>> lu.get()
    {
        'flaming': {
            'CH4': 0.003819999999999997,
            'CO': 0.07179999999999997,
            'VOC': 0.017341999999999996
        },
        'residual': {
            'NOx': 0.000908,
            'PM10': 0.01962576
        },
        'smoldering': {
            'NH3': 0.00341056
        }
    }
    >>> lu.get(phase='flaming')
    {
        'CH4': 0.003819999999999997,
        'CO': 0.07179999999999997,
        'VOC': 0.017341999999999996
    }
    >>> lu.get(phase='flaming', species='CO')
    0.07179999999999997

 or ```[]```:

    >>> lu
    {
        'flaming': {
            'CH4': 0.003819999999999997,
            'CO': 0.07179999999999997,
            'VOC': 0.017341999999999996
        },
        'residual': {
            'NOx': 0.000908,
            'PM10': 0.01962576
        },
        'smoldering': {
            'NH3': 0.00341056
        }
    }
    >>> lu['flaming']
    {
        'CH4': 0.003819999999999997,
        'CO': 0.07179999999999997,
        'VOC': 0.017341999999999996
    }
    >>> lu['flaming']['CO']
    0.07179999999999997

The one difference is that using brackets will result in KeyErrors for invalid
keys, whereas 'get' returns `None` if any of the arguments are invalid.  For example:

    >>> lu.get(phase='flaminsdfg')
    >>> lu['flaminsdfg']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'flaminsdfg'



#### ```eflookup.fepsef.FepsEFLookup```

There's only one look-up class for FEPS style EFs.  It has one option: to include
or exclude HAPS (hazardous air pollutants) chemical species; the default is to
exclude them.  The following example includes them, but the usage is identical if
they are excluded.

First, import and instantiate:

    >>> from eflookup.fepsef import FepsEFLookup
    >>> lu = FepsEFLookup(include_haps=True)

Then, get all EFs

    >>> lu.get()
    {
        'flaming': {
            'CH4': 0.003819999999999997,
            'CO': 0.07179999999999997,
            ...
            'hap_85018': 2.5e-06
        },
        'residual': {
            'CH4': 0.009868000000000002,
            'CO': 0.21011999999999997,
            ...
            'hap_85018': 2.5e-06
        },
        'smoldering': {
            'CH4': 0.009868000000000002,
            'CO': 0.21011999999999997,
            ...
            'hap_85018': 2.5e-06
        }
    }

Or, get specifically the flaming EFs

    >>> lu.get(phase='flaming')
    {
        'CH4': 0.003819999999999997,
        'CO': 0.07179999999999997,
        ...
        'hap_85018': 2.5e-06
    }

Or, get an EF for a specific species

    >>> lu.get(phase='flaming', species='CO')
    0.07179999999999997

As with BasicEFLookup, you can use ```[]```

    >>> lu['flaming']
    {
        'CH4': 0.003819999999999997,
        'CO': 0.07179999999999997,
        ...
        'hap_85018': 2.5e-06
    }

    >>> lu['flaming']['CO']
    0.07179999999999997



#### ```eflookup.fccs2ef```

There are four look-up classes to choose from, depending on whether you're
keying off of FCCS id or cover type:
Fccs2Ef, Fccs2SeraEf, CoverType2Ef, CoverType2SeraEf.
Also, each class can be instantiated either for wild fires or Rx burns. The following
example illustrates use of Fccs2Ef for an Rx burn, but the usage of
CoverType2Ef is identical other than passing in a cover type id instead of
an FCCS id, and the usage for wild fires is identical other than setting
is_rx to False when instantiating the look-up object.

Fccs2SeraEf (and CoverType2SeraEf) try to lookup the species (pollutant) in the SERA data.
If the pollutant is not found, then the original Fccs2Ef (or CoverType2Ef) class is used.<br>
Optionally, the "stat" can be specified:<br>
EF = emissions factor (this is the default if not specified)<br>
SD = standard deviation<br>
n = count<br>
all: returns EF, SD, and n<br>
Example usage:

    >>> from eflookup.fccs2ef import Fccs2SeraEf
    >>> lu = Fccs2SeraEf(52)
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="PM2.5")
    13.5
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="PM2.5", stat="all")
    {'SD': 5.18, 'n': 21, 'EF': 13.5}
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="PM2.5", stat="SD")
    5.18
    >>>
    >>>
    >>> from eflookup.fccs2ef import CoverType2SeraEf
    >>> lu = CoverType2SeraEf(118)
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="PM2.5", stat="SD")
    5.18
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="PM2.5")
    13.5
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="PM2.5", stat="all")
    {'SD': 5.18, 'n': 21, 'EF': 13.5}

This next case shows a species that is not in the SERA data. When looking up values in Fccs2SeraEf,
the is_rx setting comes into play. It can be set using set_is_rx().

    >>>
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="C2H2")
    0.312
    >>> lu.set_is_rx(False)
    >>> lu.get(phase="flaming",fuel_category="woody fuels",fuel_sub_category="1-hr fuels",species="C2H2")
    0.24

First import and instantiate

    >>> from eflookup.fccs2ef import Fccs2Ef
    >>> lu = Fccs2Ef(4, is_rx=True)

then get the EF for a given fuel category, fuel sub-category, phase,
and species.

    >>> lu.get(phase="flaming", fuel_category="nonwoody",
            fuel_sub_category="primary live", species="PM2.5")
    17.57

If no corresponding EF, `None` is returned

    >>> lu.get(phase="residual", fuel_category="nonwoody",
            fuel_sub_category="primary live", species="PM2.5")

Note that `fccs2ef` does not support using ```__getitem__``` brackets
instead of get.



### Using the Executables

#### ```fepsef```

To get all EFs:

    $ fepsef
    {"smoldering": {"CO2": 1.39308, "CO": 0.21011999999999997, "PM10": 0.01962576, "VOC": 0.04902680000000001, "SO2": 0.00098, "CH4": 0.009868000000000002, "NH3": 0.00341056, "NOx": 0.000908, "PM2.5": 0.016632}, "flaming": {"CO2": 1.6497, "CO": 0.07179999999999997, "PM10": 0.008590399999999998, "VOC": 0.017341999999999996, "SO2": 0.00098, "CH4": 0.003819999999999997, "NH3": 0.0012063999999999998, "NOx": 0.002420000000000001, "PM2.5": 0.007280000000000002}, "residual": {"CO2": 1.39308, "CO": 0.21011999999999997, "PM10": 0.01962576, "VOC": 0.04902680000000001, "SO2": 0.00098, "CH4": 0.009868000000000002, "NH3": 0.00341056, "NOx": 0.000908, "PM2.5": 0.016632}}

To get all EFs for a particular phase:

    $ fepsef -p flaming
    {"flaming": {"CO2": 1.6497, "CO": 0.07179999999999997, "PM10": 0.008590399999999998, "VOC": 0.017341999999999996, "SO2": 0.00098, "CH4": 0.003819999999999997, "NH3": 0.0012063999999999998, "NOx": 0.002420000000000001, "PM2.5": 0.007280000000000002}}

To get the EF for a particular chemical species

    $ fepsef -p flaming -s CO
    {"flaming": {"CO": 0.07179999999999997}}

Any call to ```fepsef``` can be made with '-i'/'--include-haps-polutants'
option, which as the name implies, will include the HAPS (hazardous air
pollutants) chemical species.  For example:

    $ fepsef --include-haps-polutants -p flaming
    {"flaming": {"hap_75070": 0.000204125, "hap_120127": 2.5e-06, "hap_203338": 1.2999999999999998e-06, "hap_108883": 0.00028412500000000004, "hap_74873": 6.41625e-05, "hap_50328": 7.4e-07, "hap_192972": 1.33e-06, "hap_85018": 2.5e-06, "hap_206440": 3.365e-06, "hap_1330207": 0.000121, "hap_195197": 1.95e-06, "hap_56832736": 2.57e-06, "CH4": 0.003819999999999997, "hap_26714181": 4.1149999999999996e-06, "PM2.5": 0.007280000000000002, "hap_2381217": 4.525000000000001e-06, "hap_463581": 2.67e-07, "CO": 0.07179999999999997, "hap_129000": 4.6449999999999996e-06, "SO2": 0.00098, "NOx": 0.002420000000000001, "NH3": 0.0012063999999999998, "hap_247": 1.48e-06, "hap_106990": 0.00020250000000000002, "hap_56553": 3.1e-06, "CO2": 1.6497, "hap_198550": 4.28e-07, "PM10": 0.008590399999999998, "hap_50000": 0.0012875, "VOC": 0.017341999999999996, "hap_110543": 8.20125e-06, "hap_248": 3.95e-06, "hap_218019": 3.1e-06, "hap_207089": 1.2999999999999998e-06, "hap_193395": 1.705e-06, "hap_191242": 2.5400000000000002e-06, "hap_71432": 0.0005625, "hap_107028": 0.000212}}

The -i option will have no effect if you're specifying a non-HAP species:

    $ fepsef -p flaming -s CO
    {"flaming": {"CO": 0.07179999999999997}}
    $ fepsef -i -p flaming -s CO
    {"flaming": {"CO": 0.07179999999999997}}

But the -i option must be used if you specify a HAP species:

    $ fepsef -p flaming -s hap_191242
    {"flaming": {"hap_191242": null}}
    $ fepsef -p flaming -s hap_191242 -i
    {"flaming": {"hap_191242": 2.5400000000000002e-06}}

Note that, when using the script, the resulting JSON data's nested depth is the
same regardless of the input specificity.  The format is always like the following:

    {
        <PHASE>: {
            <SPECIES>: ...
        }
    }


#### ```fccs2ef``` & ```ct2ef```

There are two scripts to choose from, again depending on whether you're
keying off of FCCS id or cover type - '''fccs2ef''' and '''ct2ef'''.  The
following example illustrates use of '''fccs2ef''' for a wild fire (the default
fire type), but as with the classes described above, the usage of '''ct2ef'''
is identical other than passing in a cover type id instead of an FCCS id.
Using the scripts for Rx burns is also idential other than having to add the
option '--rx'

To see the script's usage, you can use the '-h' options:

    fccs2ef -h

The script takes an FCCS id, phase, fuel_category, fuel_sub_category, and species
the associated EF value. For example:

    $ $ ./bin/fccs2ef 52 flaming 'woody fuels' '1-hr fuels' PM2.5
    26.0



### Invoking the Executables In Perl

The following example illustrates using fccs2ef, but could be easily modified
to work for the other executables.

#### Setup

To use the code below, you'll need JSON, which you can install with cpanm

    sudo cpanm --install JSON::Parse

To try it in a perl console, you can either use:

    perl -d -e 1

or you can use Devel::Repl, which you can install with

    sudo cpanm --install TAP::Harness::Env
    sudo cpanm --install MooseX::Object::Pluggable
    sudo cpanm --install Devel::REPL
    sudo cpanm --install Devel::REPL::Script

and invoked with

    re.pl

#### The Code

Once you're in the console (or in your perl script), you can do something
like the following:

    use JSON;
    use Data::Dumper;
    my $j = `fccs2ef 13`;
    my $p = decode_json($j);

At this point ```$p``` should be a perl hash object, and you should be able
to do something like:

    print Dumper($p{"flaming"}{"CH4"})
    ...

(Note:  I [Joel], couldn't get decode_json to work on my Mac, so take
the above code with a grain of salt.)
