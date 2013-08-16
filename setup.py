#!/usr/bin/env python
# Filename: setup.py


import os
import sys
from pkgutil import walk_packages

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def find_packages(path=__path__, prefix=""):
    yield prefix
    prefix = prefix + "."
    for _, name, ispkg in walk_packages(path, prefix):
        if ispkg:
            yield name


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


import bigtempo


setup(
    name='bigtmepo',
    version=bigtempo.__version__,
    description='Powerful processment of temporal data.',
    long_description=read('README.md'),
    author='Roberto Haddock Lobo',
    author_email='rhlobo+bigtempo@gmail.com',
    #url='http://',
    packages=list(find_packages(bigtempo.__path__, bigtempo.__name__)),
    package_data={'': ['LICENSE']},
    package_dir={'bigtempo': 'bigtempo'},
    include_package_data=True,
    install_requires=[],
    license=read('LICENSE'),
    zip_safe=False,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
