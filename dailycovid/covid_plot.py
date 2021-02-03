import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from pprint import pprint
from time import time
import pandas as pd

size = 8
dpi = 250
markersize = 2
linewidth = 1


def dateFormat(str=''):
    dateElements = str.split('-')
    day = dateElements[-1].lstrip('0')
    month = dateElements[1].lstrip('0')
    year = dateElements[0]
    return f'{month}/{day}/{year}'

# -----------------------------------------------------------------------------------------------------------------------

def plotCovid(data, state='', county='', plotsPath='', dateRange=('',''), stateCode='', previousWeek=''):
    rows = [i for i in reversed(data)]

    numOfDays = len(rows)

    casesInt = []
    deathsInt = []
    for i in rows:
        casesInt.append(int(i[-2]))
        deathsInt.append(int(i[-1]))


    cases = np.array(casesInt)
    deaths = np.array(deathsInt)
    fatalityRates = np.divide(deaths, cases) * 100
    ar = np.arange(0, numOfDays)

    dateRangeStr = f'{dateFormat(dateRange[0])} - {dateFormat(dateRange[1])}'
    togetherTitle = f'COVID-19 Tracking\n{county}, {stateCode}'

    gs = gridspec.GridSpec(3, 2)  # Create 3x2 sub plots
    fig = plt.figure()

# -----------------------------------------------------------------------------------------------------------------------

    casesSubplot = fig.add_subplot(gs[0, 1])  # row 0, col 0
    casesSubplot.set_title('title')

    casesSubplot.plot(cases,
                        'r.',
                        markersize=markersize)

    casesSubplot.set(xlabel=dateRangeStr,
                        ylabel='Cumulative Cases',
                        title='$y = cases(day)$')

# -----------------------------------------------------------------------------------------------------------------------

    deathsSubplot = fig.add_subplot(gs[2, 1])  # row 0, col 1
    deathsSubplot.set_title('title')
    deathsSubplot.plot(deaths,
                        'm.-',
                        markersize=markersize,
                        linewidth=linewidth)

    deathsSubplot.set(xlabel=dateRangeStr,
                        ylabel='Cumulative Deaths',
                        title='$y = deaths(day)$')

# -----------------------------------------------------------------------------------------------------------------------

    axfatality = fig.add_subplot(gs[1, 1])

    axfatality.plot(fatalityRates,'g.', linewidth=linewidth, markersize=markersize)
    axfatality.text(.98, 0.05,
                        f'Fatality rate\nCurrent: {round(fatalityRates[-1], 1)}%',
                        verticalalignment='bottom',
                        horizontalalignment='right',
                        transform=axfatality.transAxes,
                        color='black',
                        fontsize=8,
                        style='italic')

# -----------------------------------------------------------------------------------------------------------------------

    casesDeathsSubplot = fig.add_subplot(gs[:, 0])  # col 1, span all rows:
    casesDeathsSubplot.plot(ar, cases, 'r', linewidth=linewidth)
    casesDeathsSubplot.plot(ar, deaths, 'm', linewidth=linewidth)

    plt.fill_between(ar, deaths, cases,
                        facecolor="orange",  # The fill color
                        color='r',       # The outline color
                        alpha=.2)

    plt.fill_between(ar, deaths,
                        facecolor="green",  # The fill color
                        color='m',       # The outline color
                        alpha=.2)

    casesDeathsSubplot.set_title('Combined title',
                                    style='italic')

    casesDeathsSubplot.set(xlabel=dateRangeStr,
                            ylabel='COVID-19 Cases and Deaths',
                            title=togetherTitle)
    casesDeathsSubplot.legend((f'Cases={format(cases[numOfDays-1], ",d")}', f'Deaths={format(deaths[numOfDays-1], ",d")}'))

    casesDeathsSubplot.text(.05, 0.9,
                        previousWeek,
                        verticalalignment='top',
                        horizontalalignment='left',
                        transform=casesDeathsSubplot.transAxes,
                        color='black',
                        fontsize=6,
                        style='italic')


# -----------------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------
    fig.set_size_inches(size, size)
    plt.subplots_adjust(hspace=.5, wspace=.75)
    plt.savefig(plotsPath, dpi=dpi)
    plt.close()  # Don't forget or it memory leaks.
