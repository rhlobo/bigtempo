#!/bin/bash
CURRDIR="$(pwd)"
cd "${PROJECT_HOME}/stockExperiments"
nosetests --with-coverage --cover-package=stockExperiments --cover-inclusive --cover-html --cover-html-dir=coverage -w stockExperiments -v
find . -type f -name "*.pyc" -exec rm -f {} \;
cd "${CURRDIR}"
