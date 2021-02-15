#!/bin/env bash

repo="https://github.com/Fitzy1293/daily-covid"


# Update github repo with new figures
rm output-counties/*
echo -e "\n${purple}\nUpdating README.md figures...${white}"
python3 test_pkg.py --plot -sc "ca-los angeles" "ny-new york city" "ma-suffolk" >> publish.log
mv output-counties/*.png examples

echo -e "${green}Updated README.md figures locally\n${purple}\nPushing to ${repo}\n"
git add examples/*
git commit -m "Examples update" && git push origin -u master
