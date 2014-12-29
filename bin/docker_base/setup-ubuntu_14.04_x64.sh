#!/bin/bash -ve


## INSTALLING DEPENDENCIES
### MISC DEPS
sudo apt-get install --yes --quiet git wget

### C COMPILER
sudo apt-get install --yes --quiet build-essential

### PYTHON
sudo apt-get install --yes --quiet software-properties-common python-software-properties
sudo apt-get install --yes --quiet python python-dev python-setuptools python-pip

### SETUP TOOLS
pip install -U setuptools
#pip install -U pip

### TEST TOOLS
pip install -U pep8
pip install -U nose
pip install -U coverage
pip install -U mockito
pip install -U watchdog

### MISC TOOLING
pip install -U markupsafe

#### MEMORY PROFILER
pip install -U psutil
pip install -U memory_profiler

#### PROFILE VIZUALIZATION
##### GPROF2DOT
sudo apt-get install --yes --quiet graphviz
sudo apt-get install --yes --quiet python-profiler

#### DOCUMENTATION
pip install -U sphinx

### MISC PROJECT / SCIPY DEPENDENCIES
#pip install -U --install-option="--prefix=${VIRTUAL_ENV}" cython
pip install -U Cython
pip install -U pytz
pip install -U python-dateutil
pip install -U pyparsing

#### NUMPY
sudo apt-get install --yes --quiet libatlas-base-dev liblapack-dev
sudo apt-get install --yes --quiet libatlas3gf-sse2 || echo 'Skipping libatlas3gf-sse2'
mkdir -p "${VIRTUAL_ENV}/local"
rm -Rf "${VIRTUAL_ENV}/local/lib"
ln -s "${VIRTUAL_ENV}/lib" "${VIRTUAL_ENV}/local/lib"
pip install -U numpy

#### NUMPY COMPLEMENTARY PACKAGES
pip install -U bottleneck
pip install -U numexpr

#### SCIPY
sudo apt-get build-dep --yes --quiet python-scipy
pip install -U scipy
pip install -U sympy

#### HDF5 & PYTABLES
sudo apt-get install --yes --quiet libhdf5-7
sudo apt-get install --yes --quiet  libhdf5-serial-dev
sudo apt-get install --yes --quiet subversion
sudo apt-get build-dep --yes python-h5py
pip install -U h5py
pip install -e "git+https://github.com/PyTables/PyTables.git@v.3.0.0#egg=tables"

#### MATPLOTLIB
sudo apt-get build-dep --yes --quiet python-matplotlib
#sudo apt-get install --yes --quiet libfreetype6-dev libpng12-dev
pip install -U matplotlib

#### PANDAS & RELATED
pip install -U pandas
pip install -U patsy
pip install -U statsmodels

### IPYTHON (& DEPENDENCIES)
sudo apt-get install --yes --quiet libzmq-dev
pip install -U pyzmq
pip install -U jinja2
pip install -U tornado
pip install -U ipython
