from distutils.core import setup
from pip.req import parse_requirements

# Note: using pip.req.parse_requirements like so:
#  > REQUIREMENTS = [str(ir.req) for ir in parse_requirements('requirements.txt')]
# results in the folloing error on Heroku:
#    TypeError: parse_requirements() missing 1 required keyword argument: 'session'
with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name='fccs2ef',
    version='0.3.1',
    author='Joel Dubowy',
    author_email='jdubowy@gmail.com',
    packages=[
        'fccs2ef'
    ],
    scripts=[
        'bin/fccs2ef',
        'bin/ct2ef'
    ],
    package_data={
        'fccs2ef': ['data/*.csv']
    },
    url='git@github.com:pnwairfire/fccs2ef.git',
    description='Package supporting lookup of emissions factors by FCCS fuelbed or cover type.',
    install_requires=REQUIREMENTS,
)
