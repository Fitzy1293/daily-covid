#!/bin/env bash

green='\e[0;32m'
cyan='\e[0;36m'
red='\e[0;31m'
white='\e[0m'
purple='\e[1;35m'

la=$"ca-los angeles"
ny="ny-new york city"
boston="ma-suffolk"

pypiUrl="https://pypi.org/project/dailycovid/"
repo="https://github.com/Fitzy1293/daily-covid"


grep -v ex.gif README.md > README-pip.md

versionOnPypi="$(curl $pypiUrl -s | grep '<a class="card release__card" href="/project/dailycovid/' -m 1 | cut -d'/' -f4)"

echo -e "${cyan}Current pypi.org build:${green}"
echo $versionOnPypi
echo -e "${cyan}Enter a new poetry build version${white}"
read poetryVersion

cp pyproject.toml backup_config.toml
sed "s/.*version =.*$/version = \"$poetryVersion\"/" pyproject.toml > new.toml
cp new.toml pyproject.toml

# Update github repo with new figures
rm ./output-counties/*
echo -e "${purple}\nUpdating README.md figures...${white}"
python3 test_pkg.py --plot -sc "$boston" "$ny" "$la" >> publish.log
mv output-counties/*.png examples

echo -e "${green}Updated README.md figures locally\n${purple}\nPushing to ${repo}${white}"

git add examples >> publish.log
git commit -m "Examples update" >> publish.log && git push origin -u master

echo -e "\n${purple}Beginning poetry building and publishing\n"

poetry build
poetry publish

rm new.toml backup_config.toml publish.log

exit 0
