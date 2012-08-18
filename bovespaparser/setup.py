#!/usr/bin/python
# Filename: setup.py


from setuptools import setup, find_packages
setup(
    name="bovespaparser",
    version="0.1a",
    packages=find_packages(),
    scripts=['bovespaparser.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['docutils>=0.3'],

    package_data={
        '': ['*.txt'],
    },

    author="Roberto Haddock Lobo",
    author_email="rhlobo+python@gmail.com",
    description="Bovespa's historical series files parser.",
    # long_description
    license="PSF",
    keywords="bovespa parser historical series cotahist stock",
    # url = "http://example.com/HelloWorld/"
    # download_url
)
