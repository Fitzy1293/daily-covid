#!/bin/env bash
clear
outputDir="output-counties/"

for i in "$@" ; do
    if [[ $i == "fresh" || $i == "f" ]] ; then
        rm "${outputDir}" -rf us-counties.csv info-by-state/
        break
    fi
done


time (python3 test_pkg.py -sc MA-Berkshire)
echo
head ./output-counties/data_BERKSHIRE_MA.csv | grep '20'
#xdg-open ./counties/plots_BERKSHIRE_MA.png
