from setuptools import setup, find_packages

from eflookup import __version__

test_requirements = []
with open('requirements-test.txt') as f:
    test_requirements = [r for r in f.read().splitlines()]

setup(
    name='eflookup',
    version=__version__,
    author='Joel Dubowy',
    license='GPLv3+',
    author_email='jdubowy@gmail.com',
    packages=find_packages(),
    scripts=[
        'bin/fccs2ef',
        'bin/ct2ef'
    ],
    package_data={
        'fccs2ef': ['data/*.csv']
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 2",
        "Operating System :: POSIX",
        "Operating System :: MacOS"
    ],
    url='https://github.com/pnwairfire/eflookup/',
    description='Package supporting the look-up of emissions factors used to compute emissions from wildland fires.',
    install_requires=[
        "pyairfire>=1.1.1",
    ],
    dependency_links=[
        "https://pypi.smoke.airfire.org/simple/pyairfire/"
    ],
    tests_require=test_requirements
)
