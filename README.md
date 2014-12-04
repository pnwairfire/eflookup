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

## TODO

- Unit tests!
