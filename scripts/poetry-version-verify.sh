#!/bin/sh

green='\e[0;32m'
cyan='\e[0;36m'
white='\e[0m'
blue='\e[1;34m'
magenta='\e[1;35m'

config='pyproject.toml'

if [ ! -f ${config} ]; then
    echo "No configuration file found"
    poetry init
    exit 1
fi

# Gets package name from pyproject.toml
package="$(grep ^name.*=.*$ ${config} | cut -d'"' -f2)"
pypiUrl="https://pypi.org/project/${package}/"
# Gets latest version from the pypi website
versionOnPypi="$(curl "${pypiUrl}" -s | grep "<a class=\"card release__card\" href=\"/project/${package}/" -m 1 | cut -d'/' -f4)"

echo "${cyan}PyPi package: ${magenta}${package}\n\n${green}Found pyproject.toml\n\n${cyan}Python & PyPi requirements:${magenta}"

grep -v '^$\|#\|^ *$' ${config} | tr '\n' '\:' | sed 's/.*\[tool.poetry.dependencies\]://' | cut -d'[' -f1 | tr ':' ' '

echo "\n${cyan}Latest pypi.org version:\n${blue}${versionOnPypi}"
echo "${cyan}Enter a new version before building and publishing with poetry:${white}"
read poetryVersion

echo "\n${cyan}Backing up pyproject.toml${green}" && cp -v pyproject.toml backup_config.toml
echo "\n${cyan}Updating pyproject.toml${white}"
sed -i "s/^version.*=.*$/version = \"${poetryVersion}\"/" pyproject.toml

echo "\n${magenta}Beginning poetry building and publishing\n"

poetry build
poetry publish

exit 0
