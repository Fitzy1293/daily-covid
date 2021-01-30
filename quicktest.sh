#!/bin/env bash
clear
time (python3 test_pkg.py -sc ma-berkshire)
echo
head ./counties/data_berkshire_massachusetts.csv
xdg-open ./counties/plots_berkshire_massachusetts.png
