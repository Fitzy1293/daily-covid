#!/bin/env bash
repo="https://github.com/Fitzy1293/daily-covid"

rm publish.log && touch publish.log
grep -v ex.gif README.md > README-pip.md

green='\e[0;32m'
cyan='\e[0;36m'
red='\e[0;31m'
white='\e[0m'
purple='\e[1;35m'

la=$"ca-los angeles"
ny="ny-new york city"
boston="ma-suffolk"

package="dailycovid"
pypiUrl="https://pypi.org/project/${package}/"

versionOnPypi="$(curl ${pypiUrl} -s | grep "<a class=\"card release__card\" href=\"/project/${package}/" -m 1 | cut -d'/' -f4)"

echo -e "${cyan}Current ${package} pypi.org build:\n${green}${versionOnPypi}"
echo -e "${cyan}Enter a new version for pyproject.toml for building with poetry${white}"
read poetryVersion

cp pyproject.toml backup_config.toml
sed "s/.*version =.*$/version = \"$poetryVersion\"/" pyproject.toml > new.toml
cp new.toml pyproject.toml

# Update github repo with new figures
rm ./output-counties/*
echo -e "${purple}\nUpdating README.md figures...${white}"
python3 test_pkg.py --plot -sc "$boston" "$ny" "$la" >> publish.log
mv output-counties/*.png examples

echo -e "${green}Updated README.md figures locally\n${purple}\nPushing to ${repo}${white}\n\n"

git add .
git commit -m "Examples update" && git push origin -u master

echo -e "\n${purple}Beginning poetry building and publishing\n"

poetry build
poetry publish

rm new.toml backup_config.toml

exit 0
