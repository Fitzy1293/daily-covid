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

grep -v ex.gif README.md > README-pip.md


versionOnPypi="$(curl $pypiUrl -s | grep '<a class="card release__card" href="/project/dailycovid/' -m 1 | cut -d'/' -f4)"


echo -e "${cyan}Current pypi.org build:${green}"
echo $versionOnPypi
echo -e "${cyan}Enter a new poetry build version${white}"
read poetryVersion
sed "s/.*version =.*$/version = \"$poetryVersion\"/" pyproject.toml > new.toml
cp pyproject.toml backup_config.toml
cp new.toml pyproject.toml

rm ./output-counties/*
echo -e "${purple}Updating README.md figures...${white}"
python3 test_pkg.py -sc "$boston" > /dev/null \
&& python3 test_pkg.py -sc "$ny" > /dev/null \
&& python3 test_pkg.py -sc "$la" > /dev/null \
&& mv ./output-counties/*.png ./examples
echo -e "${green}Updated README.md figures${white}"


git add examples >> /dev/null
git commit -m "Examples update" > /dev/null && git push origin -u master

echo -e "\n${purple}Beginning poetry building and publishing \n"

poetry build
poetry publish

rm new.toml backup_config.toml
