#!/bin/env bash
poetry build && poetry publish
pip uninstall dailycovid
pip install dailycovid
pip install dailycovid
