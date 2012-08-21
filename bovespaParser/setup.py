#!/usr/bin/python
# Filename: setup.py


import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="bovespaparser",
    version="0.2",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    author="Roberto Haddock Lobo",
    author_email="rhlobo+stockexperiments@gmail.com",
    description="Bovespa's historical series files parser.",
    long_description=read('README'),
    license="PSF",
    keywords="bovespa parser historical series cotahist stock",
    test_suite='bovespaparser.tests.bovespaparser_tests.TestBovespaParserFunctions',
)
