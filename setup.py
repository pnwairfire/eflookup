import re
from setuptools import setup, find_packages

from fccs2ef import __version__

# Note: using pip.req.parse_requirements like so:
#  > REQUIREMENTS = [str(ir.req) for ir in parse_requirements('requirements.txt')]
# results in the folloing error on Heroku:
#    TypeError: parse_requirements() missing 1 required keyword argument: 'session'
git_url_matcher = re.compile('^git\+(.+)/([^/.]+)(\.git)?@v?([0-9.]+)$')
def parse_requirements(dep_links, req_file_name):
    with open(req_file_name) as f:
        reqs = []
        for r in f.read().splitlines():
            m = git_url_matcher.match(r)
            if m:
                # TODO: figure out how dep link should be formatted
                dep_links.append('%s/%s@v%s#egg=%s-%s' % (
                    m.group(1), m.group(2), m.group(4), m.group(2), m.group(4)))
                reqs.append("%s==%s" % (m.group(2), m.group(4)))
            else:
                reqs.append(r)
        return reqs

dependency_links = []
requirements = parse_requirements(dependency_links, 'requirements.txt')
test_requirements = parse_requirements(dependency_links, 'requirements-test.txt')

setup(
    name='fccs2ef',
    version=__version__,
    author='Joel Dubowy',
    license='MIT',
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
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Operating System :: POSIX",
        "Operating System :: MacOS"
    ],
    url='https://github.com/pnwairfire/fccs2ef/',
    description='Package supporting lookup of emissions factors by FCCS fuelbed or cover type.',
    install_requires=requirements,
    dependency_links=dependency_links,
    tests_require=test_requirements
)
