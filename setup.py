#!/usr/bin/env python
# Filename: setup.py


import os
import sys
import bigtempo
from pkgutil import walk_packages


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def packages(path=None, prefix="", excludes=None):
    try:
        return find_packages(excludes=excludes)
    except:
        return [name for _, name, ispkg in walk_packages(path, prefix) if ispkg]


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name='bigtmepo',
    version=bigtempo.__version__,
    description='Powerful processment of temporal data.',
    long_description=read('README.md'),
    license=read('LICENSE'),

    #url='http://',
    author='Roberto Haddock Lobo',
    author_email='rhlobo+bigtempo@gmail.com',

    install_requires=[],
    zip_safe=False,

    package_dir={'bigtempo': 'bigtempo'},
    packages=packages(bigtempo.__path__,
                      bigtempo.__name__,
                      exclude=["*.tests",
                               "*.tests.*",
                               "tests.*",
                               "tests"]),
    include_package_data=True,
    package_data={'': ['LICENSE', 'requirements.txt']},

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
