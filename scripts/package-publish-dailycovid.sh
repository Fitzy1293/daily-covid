#!/bin/env bash

repo="https://github.com/Fitzy1293/daily-covid"

# 10 MB lim on gifs for pypi.org
grep -v ex.gif README.md > README-pip.md

./pypi-build

# Update github repo with new figures
rm output-counties/*
echo -e "\n${purple}\nUpdating README.md figures...${white}"
python3 test_pkg.py --plot -sc "ca-los angeles" "ny-new york city" "ma-suffolk" >> publish.log
mv output-counties/*.png examples

exit 0
