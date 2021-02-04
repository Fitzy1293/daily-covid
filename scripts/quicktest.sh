#!/bin/env bash
clear
outputDir="output-counties"

for i in "$@" ; do
    if [[ $i == "fresh" || $i == "f" ]] ; then
        rm "${outputDir}" -rf us-counties.csv info-by-state/
        break
    fi
done

time (python3 ./scripts/test_pkg.py -sc MA-Berkshire)
echo
head ${outputDir}/data_BERKSHIRE_MA.csv | grep '20'
echo

tail ${outputDir}/data_BERKSHIRE_MA.csv | grep '20'
