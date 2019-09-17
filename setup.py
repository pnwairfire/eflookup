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
        'bin/fccs2seraef',
        'bin/ct2ef',
        'bin/fepsef',
    ],
    package_data={
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Operating System :: POSIX",
        "Operating System :: MacOS"
    ],
    url='https://github.com/pnwairfire/eflookup/',
    description='Package supporting the look-up of emissions factors used to compute emissions from wildland fires.',
    install_requires=[
        "afscripting>=1.1.2,<2.0.0",
    ],
    dependency_links=[
        "https://pypi.airfire.org/simple/afscripting/"
    ],
    tests_require=test_requirements
)
