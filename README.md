# fccs2ef

This package supports the look-up of emissions factors by either FCCS fuelbed
or FERA cover type id.  The categorization of emissions factors is based on
**Urbanski, S., 2014. Wildland fire emissions, carbon, and climate: Emission
factors. Forest Ecology and Management. 31, 51-60.

## Development

### Install Dependencies

Run the following to install dependencies:

    pip install -r requirements.txt

Run the following for installing development dependencies (like running tests):

    pip install -r requirements-test.txt

### Setup Environment

To import fccs2ef in development, you'll have to add the repo root directory
to the search path.

## Running tests

Use pytest:

    py.test
    py.test test/fccs2ef/test_lookup.py

You can also use the ```--collect-only``` option to see a list of all tests.

    py.test --collect-only

See [pytest](http://pytest.org/latest/getting-started.html#getstarted) for more information about

## Installing

### Installing With pip

First, install pip:

    sudo apt-get install python-pip

Then, to install, for example, v0.3.4, use the following:

    sudo pip install git+https://github.com/pnwairfire/fccs2ef@v0.3.4

If you get an error like    ```AttributeError: 'NoneType' object has no attribute 'skip_requirements_regex```, it means you need in upgrade pip.  One way to do so is with the following:

    pip install --upgrade pip

## Usage:

### Using the Python Package

There are two look-up classes to choose from, depending on whether you're
keying off of FCCS id or cover type - Fccs2Ef and CoverType2Ef.  The following
example illustrates use of Fccs2Ef, but the usage of CoverType2Ef is identical
other than passing in a cover type id instead of an FCCS id.

First import and instantiate

    >>> from fccs2ef.lookup import Fccs2Ef
    >>> lu = Fccs2Ef()

Then, get all EF's associated with a specific FCCS fuelbed id:

    >>> lu.get(4)
    {'duff_rsc': {'CH3CH2OH': 0.99, 'CH3COOH': 14.799, 'CH3OH': 9.355, 'C2H8N2': 0.0, 'isomer2_C9H8O': 0.076, 'isomer2_C6H8': 0.062, 'C3H4': 0.084, 'C9H12': 0.042, 'C5H8O': 0.046, 'CH4': 15.89, 'C5H10O': 0.13, 'isomer2_C7H8': 0.004, 'C6H8O': 0.152, 'C5H7N': 0.03, 'C7H14': 0.018, 'C7H16': 0.096, 'isomer1_C5H6N2': 0.088, 'C4H10': 0.958, 'C10H16': 0.004, 'isomer3_C6H10': 0.032, 'C4H6O': 0.0, 'HCOOH': 2.189, 'C4H8O2': 0.004, 'C3H4O2': 0.306, 'C6H12': 0.01, 'C6H10': 0.03, 'HCHO': 4.953, 'isomer1_C10H14': 0.006, 'C2H4O2': 0.098, 'C2H4O3': 0.18, 'isomer1_C7H8': 0.01, 'C3H8': 1.594, 'C6H14': 0.028, 'isomer4_C9H8O': 0.0, 'C11H22': 0.072, 'NMOC': 123.391, 'C5H12': 0.424, 'C5H10': 0.054, 'isomer1_C6H10': 0.002, 'C15H24': 0.19, 'isomer5_C6H10': 0.008, 'C11H24': 0.086, 'C4H8O': 0.012, 'C3H6O': 0.706, 'C8H14': 0.1, 'C8H16': 0.174, 'NOx': 1.34, 'C8H10': 0.202, 'C2H6': 4.24, 'CH3CHO': 5.4, 'C2H4': 2.929, 'HCN': 3.976, 'C6H5OH': 5.281, 'C6H8': 0.042, 'C7H6O': 1.166, 'C6H6': 0.032, 'SO2': 3.52, 'C4H6O2': 0.032, 'C8H6O': 1.816, 'C3H6': 3.581, 'HNCO': 0.542, 'isomer1_C9H8O': 0.048, 'MEK_C4H8O': 0.844, 'C4H5N': 0.102, 'C5H4O2': 0.038, 'C3H5N': 0.048, 'C6H12O': 0.02, 'C7H5N': 0.202, 'C6H6O2': 5.38, 'C8H18': 0.078, 'isomer3_C9H8O': 0.104, 'C4H6N2': 0.056, 'C3H6O2': 0.554, 'sum3isos_C6H12': 0.02, 'CO': 514.0, 'C6H8N2': 0.042, 'C9H18': 0.046, 'C3H4O': 1.18, 'isomer2_C5H6N2': 0.018, 'C9H10': 0.026, 'C10H14': 0.004, 'C3H4O3': 0.538, 'CO2': 2742.0, 'C10H10': 0.014, 'PM10': 83.308, 'C10H12': 0.01, 'CH3CN': 1.478, 'C5H8O2': 0.152, 'isomer3_C5H6N2': 0.0, 'C3H3N': 0.302, 'C6H5CH3': 0.976, 'C5H6O': 1.074, 'C7H12': 0.02, 'MVK_C4H6O': 0.842, 'PM2.5': 70.6, 'C11': 0.456, 'C9H20': 0.046, 'C10H20': 0.044, 'C10H22': 0.054, 'C8H6': 0.086, 'C8H8': 0.234, 'C9H8': 0.102, 'C4H10O': 2.36, 'C10H8': 1.63, 'C9H16': 0.0, 'C4H8': 0.196, 'C5H6': 0.024, 'C5H8': 0.024, 'C4H2': 0.018, 'C4H4': 0.036, 'C4H6': 0.028, 'C4H4O': 2.53, 'C2H2': 0.314, 'C5H10O2': 0.008, 'NH3': 5.34, 'isomer2_C10H14': 0.004, 'isomer1_C6H8': 0.056, 'isomer2_C6H10': 0.008, 'isomer4': 0.016}, 'flame_smold_rx': {'CH3CH2OH': 0.478, 'CH3COOH': 6.04, 'CH3OH': 5.03, 'C2H8N2': 0.064, 'isomer2_C9H8O': 0.046, 'isomer2_C6H8': 0.02, 'C3H4': 0.066, 'C9H12': 0.03, 'C5H8O': 0.016, 'CH4': 9.72, 'C5H10O': 0.06, 'isomer2_C7H8': 0.0, 'C6H8O': 0.072, 'C5H7N': 0.008, 'C7H14': 0.008, 'C7H16': 0.052, 'isomer1_C5H6N2': 0.028, 'C4H10': 0.252, 'C10H16': 0.012, 'isomer3_C6H10': 0.004, 'C4H6O': 0.002, 'HCOOH': 0.368, 'C4H8O2': 0.01, 'C3H4O2': 0.094, 'C6H12': 0.042, 'C6H10': 0.03, 'HCHO': 4.47, 'isomer1_C10H14': 0.018, 'C2H4O2': 0.044, 'C2H4O3': 0.092, 'isomer1_C7H8': 0.004, 'C3H8': 0.484, 'C6H14': 0.01, 'isomer4_C9H8O': 0.0, 'C11H22': 0.046, 'NMOC': 53.95, 'C5H12': 0.11, 'C5H10': 0.06, 'isomer1_C6H10': 0.022, 'C15H24': 0.164, 'isomer5_C6H10': 0.01, 'C11H24': 0.05, 'C4H8O': 0.0, 'C3H6O': 0.288, 'C8H14': 0.058, 'C8H16': 0.092, 'NOx': 4.12, 'C8H10': 0.1, 'C2H6': 1.33, 'CH3CHO': 2.238, 'C2H4': 2.762, 'HCN': 1.53, 'C6H5OH': 1.6, 'C6H8': 0.008, 'C7H6O': 0.548, 'C6H6': 0.006, 'SO2': 2.12, 'C4H6O2': 0.006, 'C8H6O': 0.27, 'C3H6': 1.446, 'HNCO': 0.294, 'isomer1_C9H8O': 0.026, 'MEK_C4H8O': 0.35, 'C4H5N': 0.02, 'C5H4O2': 0.024, 'C3H5N': 0.024, 'C6H12O': 0.024, 'C7H5N': 0.124, 'C6H6O2': 3.294, 'C8H18': 0.046, 'isomer3_C9H8O': 0.066, 'C4H6N2': 0.004, 'C3H6O2': 0.348, 'sum3isos_C6H12': 0.132, 'CO': 210.0, 'C6H8N2': 0.014, 'C9H18': 0.026, 'C3H4O': 0.684, 'isomer2_C5H6N2': 0.012, 'C9H10': 0.018, 'C10H14': 0.006, 'C3H4O3': 0.046, 'CO2': 3196.0, 'C10H10': 0.016, 'PM10': 41.4652, 'C10H12': 0.03, 'CH3CN': 0.43, 'C5H8O2': 0.07, 'isomer3_C5H6N2': 0.006, 'C3H3N': 0.068, 'C6H5CH3': 0.458, 'C5H6O': 0.022, 'C7H12': 0.02, 'MVK_C4H6O': 0.618, 'PM2.5': 35.14, 'C11': 0.276, 'C9H20': 0.028, 'C10H20': 0.036, 'C10H22': 0.028, 'C8H6': 0.012, 'C8H8': 0.138, 'C9H8': 0.04, 'C4H10O': 0.206, 'C10H8': 0.65, 'C9H16': 0.006, 'C4H8': 0.076, 'C5H6': 0.006, 'C5H8': 0.006, 'C4H2': 0.002, 'C4H4': 0.006, 'C4H6': 0.008, 'C4H4O': 0.98, 'C2H2': 0.624, 'C5H10O2': 0.034, 'NH3': 3.06, 'isomer2_C10H14': 0.01, 'isomer1_C6H8': 0.02, 'isomer2_C6H10': 0.002, 'isomer4': 0.438}, 'flame_smold_wf': {'CH3CH2OH': 0.64, 'CH3COOH': 8.922, 'CH3OH': 4.122, 'C2H8N2': 0.086, 'isomer2_C9H8O': 0.062, 'isomer2_C6H8': 0.026, 'C3H4': 0.088, 'C9H12': 0.04, 'C5H8O': 0.022, 'CH4': 14.64, 'C5H10O': 0.08, 'isomer2_C7H8': 0.0, 'C6H8O': 0.096, 'C5H7N': 0.01, 'C7H14': 0.012, 'C7H16': 0.07, 'isomer1_C5H6N2': 0.038, 'C4H10': 0.336, 'C10H16': 0.016, 'isomer3_C6H10': 0.004, 'C4H6O': 0.004, 'HCOOH': 1.01, 'C4H8O2': 0.014, 'C3H4O2': 0.124, 'C6H12': 0.056, 'C6H10': 0.042, 'HCHO': 4.496, 'isomer1_C10H14': 0.024, 'C2H4O2': 0.06, 'C2H4O3': 0.122, 'isomer1_C7H8': 0.004, 'C3H8': 1.018, 'C6H14': 0.014, 'isomer4_C9H8O': 0.0, 'C11H22': 0.06, 'NMOC': 67.748, 'C5H12': 0.148, 'C5H10': 0.08, 'isomer1_C6H10': 0.028, 'C15H24': 0.22, 'isomer5_C6H10': 0.012, 'C11H24': 0.068, 'C4H8O': 0.002, 'C3H6O': 0.386, 'C8H14': 0.078, 'C8H16': 0.122, 'NOx': 4.0, 'C8H10': 0.136, 'C2H6': 2.154, 'CH3CHO': 3.0, 'C2H4': 3.65, 'HCN': 1.08, 'C6H5OH': 1.73, 'C6H8': 0.01, 'C7H6O': 0.734, 'C6H6': 0.006, 'SO2': 2.12, 'C4H6O2': 0.008, 'C8H6O': 0.362, 'C3H6': 1.396, 'HNCO': 0.396, 'isomer1_C9H8O': 0.036, 'MEK_C4H8O': 0.468, 'C4H5N': 0.028, 'C5H4O2': 0.032, 'C3H5N': 0.032, 'C6H12O': 0.032, 'C7H5N': 0.168, 'C6H6O2': 4.412, 'C8H18': 0.062, 'isomer3_C9H8O': 0.088, 'C4H6N2': 0.006, 'C3H6O2': 0.468, 'sum3isos_C6H12': 0.176, 'CO': 270.0, 'C6H8N2': 0.02, 'C9H18': 0.034, 'C3H4O': 0.916, 'isomer2_C5H6N2': 0.016, 'C9H10': 0.024, 'C10H14': 0.008, 'C3H4O3': 0.06, 'CO2': 3200.0, 'C10H10': 0.02, 'PM10': 54.752, 'C10H12': 0.04, 'CH3CN': 0.578, 'C5H8O2': 0.094, 'isomer3_C5H6N2': 0.008, 'C3H3N': 0.09, 'C6H5CH3': 0.614, 'C5H6O': 0.03, 'C7H12': 0.026, 'MVK_C4H6O': 0.828, 'PM2.5': 46.4, 'C11': 0.368, 'C9H20': 0.038, 'C10H20': 0.048, 'C10H22': 0.036, 'C8H6': 0.016, 'C8H8': 0.186, 'C9H8': 0.054, 'C4H10O': 0.276, 'C10H8': 0.87, 'C9H16': 0.008, 'C4H8': 0.1, 'C5H6': 0.008, 'C5H8': 0.01, 'C4H2': 0.002, 'C4H4': 0.008, 'C4H6': 0.01, 'C4H4O': 0.966, 'C2H2': 0.752, 'C5H10O2': 0.046, 'NH3': 3.0, 'isomer2_C10H14': 0.014, 'isomer1_C6H8': 0.026, 'isomer2_C6H10': 0.002, 'isomer4': 0.588}, 'woody_rsc': {'CH3CH2OH': 0.038, 'CH3COOH': 3.674, 'CH3OH': 7.034, 'C2H8N2': 0.126, 'isomer2_C9H8O': 0.092, 'isomer2_C6H8': 0.038, 'C3H4': 0.038, 'C9H12': 0.05, 'C5H8O': 0.48, 'CH4': 27.88, 'C5H10O': 0.12, 'isomer2_C7H8': 0.002, 'C6H8O': 0.388, 'C5H7N': 0.016, 'C7H14': 0.018, 'C7H16': 0.086, 'isomer1_C5H6N2': 0.056, 'C4H10': 0.39, 'C10H16': 0.022, 'isomer3_C6H10': 0.008, 'C4H6O': 0.006, 'HCOOH': 0.0, 'C4H8O2': 0.02, 'C3H4O2': 0.186, 'C6H12': 0.082, 'C6H10': 0.062, 'HCHO': 4.248, 'isomer1_C10H14': 0.036, 'C2H4O2': 0.088, 'C2H4O3': 0.182, 'isomer1_C7H8': 0.006, 'C3H8': 1.604, 'C6H14': 0.022, 'isomer4_C9H8O': 0.0, 'C11H22': 0.09, 'NMOC': 90.35, 'C5H12': 0.19, 'C5H10': 0.144, 'isomer1_C6H10': 0.042, 'C15H24': 0.19, 'isomer5_C6H10': 0.018, 'C11H24': 0.1, 'C4H8O': 0.002, 'C3H6O': 0.572, 'C8H14': 0.114, 'C8H16': 0.132, 'NOx': 0.0, 'C8H10': 0.144, 'C2H6': 5.446, 'CH3CHO': 3.092, 'C2H4': 2.796, 'HCN': 1.446, 'C6H5OH': 0.3, 'C6H8': 0.016, 'C7H6O': 1.088, 'C6H6': 0.01, 'SO2': 0.0, 'C4H6O2': 0.01, 'C8H6O': 0.536, 'C3H6': 2.12, 'HNCO': 0.586, 'isomer1_C9H8O': 0.054, 'MEK_C4H8O': 0.646, 'C4H5N': 0.042, 'C5H4O2': 0.046, 'C3H5N': 0.046, 'C6H12O': 0.046, 'C7H5N': 0.248, 'C6H6O2': 6.546, 'C8H18': 0.072, 'isomer3_C9H8O': 0.132, 'C4H6N2': 0.008, 'C3H6O2': 0.138, 'sum3isos_C6H12': 0.26, 'CO': 458.0, 'C6H8N2': 0.028, 'C9H18': 0.05, 'C3H4O': 0.944, 'isomer2_C5H6N2': 0.022, 'C9H10': 0.036, 'C10H14': 0.01, 'C3H4O3': 0.09, 'CO2': 2816.0, 'C10H10': 0.03, 'PM10': 77.88, 'C10H12': 0.06, 'CH3CN': 0.812, 'C5H8O2': 0.14, 'isomer3_C5H6N2': 0.012, 'C3H3N': 0.054, 'C6H5CH3': 1.158, 'C5H6O': 1.292, 'C7H12': 0.038, 'MVK_C4H6O': 0.388, 'PM2.5': 66.0, 'C11': 0.548, 'C9H20': 0.068, 'C10H20': 0.072, 'C10H22': 0.054, 'C8H6': 0.144, 'C8H8': 0.128, 'C9H8': 0.08, 'C4H10O': 0.408, 'C10H8': 1.29, 'C9H16': 0.014, 'C4H8': 0.178, 'C5H6': 0.01, 'C5H8': 0.014, 'C4H2': 0.004, 'C4H4': 0.014, 'C4H6': 0.016, 'C4H4O': 1.71, 'C2H2': 0.414, 'C5H10O2': 0.07, 'NH3': 0.96, 'isomer2_C10H14': 0.02, 'isomer1_C6H8': 0.038, 'isomer2_C6H10': 0.004, 'isomer4': 0.872}}

Or, get specifically the flaming/smoldering rx EF's

    >>> lu.get(4, 'flame_smold_rx')
    {'CH3CH2OH': 0.478, 'CH3COOH': 6.04, 'CH3OH': 5.03, 'C2H8N2': 0.064, 'isomer2_C9H8O': 0.046, 'isomer2_C6H8': 0.02, 'C3H4': 0.066, 'C9H12': 0.03, 'C5H8O': 0.016, 'CH4': 9.72, 'C5H10O': 0.06, 'isomer2_C7H8': 0.0, 'C6H8O': 0.072, 'C5H7N': 0.008, 'C7H14': 0.008, 'C7H16': 0.052, 'isomer1_C5H6N2': 0.028, 'C4H10': 0.252, 'C10H16': 0.012, 'isomer3_C6H10': 0.004, 'C4H6O': 0.002, 'HCOOH': 0.368, 'C4H8O2': 0.01, 'C3H4O2': 0.094, 'C6H12': 0.042, 'C6H10': 0.03, 'HCHO': 4.47, 'isomer1_C10H14': 0.018, 'C2H4O2': 0.044, 'C2H4O3': 0.092, 'isomer1_C7H8': 0.004, 'C3H8': 0.484, 'C6H14': 0.01, 'isomer4_C9H8O': 0.0, 'C11H22': 0.046, 'NMOC': 53.95, 'C5H12': 0.11, 'C5H10': 0.06, 'isomer1_C6H10': 0.022, 'C15H24': 0.164, 'isomer5_C6H10': 0.01, 'C11H24': 0.05, 'C4H8O': 0.0, 'C3H6O': 0.288, 'C8H14': 0.058, 'C8H16': 0.092, 'NOx': 4.12, 'C8H10': 0.1, 'C2H6': 1.33, 'CH3CHO': 2.238, 'C2H4': 2.762, 'HCN': 1.53, 'C6H5OH': 1.6, 'C6H8': 0.008, 'C7H6O': 0.548, 'C6H6': 0.006, 'SO2': 2.12, 'C4H6O2': 0.006, 'C8H6O': 0.27, 'C3H6': 1.446, 'HNCO': 0.294, 'isomer1_C9H8O': 0.026, 'MEK_C4H8O': 0.35, 'C4H5N': 0.02, 'C5H4O2': 0.024, 'C3H5N': 0.024, 'C6H12O': 0.024, 'C7H5N': 0.124, 'C6H6O2': 3.294, 'C8H18': 0.046, 'isomer3_C9H8O': 0.066, 'C4H6N2': 0.004, 'C3H6O2': 0.348, 'sum3isos_C6H12': 0.132, 'CO': 210.0, 'C6H8N2': 0.014, 'C9H18': 0.026, 'C3H4O': 0.684, 'isomer2_C5H6N2': 0.012, 'C9H10': 0.018, 'C10H14': 0.006, 'C3H4O3': 0.046, 'CO2': 3196.0, 'C10H10': 0.016, 'PM10': 41.4652, 'C10H12': 0.03, 'CH3CN': 0.43, 'C5H8O2': 0.07, 'isomer3_C5H6N2': 0.006, 'C3H3N': 0.068, 'C6H5CH3': 0.458, 'C5H6O': 0.022, 'C7H12': 0.02, 'MVK_C4H6O': 0.618, 'PM2.5': 35.14, 'C11': 0.276, 'C9H20': 0.028, 'C10H20': 0.036, 'C10H22': 0.028, 'C8H6': 0.012, 'C8H8': 0.138, 'C9H8': 0.04, 'C4H10O': 0.206, 'C10H8': 0.65, 'C9H16': 0.006, 'C4H8': 0.076, 'C5H6': 0.006, 'C5H8': 0.006, 'C4H2': 0.002, 'C4H4': 0.006, 'C4H6': 0.008, 'C4H4O': 0.98, 'C2H2': 0.624, 'C5H10O2': 0.034, 'NH3': 3.06, 'isomer2_C10H14': 0.01, 'isomer1_C6H8': 0.02, 'isomer2_C6H10': 0.002, 'isomer4': 0.438}

Or, get an EF for a specific species:

    >>> lu.get(4, 'flame_smold_rx', 'CO2')
    3196.0

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
keys, whereas 'get' returns None if any of the arguments are invalid.  For example:

    >>> lu.get(4,'flame_smold_rsdfsdfx')
    >>> lu[4]['flame_smold_rsdfsdfx']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'flame_smold_rsdfsdfx'

### Using the Executables

There are two scripts to choose from, again depending on whether you're
keying off of FCCS id or cover type - ./bin/fccs2ef and ./bin/ct2ef.  The
following example illustrates use of ./bin/fccs2ef, but as with the classes
described above, the usage of ./bin/ct2ef is identical other than passing
in a cover type id instead of an FCCS id.

To see the script's usage, you can use the '-h' options:

    ./bin/fccs2ef -h

The script takes an FCCS id and returns JSON formatted data containing the EFs
for that fuelbed. For example, to get all EF's associated with FCCS fuelbed 10:

    $ ./bin/fccs2ef 10
    {"10": {"duff_rsc": {"CH3CH2OH": 0.99, "CH3COOH": 14.799, "CH3OH": 9.355, "C2H8N2": 0.0, "isomer2_C9H8O": 0.076, "isomer2_C6H8": 0.062, "C3H4": 0.084, "C9H12": 0.042, "C5H8O": 0.046, "CH4": 15.89, "C5H10O": 0.13, "isomer2_C7H8": 0.004, "C6H8O": 0.152, "C5H7N": 0.03, "C7H14": 0.018, "C7H16": 0.096, "isomer1_C5H6N2": 0.088, "C4H10": 0.958, "C10H16": 0.004, "isomer3_C6H10": 0.032, "C4H6O": 0.0, "HCOOH": 2.189, "C4H8O2": 0.004, "C3H4O2": 0.306, "C6H12": 0.01, "C6H10": 0.03, "HCHO": 4.953, "isomer1_C10H14": 0.006, "C2H4O2": 0.098, "C2H4O3": 0.18, "isomer1_C7H8": 0.01, "C3H8": 1.594, "C6H14": 0.028, "isomer4_C9H8O": 0.0, "C11H22": 0.072, "NMOC": 123.391, "C5H12": 0.424, "C5H10": 0.054, "isomer1_C6H10": 0.002, "C15H24": 0.19, "isomer5_C6H10": 0.008, "C11H24": 0.086, "C4H8O": 0.012, "C3H6O": 0.706, "C8H14": 0.1, "C8H16": 0.174, "NOx": 1.34, "C8H10": 0.202, "C2H6": 4.24, "CH3CHO": 5.4, "C2H4": 2.929, "HCN": 3.976, "C6H5OH": 5.281, "C6H8": 0.042, "C7H6O": 1.166, "C6H6": 0.032, "SO2": 3.52, "C4H6O2": 0.032, "C8H6O": 1.816, "C3H6": 3.581, "HNCO": 0.542, "isomer1_C9H8O": 0.048, "MEK_C4H8O": 0.844, "C4H5N": 0.102, "C5H4O2": 0.038, "C3H5N": 0.048, "C6H12O": 0.02, "C7H5N": 0.202, "C6H6O2": 5.38, "C8H18": 0.078, "isomer3_C9H8O": 0.104, "C4H6N2": 0.056, "C3H6O2": 0.554, "sum3isos_C6H12": 0.02, "CO": 514.0, "C6H8N2": 0.042, "C9H18": 0.046, "C3H4O": 1.18, "isomer2_C5H6N2": 0.018, "C9H10": 0.026, "C10H14": 0.004, "C3H4O3": 0.538, "CO2": 2742.0, "C10H10": 0.014, "PM10": 83.308, "C10H12": 0.01, "CH3CN": 1.478, "C5H8O2": 0.152, "isomer3_C5H6N2": 0.0, "C3H3N": 0.302, "C6H5CH3": 0.976, "C5H6O": 1.074, "C7H12": 0.02, "MVK_C4H6O": 0.842, "PM2.5": 70.6, "C11": 0.456, "C9H20": 0.046, "C10H20": 0.044, "C10H22": 0.054, "C8H6": 0.086, "C8H8": 0.234, "C9H8": 0.102, "C4H10O": 2.36, "C10H8": 1.63, "C9H16": 0.0, "C4H8": 0.196, "C5H6": 0.024, "C5H8": 0.024, "C4H2": 0.018, "C4H4": 0.036, "C4H6": 0.028, "C4H4O": 2.53, "C2H2": 0.314, "C5H10O2": 0.008, "NH3": 5.34, "isomer2_C10H14": 0.004, "isomer1_C6H8": 0.056, "isomer2_C6H10": 0.008, "isomer4": 0.016}, "flame_smold_rx": {"CH3CH2OH": 0.478, "CH3COOH": 6.04, "CH3OH": 5.03, "C2H8N2": 0.064, "isomer2_C9H8O": 0.046, "isomer2_C6H8": 0.02, "C3H4": 0.066, "C9H12": 0.03, "C5H8O": 0.016, "CH4": 9.72, "C5H10O": 0.06, "isomer2_C7H8": 0.0, "C6H8O": 0.072, "C5H7N": 0.008, "C7H14": 0.008, "C7H16": 0.052, "isomer1_C5H6N2": 0.028, "C4H10": 0.252, "C10H16": 0.012, "isomer3_C6H10": 0.004, "C4H6O": 0.002, "HCOOH": 0.368, "C4H8O2": 0.01, "C3H4O2": 0.094, "C6H12": 0.042, "C6H10": 0.03, "HCHO": 4.47, "isomer1_C10H14": 0.018, "C2H4O2": 0.044, "C2H4O3": 0.092, "isomer1_C7H8": 0.004, "C3H8": 0.484, "C6H14": 0.01, "isomer4_C9H8O": 0.0, "C11H22": 0.046, "NMOC": 53.95, "C5H12": 0.11, "C5H10": 0.06, "isomer1_C6H10": 0.022, "C15H24": 0.164, "isomer5_C6H10": 0.01, "C11H24": 0.05, "C4H8O": 0.0, "C3H6O": 0.288, "C8H14": 0.058, "C8H16": 0.092, "NOx": 4.12, "C8H10": 0.1, "C2H6": 1.33, "CH3CHO": 2.238, "C2H4": 2.762, "HCN": 1.53, "C6H5OH": 1.6, "C6H8": 0.008, "C7H6O": 0.548, "C6H6": 0.006, "SO2": 2.12, "C4H6O2": 0.006, "C8H6O": 0.27, "C3H6": 1.446, "HNCO": 0.294, "isomer1_C9H8O": 0.026, "MEK_C4H8O": 0.35, "C4H5N": 0.02, "C5H4O2": 0.024, "C3H5N": 0.024, "C6H12O": 0.024, "C7H5N": 0.124, "C6H6O2": 3.294, "C8H18": 0.046, "isomer3_C9H8O": 0.066, "C4H6N2": 0.004, "C3H6O2": 0.348, "sum3isos_C6H12": 0.132, "CO": 210.0, "C6H8N2": 0.014, "C9H18": 0.026, "C3H4O": 0.684, "isomer2_C5H6N2": 0.012, "C9H10": 0.018, "C10H14": 0.006, "C3H4O3": 0.046, "CO2": 3196.0, "C10H10": 0.016, "PM10": 41.4652, "C10H12": 0.03, "CH3CN": 0.43, "C5H8O2": 0.07, "isomer3_C5H6N2": 0.006, "C3H3N": 0.068, "C6H5CH3": 0.458, "C5H6O": 0.022, "C7H12": 0.02, "MVK_C4H6O": 0.618, "PM2.5": 35.14, "C11": 0.276, "C9H20": 0.028, "C10H20": 0.036, "C10H22": 0.028, "C8H6": 0.012, "C8H8": 0.138, "C9H8": 0.04, "C4H10O": 0.206, "C10H8": 0.65, "C9H16": 0.006, "C4H8": 0.076, "C5H6": 0.006, "C5H8": 0.006, "C4H2": 0.002, "C4H4": 0.006, "C4H6": 0.008, "C4H4O": 0.98, "C2H2": 0.624, "C5H10O2": 0.034, "NH3": 3.06, "isomer2_C10H14": 0.01, "isomer1_C6H8": 0.02, "isomer2_C6H10": 0.002, "isomer4": 0.438}, "flame_smold_wf": {"CH3CH2OH": 0.64, "CH3COOH": 8.922, "CH3OH": 4.122, "C2H8N2": 0.086, "isomer2_C9H8O": 0.062, "isomer2_C6H8": 0.026, "C3H4": 0.088, "C9H12": 0.04, "C5H8O": 0.022, "CH4": 14.64, "C5H10O": 0.08, "isomer2_C7H8": 0.0, "C6H8O": 0.096, "C5H7N": 0.01, "C7H14": 0.012, "C7H16": 0.07, "isomer1_C5H6N2": 0.038, "C4H10": 0.336, "C10H16": 0.016, "isomer3_C6H10": 0.004, "C4H6O": 0.004, "HCOOH": 1.01, "C4H8O2": 0.014, "C3H4O2": 0.124, "C6H12": 0.056, "C6H10": 0.042, "HCHO": 4.496, "isomer1_C10H14": 0.024, "C2H4O2": 0.06, "C2H4O3": 0.122, "isomer1_C7H8": 0.004, "C3H8": 1.018, "C6H14": 0.014, "isomer4_C9H8O": 0.0, "C11H22": 0.06, "NMOC": 67.748, "C5H12": 0.148, "C5H10": 0.08, "isomer1_C6H10": 0.028, "C15H24": 0.22, "isomer5_C6H10": 0.012, "C11H24": 0.068, "C4H8O": 0.002, "C3H6O": 0.386, "C8H14": 0.078, "C8H16": 0.122, "NOx": 4.0, "C8H10": 0.136, "C2H6": 2.154, "CH3CHO": 3.0, "C2H4": 3.65, "HCN": 1.08, "C6H5OH": 1.73, "C6H8": 0.01, "C7H6O": 0.734, "C6H6": 0.006, "SO2": 2.12, "C4H6O2": 0.008, "C8H6O": 0.362, "C3H6": 1.396, "HNCO": 0.396, "isomer1_C9H8O": 0.036, "MEK_C4H8O": 0.468, "C4H5N": 0.028, "C5H4O2": 0.032, "C3H5N": 0.032, "C6H12O": 0.032, "C7H5N": 0.168, "C6H6O2": 4.412, "C8H18": 0.062, "isomer3_C9H8O": 0.088, "C4H6N2": 0.006, "C3H6O2": 0.468, "sum3isos_C6H12": 0.176, "CO": 270.0, "C6H8N2": 0.02, "C9H18": 0.034, "C3H4O": 0.916, "isomer2_C5H6N2": 0.016, "C9H10": 0.024, "C10H14": 0.008, "C3H4O3": 0.06, "CO2": 3200.0, "C10H10": 0.02, "PM10": 54.752, "C10H12": 0.04, "CH3CN": 0.578, "C5H8O2": 0.094, "isomer3_C5H6N2": 0.008, "C3H3N": 0.09, "C6H5CH3": 0.614, "C5H6O": 0.03, "C7H12": 0.026, "MVK_C4H6O": 0.828, "PM2.5": 46.4, "C11": 0.368, "C9H20": 0.038, "C10H20": 0.048, "C10H22": 0.036, "C8H6": 0.016, "C8H8": 0.186, "C9H8": 0.054, "C4H10O": 0.276, "C10H8": 0.87, "C9H16": 0.008, "C4H8": 0.1, "C5H6": 0.008, "C5H8": 0.01, "C4H2": 0.002, "C4H4": 0.008, "C4H6": 0.01, "C4H4O": 0.966, "C2H2": 0.752, "C5H10O2": 0.046, "NH3": 3.0, "isomer2_C10H14": 0.014, "isomer1_C6H8": 0.026, "isomer2_C6H10": 0.002, "isomer4": 0.588}, "woody_rsc": {"CH3CH2OH": 0.038, "CH3COOH": 3.674, "CH3OH": 7.034, "C2H8N2": 0.126, "isomer2_C9H8O": 0.092, "isomer2_C6H8": 0.038, "C3H4": 0.038, "C9H12": 0.05, "C5H8O": 0.48, "CH4": 27.88, "C5H10O": 0.12, "isomer2_C7H8": 0.002, "C6H8O": 0.388, "C5H7N": 0.016, "C7H14": 0.018, "C7H16": 0.086, "isomer1_C5H6N2": 0.056, "C4H10": 0.39, "C10H16": 0.022, "isomer3_C6H10": 0.008, "C4H6O": 0.006, "HCOOH": 0.0, "C4H8O2": 0.02, "C3H4O2": 0.186, "C6H12": 0.082, "C6H10": 0.062, "HCHO": 4.248, "isomer1_C10H14": 0.036, "C2H4O2": 0.088, "C2H4O3": 0.182, "isomer1_C7H8": 0.006, "C3H8": 1.604, "C6H14": 0.022, "isomer4_C9H8O": 0.0, "C11H22": 0.09, "NMOC": 90.35, "C5H12": 0.19, "C5H10": 0.144, "isomer1_C6H10": 0.042, "C15H24": 0.19, "isomer5_C6H10": 0.018, "C11H24": 0.1, "C4H8O": 0.002, "C3H6O": 0.572, "C8H14": 0.114, "C8H16": 0.132, "NOx": 0.0, "C8H10": 0.144, "C2H6": 5.446, "CH3CHO": 3.092, "C2H4": 2.796, "HCN": 1.446, "C6H5OH": 0.3, "C6H8": 0.016, "C7H6O": 1.088, "C6H6": 0.01, "SO2": 0.0, "C4H6O2": 0.01, "C8H6O": 0.536, "C3H6": 2.12, "HNCO": 0.586, "isomer1_C9H8O": 0.054, "MEK_C4H8O": 0.646, "C4H5N": 0.042, "C5H4O2": 0.046, "C3H5N": 0.046, "C6H12O": 0.046, "C7H5N": 0.248, "C6H6O2": 6.546, "C8H18": 0.072, "isomer3_C9H8O": 0.132, "C4H6N2": 0.008, "C3H6O2": 0.138, "sum3isos_C6H12": 0.26, "CO": 458.0, "C6H8N2": 0.028, "C9H18": 0.05, "C3H4O": 0.944, "isomer2_C5H6N2": 0.022, "C9H10": 0.036, "C10H14": 0.01, "C3H4O3": 0.09, "CO2": 2816.0, "C10H10": 0.03, "PM10": 77.88, "C10H12": 0.06, "CH3CN": 0.812, "C5H8O2": 0.14, "isomer3_C5H6N2": 0.012, "C3H3N": 0.054, "C6H5CH3": 1.158, "C5H6O": 1.292, "C7H12": 0.038, "MVK_C4H6O": 0.388, "PM2.5": 66.0, "C11": 0.548, "C9H20": 0.068, "C10H20": 0.072, "C10H22": 0.054, "C8H6": 0.144, "C8H8": 0.128, "C9H8": 0.08, "C4H10O": 0.408, "C10H8": 1.29, "C9H16": 0.014, "C4H8": 0.178, "C5H6": 0.01, "C5H8": 0.014, "C4H2": 0.004, "C4H4": 0.014, "C4H6": 0.016, "C4H4O": 1.71, "C2H2": 0.414, "C5H10O2": 0.07, "NH3": 0.96, "isomer2_C10H14": 0.02, "isomer1_C6H8": 0.038, "isomer2_C6H10": 0.004, "isomer4": 0.872}}}

You can optionally specify a particular set of EF's.  For example, to
specifically get the flaming/smoldering rx EF's:

    $ ./bin/fccs2ef 10 -e flame_smold_rx
    {"10": {"flame_smold_rx": {"CH3CH2OH": 0.478, "CH3COOH": 6.04, "CH3OH": 5.03, "C2H8N2": 0.064, "isomer2_C9H8O": 0.046, "isomer2_C6H8": 0.02, "C3H4": 0.066, "C9H12": 0.03, "C5H8O": 0.016, "CH4": 9.72, "C5H10O": 0.06, "isomer2_C7H8": 0.0, "C6H8O": 0.072, "C5H7N": 0.008, "C7H14": 0.008, "C7H16": 0.052, "isomer1_C5H6N2": 0.028, "C4H10": 0.252, "C10H16": 0.012, "isomer3_C6H10": 0.004, "C4H6O": 0.002, "HCOOH": 0.368, "C4H8O2": 0.01, "C3H4O2": 0.094, "C6H12": 0.042, "C6H10": 0.03, "HCHO": 4.47, "isomer1_C10H14": 0.018, "C2H4O2": 0.044, "C2H4O3": 0.092, "isomer1_C7H8": 0.004, "C3H8": 0.484, "C6H14": 0.01, "isomer4_C9H8O": 0.0, "C11H22": 0.046, "NMOC": 53.95, "C5H12": 0.11, "C5H10": 0.06, "isomer1_C6H10": 0.022, "C15H24": 0.164, "isomer5_C6H10": 0.01, "C11H24": 0.05, "C4H8O": 0.0, "C3H6O": 0.288, "C8H14": 0.058, "C8H16": 0.092, "NOx": 4.12, "C8H10": 0.1, "C2H6": 1.33, "CH3CHO": 2.238, "C2H4": 2.762, "HCN": 1.53, "C6H5OH": 1.6, "C6H8": 0.008, "C7H6O": 0.548, "C6H6": 0.006, "SO2": 2.12, "C4H6O2": 0.006, "C8H6O": 0.27, "C3H6": 1.446, "HNCO": 0.294, "isomer1_C9H8O": 0.026, "MEK_C4H8O": 0.35, "C4H5N": 0.02, "C5H4O2": 0.024, "C3H5N": 0.024, "C6H12O": 0.024, "C7H5N": 0.124, "C6H6O2": 3.294, "C8H18": 0.046, "isomer3_C9H8O": 0.066, "C4H6N2": 0.004, "C3H6O2": 0.348, "sum3isos_C6H12": 0.132, "CO": 210.0, "C6H8N2": 0.014, "C9H18": 0.026, "C3H4O": 0.684, "isomer2_C5H6N2": 0.012, "C9H10": 0.018, "C10H14": 0.006, "C3H4O3": 0.046, "CO2": 3196.0, "C10H10": 0.016, "PM10": 41.4652, "C10H12": 0.03, "CH3CN": 0.43, "C5H8O2": 0.07, "isomer3_C5H6N2": 0.006, "C3H3N": 0.068, "C6H5CH3": 0.458, "C5H6O": 0.022, "C7H12": 0.02, "MVK_C4H6O": 0.618, "PM2.5": 35.14, "C11": 0.276, "C9H20": 0.028, "C10H20": 0.036, "C10H22": 0.028, "C8H6": 0.012, "C8H8": 0.138, "C9H8": 0.04, "C4H10O": 0.206, "C10H8": 0.65, "C9H16": 0.006, "C4H8": 0.076, "C5H6": 0.006, "C5H8": 0.006, "C4H2": 0.002, "C4H4": 0.006, "C4H6": 0.008, "C4H4O": 0.98, "C2H2": 0.624, "C5H10O2": 0.034, "NH3": 3.06, "isomer2_C10H14": 0.01, "isomer1_C6H8": 0.02, "isomer2_C6H10": 0.002, "isomer4": 0.438}}}

You can then optionally specify a particular emissions species. For example,
to get the EF for flaming/smoldering rx CO2:

    $ /bin/fccs2ef 10 -e flame_smold_rx -s CO2
    {"10": {"flame_smold_rx": {"CO2": 3196.0}}}

Note that, when using the script, the resulting JSON data's nested depth is the
same regardless of the input specificity.  The format is always like the following:

    {
        <FCCS_ID>: {
            <EF_SET_ID>: {
                <SPECIES>: ...
            }
        }
    }


### Invoking the Executables In Perl

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
    my $j = `./bin/fccs2ef.py 13`;
    my $p = decode_json($j);

At this point ```$p``` should be a perl hash object, and you should be able
to do something like:

    print Dumper($p{"flame_smold_rx"}{"CH4"})
    ...

(Note:  I [Joel], couldn't get decode_json to work on my Mac, so take
the above code with a grain of salt.)
