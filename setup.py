#!/usr/bin/env python
# Filename: setup.py


import os
import re
import sys
import bigtempo
from pkgutil import walk_packages


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


def packages(path=None, prefix="", exclude=None):
    try:
        return find_packages(exclude=exclude)
    except:
        return [name for _, name, ispkg in walk_packages(path, prefix) if ispkg]


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


def filter_comments(contents):
    filter_pattern = re.compile(r'[\s]*#.*')
    return filter(lambda x: not filter_pattern.match(x), contents)


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name='bigtempo',
    version=bigtempo.__version__,
    description='Powerful processment of temporal data.',
    long_description=read('README.md'),
    license=read('LICENSE'),

    author='Roberto Haddock Lobo',
    author_email='rhlobo+bigtempo@gmail.com',
    url='https://github.com/rhlobo/bigtempo',

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
    ),

    install_requires=filter_comments(read('requirements.txt').split('\n')),
    package_data={'': ['README.md', 'LICENSE', 'requirements.txt']},
    package_dir={'bigtempo': 'bigtempo'},
    packages=packages(bigtempo.__path__,
                      bigtempo.__name__,
                      exclude=["*.tests",
                               "*.tests.*",
                               "tests.*",
                               "tests"]),

    include_package_data=True,
    zip_safe=False
)
