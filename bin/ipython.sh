#!/bin/bash

CURRDIR="$(pwd)"
export PYTHONPATH="${PROJECT_HOME}/stockExperiments/stockExperiments"
cd "${PYTHONPATH}/../ipy-notebooks"
ipython notebook --pylab inline
cd "${CURRDIR}"
