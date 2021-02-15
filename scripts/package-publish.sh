#!/bin/env bash
repo="https://github.com/Fitzy1293/daily-covid"
la=$"ca-los angeles"
ny="ny-new york city"
boston="ma-suffolk"

./poetry-version-verify.sh

# Update github repo with new figures
rm output-counties/*
echo -e "\n${purple}\nUpdating README.md figures...${white}"
python3 test_pkg.py --plot -sc "$boston" "$ny" "$la" >> publish.log
mv output-counties/*.png examples

echo -e "${green}Updated README.md figures locally\n${purple}\nPushing to ${repo}${white}\n\n"
git add .
git commit -m "Examples update" && git push origin -u master

echo -e "\n${purple}Beginning poetry building and publishing\n"

poetry build
poetry publish

rm backup_config.toml

exit 0
