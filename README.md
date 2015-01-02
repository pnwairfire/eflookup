# fccs2ef

This package supports the look-up of emissions factors for FCCS fuel bed types.
It is based on **Urbanski, S., 2014. Wildland fire emissions, carbon, and
climate: Emission factors. Forest Ecology and Management. 31, 51-60.

## Development

### Install Dependencies

Run the following to install dependencies:

    pip install -r requirements.txt

Run the following for installing development dependencies (like running tests):

    pip install -r dev-requirements.txt

### Setup Environment

To import fccs2ef in development, you'll have to add the repo root directory
to the search path.

## Running tests

Use pytest:

    pytest
    pytest test/fccs2ef/test_lookup.py

You can also use the ```--collect-only``` option to see a list of all tests.

    py.test --collect-only

See [pytest](http://pytest.org/latest/getting-started.html#getstarted) for more information about

## Installing

The repo is currently public. So, you don't need to be on the FERA bitbucket team
to install from the repo.

### Installing With pip

First, install pip:

    sudo apt-get install python-pip

Then, to install, for example, v0.1.0, use the following:

    sudo pip install git+https://bitbucket.org/fera/airfire-fccs2ef@v0.1.0

If you get an error like    ```AttributeError: 'NoneType' object has no attribute 'skip_requirements_regex```, it means you need in upgrade pip.  One way to do so is with the following:

    pip install --upgrade pip

## Usage:

### Using the Python Package

First import and instantiate

    >>> from fccs2ef.lookup import LookUp
    >>> lu = LookUp()

Then, get all EF's associated with a specific FCCS fuelbed id:

    >>> lu.get(4)
    {'flame_smold_rx': {'CH3CH2OH': None, 'CH3COOH': None, 'CH3OH': None, 'C2H8N2': None, 'C4H6O': None, 'isomer 3,C9H8O': None, 'MEK,C4H8O': None, 'C5H8O': None, 'CH4': 4.86, 'isomer 1': None, 'C6H8O': None, 'C5H7N': None, 'C7H14': None, 'C7H16': None, 'C4H10': None, 'C10H16': None, 'isomer 2,C10H14': None, 'PM2.5 ': 17.57, 'NOx as NO': 2.06, 'HCOOH': None, 'C4H8O2': None, 'C3H4O2': None, 'C6H12': None, 'C6H10': None, 'HCHO': None, 'C2H4O2': None, 'C2H4O3': None, 'C3H8': None, 'C6H14': None, 'sum of 3 isomers, C6H12': None, 'C11H22': None, 'isomer 2,C9H8O': None, 'NMOC': 26.98, 'C5H12': None, 'C5H10': None, 'C15H24': None, 'C11H24': None, 'C4H8O': None, 'C3H6O': None, 'C8H14': None, 'C8H16': None, 'C8H10': None, 'C2H6': None, 'CH3CHO': None, 'C2H4': None, 'HCN': None, 'C6H5OH': None, 'C6H8': None, 'C7H6O': None, 'C6H6': None, 'SO2': 1.06, 'C4H6O2': None, 'C8H6O': None, 'isomer 1,C10H14': None, 'C3H6': None, 'HNCO': None, 'C3H4': None, 'C4H5N': None, 'C5H4O2': None, 'C3H5N': None, 'C6H12O': None, 'C7H5N': None, 'C6H6O2': None, 'isomer 1,C9H8O': None, 'C2H2': None, 'C8H18': None, 'C4H6N2': None, 'C3H6O2': None, 'CO': 105.0, 'C6H8N2': None, 'isomer2,C5H6N2': None, 'isomer 1,C6H8': None, 'C9H18': None, 'C3H4O': None, 'C9H12': None, 'C9H10': None, 'C10H14': None, 'C3H4O3': None, 'CO2': 1598.0, 'C10H10': None, 'PM10': 20.7, 'C10H12': None, 'isomer 1,C7H8': None, 'CH3CN': None, 'C5H8O2': None, 'isomer 4,C9H8O': None, 'C3H3N': None, 'C6H5CH3': None, 'C5H6O': None, 'C7H12': None, 'C11': None, 'MVK,C4H6O': None, 'C10H20': None, 'C10H22': None, 'C8H6': None, 'C9H20': None, 'C8H8': None, 'isomer 5': None, 'isomer 4': None, 'C5H10O': None, 'C4H10O': None, 'isomer 3': None, 'isomer 2': None, 'C10H8': None, 'isomer1,C5H6N2': None, 'C9H16': None, 'C4H8': None, 'isomer 2,C7H8': None, 'C5H6': None, 'C5H8': None, 'C4H2': None, 'C4H4': None, 'C4H6': None, 'C4H4O': None, 'C5H10O2': None, 'NH3': 1.53, 'isomer 2,C6H8': None, 'isomer 1 ,C10H14': None, 'C9H8': None, 'isomer3,C5H6N2': None}, 'flame_smold_wf': {'CH3CH2OH': 0.32, 'CH3COOH': 4.461, 'CH3OH': 2.061, 'C2H8N2': 0.043, 'C4H6O': 0.002, 'isomer 3,C9H8O': 0.044, 'MEK,C4H8O': 0.234, 'C5H8O': 0.011, 'CH4': 7.32, 'isomer 1': 0.014, 'C6H8O': 0.048, 'C5H7N': 0.005, 'C7H14': 0.006, 'C7H16': 0.035, 'C4H10': 0.168, 'C10H16': 0.008, 'isomer 2,C10H14': 0.007, 'PM2.5 ': 23.2, 'NOx as NO': 2.0, 'HCOOH': 0.505, 'C4H8O2': 0.007, 'C3H4O2': 0.062, 'C6H12': 0.028, 'C6H10': 0.021, 'HCHO': 2.248, 'C2H4O2': 0.03, 'C2H4O3': 0.061, 'C3H8': 0.509, 'C6H14': 0.007, 'sum of 3 isomers, C6H12': 0.088, 'C11H22': 0.03, 'isomer 2,C9H8O': 0.031, 'NMOC': 33.87, 'C5H12': 0.074, 'C5H10': 0.04, 'C15H24': 0.11, 'C11H24': 0.034, 'C4H8O': 0.001, 'C3H6O': 0.193, 'C8H14': 0.039, 'C8H16': 0.061, 'C8H10': 0.068, 'C2H6': 1.077, 'CH3CHO': 1.5, 'C2H4': 1.825, 'HCN': 0.54, 'C6H5OH': 0.865, 'C6H8': 0.005, 'C7H6O': 0.367, 'C6H6': 0.003, 'SO2': 1.06, 'C4H6O2': 0.004, 'C8H6O': 0.181, 'isomer 1,C10H14': 0.012, 'C3H6': 0.698, 'HNCO': 0.198, 'C3H4': 0.044, 'C4H5N': 0.014, 'C5H4O2': 0.016, 'C3H5N': 0.016, 'C6H12O': 0.016, 'C7H5N': 0.084, 'C6H6O2': 2.206, 'isomer 1,C9H8O': 0.018, 'C2H2': 0.376, 'C8H18': 0.031, 'C4H6N2': 0.003, 'C3H6O2': 0.234, 'CO': 135.0, 'C6H8N2': 0.01, 'isomer2,C5H6N2': 0.008, 'isomer 1,C6H8': 0.013, 'C9H18': 0.017, 'C3H4O': 0.458, 'C9H12': 0.02, 'C9H10': 0.012, 'C10H14': 0.004, 'C3H4O3': 0.03, 'CO2': 1600.0, 'C10H10': 0.01, 'PM10': 27.4, 'C10H12': 0.02, 'isomer 1,C7H8': 0.002, 'CH3CN': 0.289, 'C5H8O2': 0.047, 'isomer 4,C9H8O': 0.0, 'C3H3N': 0.045, 'C6H5CH3': 0.307, 'C5H6O': 0.015, 'C7H12': 0.013, 'C11': 0.184, 'MVK,C4H6O': 0.414, 'C10H20': 0.024, 'C10H22': 0.018, 'C8H6': 0.008, 'C9H20': 0.019, 'C8H8': 0.093, 'isomer 5': 0.006, 'isomer 4': 0.294, 'C5H10O': 0.04, 'C4H10O': 0.138, 'isomer 3': 0.002, 'isomer 2': 0.001, 'C10H8': 0.435, 'isomer1,C5H6N2': 0.019, 'C9H16': 0.004, 'C4H8': 0.05, 'isomer 2,C7H8': 0.0, 'C5H6': 0.004, 'C5H8': 0.005, 'C4H2': 0.001, 'C4H4': 0.004, 'C4H6': 0.005, 'C4H4O': 0.483, 'C5H10O2': 0.023, 'NH3': 1.5, 'isomer 2,C6H8': 0.013, 'isomer 1 ,C10H14': 0.012, 'C9H8': 0.027, 'isomer3,C5H6N2': 0.004}, 'residual': {'CH3CH2OH': 0.019, 'CH3COOH': 1.837, 'CH3OH': 3.517, 'C2H8N2': 0.063, 'C4H6O': 0.003, 'isomer 3,C9H8O': 0.066, 'MEK,C4H8O': 0.323, 'C5H8O': 0.24, 'CH4': 13.94, 'isomer 1': 0.021, 'C6H8O': 0.194, 'C5H7N': 0.008, 'C7H14': 0.009, 'C7H16': 0.043, 'C4H10': 0.195, 'C10H16': 0.011, 'isomer 2,C10H14': 0.01, 'PM2.5 ': 33.0, 'NOx as NO': 0.0, 'HCOOH': 0.0, 'C4H8O2': 0.01, 'C3H4O2': 0.093, 'C6H12': 0.041, 'C6H10': 0.031, 'HCHO': 2.124, 'C2H4O2': 0.044, 'C2H4O3': 0.091, 'C3H8': 0.802, 'C6H14': 0.011, 'sum of 3 isomers, C6H12': 0.13, 'C11H22': 0.045, 'isomer 2,C9H8O': 0.046, 'NMOC': 45.243, 'C5H12': 0.095, 'C5H10': 0.072, 'C15H24': 0.163, 'C11H24': 0.05, 'C4H8O': 0.001, 'C3H6O': 0.286, 'C8H14': 0.057, 'C8H16': 0.066, 'C8H10': 0.072, 'C2H6': 2.723, 'CH3CHO': 1.546, 'C2H4': 1.398, 'HCN': 0.723, 'C6H5OH': 0.15, 'C6H8': 0.008, 'C7H6O': 0.544, 'C6H6': 0.005, 'SO2': 0.0, 'C4H6O2': 0.005, 'C8H6O': 0.268, 'isomer 1,C10H14': 0.018, 'C3H6': 1.06, 'HNCO': 0.293, 'C3H4': 0.019, 'C4H5N': 0.021, 'C5H4O2': 0.023, 'C3H5N': 0.023, 'C6H12O': 0.023, 'C7H5N': 0.124, 'C6H6O2': 3.273, 'isomer 1,C9H8O': 0.027, 'C2H2': 0.207, 'C8H18': 0.036, 'C4H6N2': 0.004, 'C3H6O2': 0.069, 'CO': 229.0, 'C6H8N2': 0.014, 'isomer2,C5H6N2': 0.011, 'isomer 1,C6H8': 0.019, 'C9H18': 0.025, 'C3H4O': 0.472, 'C9H12': 0.025, 'C9H10': 0.018, 'C10H14': 0.005, 'C3H4O3': 0.045, 'CO2': 1408.0, 'C10H10': 0.015, 'PM10': 38.9, 'C10H12': 0.03, 'isomer 1,C7H8': 0.003, 'CH3CN': 0.406, 'C5H8O2': 0.07, 'isomer 4,C9H8O': 0.0, 'C3H3N': 0.027, 'C6H5CH3': 0.579, 'C5H6O': 0.646, 'C7H12': 0.019, 'C11': 0.274, 'MVK,C4H6O': 0.194, 'C10H20': 0.036, 'C10H22': 0.027, 'C8H6': 0.072, 'C9H20': 0.034, 'C8H8': 0.064, 'isomer 5': 0.009, 'isomer 4': 0.436, 'C5H10O': 0.06, 'C4H10O': 0.204, 'isomer 3': 0.004, 'isomer 2': 0.002, 'C10H8': 0.645, 'isomer1,C5H6N2': 0.028, 'C9H16': 0.007, 'C4H8': 0.089, 'isomer 2,C7H8': 0.001, 'C5H6': 0.005, 'C5H8': 0.007, 'C4H2': 0.002, 'C4H4': 0.007, 'C4H6': 0.008, 'C4H4O': 0.855, 'C5H10O2': 0.035, 'NH3': 0.48, 'isomer 2,C6H8': 0.019, 'isomer 1 ,C10H14': 0.018, 'C9H8': 0.04, 'isomer3,C5H6N2': 0.006}, 'duff': {'CH3CH2OH': 0.495, 'CH3COOH': 8.836, 'CH3OH': 6.307, 'C2H8N2': 0.0, 'C4H6O': 0.0, 'isomer 3,C9H8O': 0.052, 'MEK,C4H8O': 0.422, 'C5H8O': 0.023, 'CH4': 7.47, 'isomer 1': 0.001, 'C6H8O': 0.076, 'C5H7N': 0.015, 'C7H14': 0.009, 'C7H16': 0.048, 'C4H10': 0.479, 'C10H16': 0.002, 'isomer 2,C10H14': 0.002, 'PM2.5 ': 50.0, 'NOx as NO': 0.67, 'HCOOH': 1.456, 'C4H8O2': 0.002, 'C3H4O2': 0.153, 'C6H12': 0.005, 'C6H10': 0.015, 'HCHO': 3.343, 'C2H4O2': 0.049, 'C2H4O3': 0.09, 'C3H8': 0.797, 'C6H14': 0.014, 'sum of 3 isomers, C6H12': 0.01, 'C11H22': 0.036, 'isomer 2,C9H8O': 0.038, 'NMOC': 68.865, 'C5H12': 0.212, 'C5H10': 0.027, 'C15H24': 0.095, 'C11H24': 0.043, 'C4H8O': 0.006, 'C3H6O': 0.353, 'C8H14': 0.05, 'C8H16': 0.087, 'C8H10': 0.101, 'C2H6': 2.08, 'CH3CHO': 2.7, 'C2H4': 1.683, 'HCN': 1.519, 'C6H5OH': 4.236, 'C6H8': 0.021, 'C7H6O': 0.583, 'C6H6': 0.016, 'SO2': 1.76, 'C4H6O2': 0.016, 'C8H6O': 0.908, 'isomer 1,C10H14': 0.002, 'C3H6': 1.814, 'HNCO': 0.271, 'C3H4': 0.042, 'C4H5N': 0.051, 'C5H4O2': 0.019, 'C3H5N': 0.024, 'C6H12O': 0.01, 'C7H5N': 0.101, 'C6H6O2': 2.69, 'isomer 1,C9H8O': 0.024, 'C2H2': 0.205, 'C8H18': 0.039, 'C4H6N2': 0.028, 'C3H6O2': 0.277, 'CO': 271.0, 'C6H8N2': 0.021, 'isomer2,C5H6N2': 0.009, 'isomer 1,C6H8': 0.028, 'C9H18': 0.023, 'C3H4O': 0.59, 'C9H12': 0.021, 'C9H10': 0.013, 'C10H14': 0.002, 'C3H4O3': 0.269, 'CO2': 1305.0, 'C10H10': 0.007, 'PM10': 59.0, 'C10H12': 0.005, 'isomer 1,C7H8': 0.005, 'CH3CN': 0.739, 'C5H8O2': 0.076, 'isomer 4,C9H8O': 0.0, 'C3H3N': 0.151, 'C6H5CH3': 0.488, 'C5H6O': 0.537, 'C7H12': 0.01, 'C11': 0.228, 'MVK,C4H6O': 0.421, 'C10H20': 0.022, 'C10H22': 0.027, 'C8H6': 0.043, 'C9H20': 0.023, 'C8H8': 0.117, 'isomer 5': 0.004, 'isomer 4': 0.008, 'C5H10O': 0.065, 'C4H10O': 1.18, 'isomer 3': 0.016, 'isomer 2': 0.004, 'C10H8': 0.815, 'isomer1,C5H6N2': 0.044, 'C9H16': 0.0, 'C4H8': 0.098, 'isomer 2,C7H8': 0.002, 'C5H6': 0.012, 'C5H8': 0.012, 'C4H2': 0.009, 'C4H4': 0.018, 'C4H6': 0.014, 'C4H4O': 1.46, 'C5H10O2': 0.004, 'NH3': 2.67, 'isomer 2,C6H8': 0.031, 'isomer 1 ,C10H14': 0.003, 'C9H8': 0.051, 'isomer3,C5H6N2': 0.0}}

Or, get specifically the flame smoldering EF's

    >>> lu.get(4, 'flame_smold_rx')
    {'CH3CH2OH': None, 'CH3COOH': None, 'CH3OH': None, 'C2H8N2': None, 'C4H6O': None, 'isomer 3,C9H8O': None, 'MEK,C4H8O': None, 'C5H8O': None, 'CH4': 4.86, 'isomer 1': None, 'C6H8O': None, 'C5H7N': None, 'C7H14': None, 'C7H16': None, 'C4H10': None, 'C10H16': None, 'isomer 2,C10H14': None, 'PM2.5 ': 17.57, 'NOx as NO': 2.06, 'HCOOH': None, 'C4H8O2': None, 'C3H4O2': None, 'C6H12': None, 'C6H10': None, 'HCHO': None, 'C2H4O2': None, 'C2H4O3': None, 'C3H8': None, 'C6H14': None, 'sum of 3 isomers, C6H12': None, 'C11H22': None, 'isomer 2,C9H8O': None, 'NMOC': 26.98, 'C5H12': None, 'C5H10': None, 'C15H24': None, 'C11H24': None, 'C4H8O': None, 'C3H6O': None, 'C8H14': None, 'C8H16': None, 'C8H10': None, 'C2H6': None, 'CH3CHO': None, 'C2H4': None, 'HCN': None, 'C6H5OH': None, 'C6H8': None, 'C7H6O': None, 'C6H6': None, 'SO2': 1.06, 'C4H6O2': None, 'C8H6O': None, 'isomer 1,C10H14': None, 'C3H6': None, 'HNCO': None, 'C3H4': None, 'C4H5N': None, 'C5H4O2': None, 'C3H5N': None, 'C6H12O': None, 'C7H5N': None, 'C6H6O2': None, 'isomer 1,C9H8O': None, 'C2H2': None, 'C8H18': None, 'C4H6N2': None, 'C3H6O2': None, 'CO': 105.0, 'C6H8N2': None, 'isomer2,C5H6N2': None, 'isomer 1,C6H8': None, 'C9H18': None, 'C3H4O': None, 'C9H12': None, 'C9H10': None, 'C10H14': None, 'C3H4O3': None, 'CO2': 1598.0, 'C10H10': None, 'PM10': 20.7, 'C10H12': None, 'isomer 1,C7H8': None, 'CH3CN': None, 'C5H8O2': None, 'isomer 4,C9H8O': None, 'C3H3N': None, 'C6H5CH3': None, 'C5H6O': None, 'C7H12': None, 'C11': None, 'MVK,C4H6O': None, 'C10H20': None, 'C10H22': None, 'C8H6': None, 'C9H20': None, 'C8H8': None, 'isomer 5': None, 'isomer 4': None, 'C5H10O': None, 'C4H10O': None, 'isomer 3': None, 'isomer 2': None, 'C10H8': None, 'isomer1,C5H6N2': None, 'C9H16': None, 'C4H8': None, 'isomer 2,C7H8': None, 'C5H6': None, 'C5H8': None, 'C4H2': None, 'C4H4': None, 'C4H6': None, 'C4H4O': None, 'C5H10O2': None, 'NH3': 1.53, 'isomer 2,C6H8': None, 'isomer 1 ,C10H14': None, 'C9H8': None, 'isomer3,C5H6N2': None}

Or, get an EF for a specific species:

    >>> lu.get(4, 'flame_smold_rx', 'CO2')
    1598.0

Note that you can use ```__getitem__``` brackets instead of get:

    # this
    lu.get(4)
    # is equivalent to
    lu[4]

    # this
    lu.get(4, 'flame_smold_rx')
    # is equivalent to
    lu[4]['flame_smold_rx']

    # this
    lu.get(4, 'flame_smold_rx', 'CO2')
    # is equivalent to
    lu[4]['flame_smold_rx']['CO2']

The one difference is that using brackets will result in KeyErrors for invalid
keys, whereas 'get' returns None if any of the arguments are invalid.

### Using the Executable In Perl

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
    my $j = `./bin/fccs2ef.py -f 13`;
    my $p = decode_json($j);

At this point ```$p``` should be a perl hash object, and you should be able
to do something like:

    print Dumper($p{"flame_smold_rx"}{"CH4"})
    ...

(Note:  I [Joel], couldn't get decode_json to work on my Mac, so take
the above code with a grain of salt.)

## TODO

- Unit tests!
