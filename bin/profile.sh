#!/bin/bash

profile() {
	local PSTATSFILE IMGFILE
	PSTATSFILE="profile/profile.pstats"
	IMGFILE="profile/profile.png"
	#IMGFILE="profile/profile_$(date +%F_%T | sed 's/[\s:]//g').png"

	mkdir -p "profile"
	python -m cProfile -s cumulative -o "${PSTATSFILE}" stockExperiments/experiments.py
	python bin/util/gprof2dot.py -f pstats "${PSTATSFILE}" | dot -Tpng -o "${IMGFILE}"
	python bin/util/displayprofilestats.py "${PSTATSFILE}"
}

CURRDIR="$(pwd)"
cd "${PROJECT_HOME}/stockExperiments"
profile
find . -type f -name "*.pyc" -exec rm -f {} \;
cd "${CURRDIR}"
