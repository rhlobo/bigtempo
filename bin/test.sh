#!/bin/bash
CURRDIR="$(pwd)"
TESTTYPE=${1:-full}
export TESTTYPE
cd "${PROJECT_HOME}/stockExperiments"


echo
echo "TESTS"
echo "--------------------------------------------------------------------------------"
nosetests -v --with-coverage --cover-erase --cover-inclusive --cover-branches --cover-package=stockExperiments --cover-html --cover-html-dir="../coverage/" -w stockExperiments
echo
echo
echo "PEP8 CODE STYLE CHECK"
echo "--------------------------------------------------------------------------------"
find "stockExperiments" -type f -name "*.py" -exec pep8 --first --max-line-length=160 {} \;
echo
echo "#     Err  Description"
echo "--------------------------------------------------------------------------------"
pep8 --statistics --max-line-length=160 -qq "./stockExperiments" | sort -nr
echo

find . -type f -name "*.pyc" -exec rm -f {} \;
cd "${CURRDIR}"
