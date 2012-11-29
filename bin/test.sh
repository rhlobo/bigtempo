#!/bin/bash
CURRDIR="$(pwd)"
cd "${PROJECT_HOME}/stockExperiments"
nosetests -v --with-coverage --cover-erase --cover-package=stockExperiments --cover-inclusive --cover-branches --cover-html -w stockExperiments
find . -type f -name "*.pyc" -exec rm -f {} \;
cd "${CURRDIR}"
