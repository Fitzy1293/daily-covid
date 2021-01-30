#!/bin/env python3

from pprint import pprint
import os
import sys
import argparse
from .covid_plot import *
from .american_states import *
import requests
import csv

endpoint = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

parser = argparse.ArgumentParser(description='Create plots for up to date COVID-19 daily changes.', formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--get-data', '-g', dest='getData', action='store_true', help=f'Download data from New York Times COVID endpoint.\n{endpoint}\n ')
parser.add_argument('--state', '-s', nargs='*', default= [])
parser.add_argument('--county', '-c', default=False, help='\n')
parser.add_argument('-sc', nargs='*', dest='stateCounty', default=False, help='Use state and county syperated by a dash.\ndailycovid -sc \'state-county\'')

args = parser.parse_args()

if len(sys.argv) == 1: # Print help if using CL tool and there are no args.
    parser.print_help()
    sys.exit()

boxCharSep = '─' * 100
stateInfoDir = 'info-by-state'
outputDir = 'output-counties'

head = ['Date', 'Cases-Total: Δ=Daily-Change', 'Deaths-Total: Δ=Daily-Change']
headStr = ','.join(head)

stateCodes = sorted(stateCodesSet())

print() #space

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def createNewRow(row, previous):
    cases = f'{row[-2]}: Δ={int(row[-2]) - int(previous[-2])}'
    deaths = f'{row[-1]}: Δ={int(row[-1]) - int(previous[-1])}'
    return ([row[0], cases, deaths], row)

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def shortenTable(rows):
    previous = rows[0]
    fixedfirstDate = [previous[0], f'{previous[-2]}: Δ={previous[-2]}', f'{previous[-1]} Δ={previous[-1]}']
    returnRows = [fixedfirstDate]

    for row in rows[1:]:
        newRow = createNewRow(row, previous)
        returnRows.append(newRow[0])
        previous = newRow[-1]
    return returnRows

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def csvCreate(rows, fname):
    newCsvStr = '\n'.join([','.join(i) for i in rows])
    with open(fname, 'w+', encoding='utf-8') as f:
        f.write(f'{newCsvStr}\n')

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def writeInfoByState(path='', allInfo='', stateCode=''):
    with open(path, 'w+') as f:
        goodLines = '\n'.join([row[3:] for row in allInfo if row[:2] == stateCode])
        if stateCode == 'GU':
            goodLines = goodLines.replace('UNKNOWN', 'GUAM')
        f.write(f'{goodLines}\n')

#-----------------------------------------------------------------------------------------------------------------------------------------------------

def nytimesUpdate(endpoint=''):
    print(f'Downloading NY times COVID-19 CSV - {endpoint}')
    csvRaw = requests.get(endpoint)
    print(f'http status: {csvRaw.status_code}\n\nCreating files for each state for quicker searching.')

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
            if testingStateString in stateCodesSet():
                states.append((testingStateString, stateCodeKey().get(testingStateString)))
            else:
                sys.exit(f'{testingStateString} is not a valid two letter state code, stopping execution.')
        else:
            testingStateString = testingStateString.replace(' ', '-')
            if testingStateString in statesFullNameSet():
                states.append((stateFullNameKey().get(testingStateString), testingStateString))
            else:
                sys.exit(f'{testingStateString} is not the name of a state, stopping execution.')

    return states
#-----------------------------------------------------------------------------------------------------------------------------------------------------

def run(**kwargs):
    countyLines = kwargs.get('lines')
    dateRange = kwargs.get('dateRange')

    fileID = f'{kwargs["county"]}_{kwargs["stateCode"]}'
    csvFname = f'data_{fileID}.csv'
    plotsFname = f'plots_{fileID}.png'

    outPaths = {
        'csv': os.path.join(outputDir, csvFname),
        'plots': os.path.join(outputDir, plotsFname),
    }

    rowsCols = [i.split(',') for i in countyLines]
    reversedRows = reversed(shortenTable(rowsCols))

    outputTable = [i for i in reversedRows]
    csvCreate([head] + outputTable, outPaths['csv'])

    countyInfoPrintOut = (
                '\n'
                f'{len(rowsCols)} days\nDate range: {dateRange[0]} - {dateRange[1]}'
                f'\n\ncsv: {outPaths.get("csv")}\nplots: {outPaths.get("plots")}'
                f'\n{boxCharSep}'
    )

    print(countyInfoPrintOut)

    plotCovid(
        rowsCols,
        state=kwargs['state'],
        stateCode=kwargs['stateCode'],
        county=kwargs['county'],
        plotsPath=outPaths['plots'],
        dateRange=kwargs['dateRange']
    )
#-----------------------------------------------------------------------------------------------------------------------------------------------------
def main():
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    if not os.path.exists(stateInfoDir):
        os.mkdir(stateInfoDir)

    if args.getData: # Used when actually updating, shell online is easier
        nytimesUpdate(endpoint=endpoint)

    dictArgs = vars(args)
    if args.stateCounty:
        stateCountyList = [i.upper() for i in args.stateCounty]
        dictArgs['state'] = sorted(stateCountyList)

    if args.state or args.stateCounty:
        if not os.path.exists('us-counties.csv') or not os.path.exists(stateInfoDir):
            nytimesUpdate(endpoint=endpoint)
        statePairs = parseAmericanState(dictArgs['state'])

        for pair in sorted(set(statePairs)):
            stateCode = pair[0]
            state = pair[1]

            with open(os.path.join(stateInfoDir, f'{stateCode}.csv'), 'r') as f:
                csvLines = f.read().splitlines()

            if not args.county and not args.stateCounty:
                counties = set([line.split(',')[1].upper() for line in csvLines])
                counties = sorted(counties - {'UNKNOWN'})
                printCounties = "\n\t".join(counties)
                print(f'\n** Running for every county in "{stateCode}" **\n\t{printCounties}')
            elif args.stateCounty:
                counties = set([i.split('-')[1].upper().replace(' ', '-') for i in dictArgs['state'] if i.split('-')[0] in pair])
                counties = sorted(counties)
            elif args.state and args.county:
                counties = [dictArgs['county'].upper().replace(' ', '-')]

            print(f'\n{boxCharSep}')

            for county in counties:
                print(f'State: {stateCode} - County: {county}')
                lenCounty = len(county)

                stateCountyData = [i for i in csvLines if i[11:][:lenCounty] == county]
                dateRange = (stateCountyData[0][:10], stateCountyData[-1][:10])

                try:
                    run(
                        lines=stateCountyData,
                        stateCode=stateCode,
                        state=state,
                        county=county,
                        dateRange=dateRange
                    )
                except ZeroDivisionError:
                    pass

        print(f'Output files are located in the "{outputDir}" folder of the current working directory.')
        print(f'\nUsing cache from: {csvLines[-1][:10]}\nUse -g as an argument if you need to update the us-counties.csv cache.\n')
        print(f'CSV structure: {headStr}\n')

    print(f'Arguments used: {args}\n')
