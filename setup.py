#!/usr/bin/python
# Filename: setup.py


from setuptools import setup, find_packages
import os


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name="stockExperiments",
    version="0.1",
    packages=find_packages(exclude=["*.tests",
                                    "*.tests.*",
                                    "tests.*",
                                    "tests"]),
    author="Roberto Haddock Lobo",
    author_email="rhlobo+stockexperiments@gmail.com",
    description="Stock Experiments",
    long_description=read('README.md'),
    license="MIT",
    #test_suite='stockExperiments.tests.testSuite.TestStockExperiments',
    #url='http://pypi.python.org/pypi/stockExperiments',
    keywords=["investment", "financial", "stock"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
