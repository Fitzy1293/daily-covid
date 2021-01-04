#!/bin/env bash

la=$"ca-los angeles"
ny="ny-new york city"
boston="ma-suffolk"

green='\e[0;32m'
cyan='\e[0;36m'
red='\e[0;31m'
white='\e[0m'

echo -e "${cyan}Current pypi build:${green}"
grep "version = " pyproject.toml | head -n 1
echo -e "${cyan}Enter a new poetry build version${white}"
read poetryVersion
sed -e "s/.*version =.*$/version = \"$poetryVersion\"/" pyproject.toml > temp.toml

rm ./counties/*

python3 test_pkg.py -sc "$boston" > /dev/null
python3 test_pkg.py -sc "$ny" > /dev/null
python3 test_pkg.py -sc "$la" > /dev/null
mv ./counties/*.png ./examples
echo -e "${green}Updated README.md figures${white}"

git add examples
git commit -m "Examples update" > /dev/null && git push origin -u master

mv temp.toml pyproject.toml

poetry build
poetry publish
