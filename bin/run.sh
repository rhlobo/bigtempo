#!/bin/bash
CURRDIR="$(pwd)"
cd "${PROJECT_HOME}/stockExperiments"
python stockExperiments/experiments.py
find . -type f -name "*.pyc" -exec rm -f {} \;
cd "${CURRDIR}"
