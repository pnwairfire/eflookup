from distutils.core import setup
from pip.req import parse_requirements

REQUIREMENTS = [str(ir.req) for ir in parse_requirements('requirements.txt')]

setup(
    name='fccs2ef',
    version='0.2.2',
    author='Joel Dubowy',
    author_email='jdubowy@gmail.com',
    packages=[
        'fccs2ef'
    ],
    scripts=[
        'bin/fccs2ef',
        'bin/import-fccs2ef'
    ],
    package_data={
        'fccs2ef': ['data/*.csv']
    },
    url='git@bitbucket.org:fera/airfire-fccs2ef.git',
    description='Package supporting lookup of emissions factors by FCCS fuel bed or cover type.',
    install_requires=REQUIREMENTS,
)
