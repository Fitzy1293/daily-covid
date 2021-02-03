#!/bin/env python3

from pprint import pprint
import os
import sys
from sys import exit as done
import argparse
from .covid_plot import *
from .american_states import *
import requests
from traceback import print_exc
import pandas as pd
import numpy as np

cwd = os.getcwd()
endpoint = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

parser = argparse.ArgumentParser(description='Create plots for up to date COVID-19 daily changes.', formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--get-data', '-g', dest='getData', action='store_true', help=f'Download data from New York Times COVID endpoint.\n{endpoint}\n ')
parser.add_argument('--state', '-s', nargs='*', dest='parserState', default= [])
parser.add_argument('--county', '-c', default=False, help='\n')
parser.add_argument('--county-level', '-sc', nargs='*', dest='stateCounty', default=[], help='Use state and county syperated by a dash.\ndailycovid -sc \'state-county\'')
parser.add_argument('--plot', '-p', dest='plot', default=False, action='store_true')
parser.add_argument('-all', dest='all', default=False, action='store_true')

args = parser.parse_args()

if len(sys.argv) == 1: # Print help if using CL tool and there are no args.
    parser.print_help()
    sys.exit()

boxCharSep = '─' * 100
stateInfoDir = 'info-by-state'
outputDir = 'output-counties'

head = ['Date', 'Cases-Total: Δ=Daily-Change', 'Deaths-Total: Δ=Daily-Change']
headStr = ','.join(head)

stateAbbrevs = stateCodesSet()
stateCodes = sorted(stateAbbrevs)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def deltaTable(county='', csvPath='', dateRange=''): # This is shit, rewrite this.
    fields = ('date','county','cases','deaths')

    df = pd.read_csv(csvPath,names=fields)
    countyDf = df[df['county'] == (county)]

    dates = [i for i in countyDf['date']]

    initCounts = countyDf.to_string().split('      ')
    initCases = initCounts[-2].strip()
    initDeaths = initCounts[-1].strip()

    cases = np.array(countyDf['cases'])
    caseDeltas = np.diff(cases * -1)
    deaths = np.array(countyDf['deaths'])
    deathsDeltas = np.diff(deaths * -1)

    returnRows = []
    for date, case, caseDelta, death, deathsDelta in zip(dates, cases, caseDeltas, deaths, deathsDeltas):
        returnRows.append( (f'{date},{case}: Δ={caseDelta},{death}: Δ={deathsDelta}') )

    returnRows.append(f'{dates[-1]},{initCases}: Δ={initCases},{initDeaths}: Δ={initDeaths}')

    return returnRows

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def deltaCsvCreate(rows, fname):
    rows = "\n".join(rows)
    with open(fname, 'w+', encoding='utf-8') as f:
        f.write(f'{headStr}\n{rows}\n')

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def writeInfoByState(path='', allInfo='', stateCode=''):
    with open(path, 'w+') as f:
        goodLines = '\n'.join(reversed([row[3:] for row in allInfo if row[:2] == stateCode]))
        if stateCode == 'GU':
            goodLines = goodLines.replace('UNKNOWN', 'GUAM')
        #if stateCode == 'PR':
            #pass#goodLines = goodLines.replace(',\n', 'GUAM')
        f.write(f'{goodLines}\n')

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def nytimesUpdate():
    print(f'Downloading NY times COVID-19 CSV - {endpoint}')
    csvRaw = requests.get(endpoint)
    print(f'http status: {csvRaw.status_code}\nCreating state CSV cache')

    normalizedTxt = csvRaw.text.upper().replace(' ', '-')
    nytimesLines = normalizedTxt.split('\n')

    with open('us-counties.csv', 'w+') as f:
            f.write(normalizedTxt)

    newCsv = []
    for line in nytimesLines[1:]:
        cells = line.split(',')
        newCsv.append(f'{stateFullNameKey().get(cells[2])},{cells[0]},{cells[1]},{cells[4]},{cells[5]}')

    allInfo = sorted(set(newCsv))

    for stateCode in stateCodes:
        outCSV = os.path.join('info-by-state', f'{stateCode}.csv')
        print(f'\t{outCSV}')
        writeInfoByState(path=outCSV, allInfo=allInfo, stateCode=stateCode)

#-----------------------------------------------------------------------------------------------------------------------------------------------------
def parseAmericanState(inputState=''):
    states = []
    for str in inputState:
        if '-' in str:
            str = str.split('-')[0]
        testingStateString = str.upper()

        if len(testingStateString) == 2:
            if testingStateString in stateAbbrevs:
                states.append((testingStateString, stateCodeKey()[testingStateString]))
            else:
                sys.exit(f'{testingStateString} is not a valid two letter state code, stopping execution.')
        else:
            testingStateString = testingStateString.replace(' ', '-')
            if testingStateString in statesFullNameSet():
                states.append((stateFullNameKey()[testingStateString], testingStateString))
            else:
                sys.exit(f'{testingStateString} is not the name of a state, stopping execution.')

    return states
#-----------------------------------------------------------------------------------------------------------------------------------------------------

def run(**kwargs):
    countyLines = kwargs.get('lines')
    dateRange = kwargs.get('dateRange')
    county = kwargs['county']
    stateCode = kwargs['stateCode']
    state = kwargs['state']

    fileID = f'{county}_{stateCode}'
    csvFname = f'data_{fileID}.csv'
    plotsFname = f'plots_{fileID}.png'

    outPaths = {
        'csv': os.path.join(outputDir, csvFname),
        'plots': os.path.join(outputDir, plotsFname),
        'cachedCsv': os.path.join('info-by-state', f'{stateCode}.csv')
    }

    newCsv = deltaTable(county=county, csvPath=outPaths['cachedCsv'], dateRange=dateRange)
    dateRange = (newCsv[-1][:10], newCsv[0][:10])
    deltaCsvCreate(newCsv, outPaths['csv'])

    printOut = ''
    if args.plot:
        printOut = f'\nplots: {outPaths["plots"]}'
        sevenDays = [i.split(',') for i in newCsv[:7]]
        sevenDaysData = '\n'.join([' '.join(i[1:]) for i in sevenDays])
        data = [(i.split(',')[1].split(':')[0], i.split(',')[2].split(':')[0]) for i in newCsv]
        plotCovid(
            data,
            state=state,
            stateCode=stateCode,
            county=county,
            plotsPath=outPaths['plots'],
            dateRange=dateRange,
            previousWeek=f'Previous 7 days (Cases, Deaths)\n{dateRange[1]} - {sevenDays[6][0]}\n\n{sevenDaysData}'
    )

    countyInfoPrintOut = (
                '\n'
                f'{len(newCsv)} days: {dateRange[0], dateRange[1]}'
                f'\n\ncsv: {outPaths["csv"]}{printOut}'
                f'\n{boxCharSep}'
    )

    print(countyInfoPrintOut)


#-----------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    if args.parserState and args.stateCounty:
        sys.exit('You cannot use -sc and -s together.\nUse them individually.')

    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    if not os.path.exists(stateInfoDir):
        os.mkdir(stateInfoDir)

    if args.getData: # Used when actually updating, shell online is easier
        nytimesUpdate()

    dictArgs = vars(args)

    if args.parserState or args.stateCounty or args.all:
        if not os.path.exists('us-counties.csv') or not os.path.exists(stateInfoDir):
            nytimesUpdate()

        if args.stateCounty:
            statePairs = sorted(set(parseAmericanState(args.stateCounty)))
        elif args.parserState:
            statePairs = sorted(set(parseAmericanState(args.parserState)))
        elif args.all:
            statePairs = parseAmericanState(stateCodes)

        for pair in statePairs:
            stateCode = pair[0]
            state = pair[1]

            with open(os.path.join(stateInfoDir, f'{stateCode}.csv'), 'r') as f:
                csvLines = f.read().splitlines()

            if not args.county and not args.stateCounty:
                counties = set([line.split(',')[1].upper() for line in csvLines if line.count(',') > 1])
                counties = sorted(counties - {'UNKNOWN'})
                printCounties = "\n\t".join(counties)
                print(f'\n** Running for every county in "{stateCode}" **\n\t{printCounties}')
            elif args.stateCounty:
                counties = set([i.split('-')[1].upper().replace(' ', '-') for i in args.stateCounty if i.upper().split('-')[0] in pair])
                counties = sorted(counties)
            elif args.state and args.county:
                counties = [dictArgs['county'].upper().replace(' ', '-')]

            print(f'\n{boxCharSep}')
            for county in counties:
                print(f'State: {stateCode} - County: {county}')
                lenCounty = len(county)

                try:
                    run(
                        lines=csvLines,
                        stateCode=stateCode,
                        state=state,
                        county=county,
                        dateRange=''
                    )
                except ZeroDivisionError:
                    pass

        print(f'Output files are located in the "{outputDir}" folder of the current working directory.')
        print(f'\nUsing cache from: {csvLines[-1][:10]}\nUse -g as an argument if you need to update the us-counties.csv cache.\n')
        print(f'CSV structure: {headStr}\n')
