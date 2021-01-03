#!/bin/env python3

from pprint import pprint
import os
from pathlib import Path
import sys
import argparse
from datetime import date
from .covid_plot import *
import subprocess
import requests


states = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California",
    "CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia",
    "HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas",
    "KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi",
    "MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
    "NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon",
    "PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah",
    "VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia",
    "WI":"Wisconsin","WY":"Wyoming"}

endpoint = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

parser = argparse.ArgumentParser(description='Create plots for up to date COVID-19 daily changes.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--getdata', '-g', action='store_true', help=f'Download data from New York Times COVID endpoint.\n{endpoint}\n ')
parser.add_argument('--state', '-s', default=False)
parser.add_argument('--county', '-c', default=False, help='\n')
parser.add_argument('-sc', dest='stateCounty', default=False, help='Use state and county syperated by a dash.\ndailycovid -sc \'state-county\'')

args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit()

if args.getdata: # Used when actually updating, shell online is easier
    nytimesUpdate(endpoint=endpoint)

endpoint = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
boxCarSep = '─' * 100
cwd = os.getcwd()
countiesDir = os.path.join(cwd, 'counties', '')
head = ['Date', 'Cases (Total: delta=Daily Change)', 'Deaths: (Total: delta=Daily Change)']
headStr = ','.join(head)

print() #space


#-----------------------------------------------------------------------------------------------------------------------------------------------------

def createNewRow(row, previous):
    cases = f'{row[-2]}: delta={int(row[-2]) - int(previous[-2])}'
    deaths = f'{row[-1]}: delta={int(row[-1]) - int(previous[-1])}'
    return ([dateFormat(row[0]), cases, deaths], row)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def shortenTable(rows):
    previous = rows[0]
    fixedFirstDay = [dateFormat(previous[0]), f'{previous[-2]}: delta={previous[-2]}', f'{previous[-1]} delta={previous[-1]}']
    returnRows = [fixedFirstDay]

    for row in rows[1:]:
        newRow = createNewRow(row, previous)
        returnRows.append(newRow[0])
        previous = newRow[-1]

    return returnRows

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def csvCreate(rows, fname):
    with open(fname, 'w+', encoding='utf-8') as f:
        for i in rows:
            f.write(f'{",".join(i)}\n')

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def nytimesUpdate(endpoint=''):
    print(f'Downloading NY times COVID-19 CSV - {endpoint}')
    r = requests.get(endpoint)
    print('http status:', r.status_code)
    endpointTxt = r.text # Writing to disk and keeping in memory
    with open('us-counties.csv', 'w+') as f:
        f.write(r.text)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def run(**kwargs):
    if not os.path.exists(countiesDir):
        os.mkdir(couniesDirs)

    stateReplaceSpace = kwargs['state'].replace(' ', '-')
    countyReplaceSpace = kwargs['county'].replace(' ', '-')
    csvFname = f'data_{countyReplaceSpace}_{stateReplaceSpace}.csv'
    plotsFname = f'plots_{countyReplaceSpace}_{stateReplaceSpace}.png'

    csvPath = countiesDir + csvFname
    plotsPath = countiesDir + plotsFname

    rowsCols = [i.split(',') for i in kwargs['lines']][:-1]


    outputTable = [i for i in reversed(shortenTable(rowsCols))]
    csvData = [head] + outputTable
    csvCreate(csvData, csvPath)


    print(f'\ncsv: {csvFname}\ntplot: {plotsFname}\ndays: {len(rowsCols)}\n')

    print(f'Range\n{" ".join(rowsCols[-1])}\n{" ".join(rowsCols[0])}')
    print(boxCarSep)


    plotCovid(rowsCols, state=kwargs['state'], county=kwargs['county'], plotsPath=plotsPath)


#-----------------------------------------------------------------------------------------------------------------------------------------------------

def main():

    dictArgs = vars(args)
    if args.stateCounty:
        stateCountyList = args.stateCounty.split('-')
        dictArgs['state'] = stateCountyList[0]
        dictArgs['county'] = stateCountyList[1]

    if args.state or args.stateCounty:
        if not os.path.exists('us-counties.csv'):
            nytimesUpdate(endpoint=endpoint)

        with open('us-counties.csv', 'r') as f:
            endpointTxt = f.read().splitlines()

        print(f'us-counties.csv date: {endpointTxt[1][:10]}\nUse -getdata as an argument if you need to update the us-counties.csv cache.\n')

        print(f'CSV structure: {headStr}\n')

        state = states[dictArgs['state'][:2].upper()].lower()

        if not args.county and not args.stateCounty:
            counties = set([i.split(',')[1].lower() for i in endpointTxt if state.lower() == i.lower().split(',')[2]])
            counties = sorted(counties - {'unknown'})
            print(*counties, sep='\n')

        else:
            counties = [dictArgs['county'].lower()]

        print(f'\n{boxCarSep}')
        for county in counties:
            print(f'{state} - {county}')
            query = f',{county},{state},'
            countyStateStr = f'{state},{county}'
            fname = '_'.join(countyStateStr.lower().split(',')) + '.csv'

            stateCountyData = [i for i in endpointTxt if query.lower() in i.lower()]
            try:
                run(lines=stateCountyData,
                     state=state,
                     county=county)
            except ZeroDivisionError:
                pass

    print(f'Find your files here: {countiesDir}')
