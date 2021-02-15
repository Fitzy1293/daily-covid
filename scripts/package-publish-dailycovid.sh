#!/bin/env bash


grep -v ex.gif README.md > README-pip.md

./scripts/poetry-version-verify.sh
./scripts/update-figures.sh

rm backup_config.toml

exit 0
