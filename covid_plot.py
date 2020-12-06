from nytimes_covid import dateFormat
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
def plotCovid(rows, state='', county='', countiesPath=''):
    cases = [int(i[-2]) for i in rows[1:]]
    deaths = [int(i[-1]) for i in rows[1:]]

    genericTitle = f'{county}, {state} - COVID-19 cases'

    startDate = dateFormat(rows[1][0])
    endDate = dateFormat(rows[-1][0])

    gs = gridspec.GridSpec(2, 2) # Create 2x2 sub plots

    fig = plt.figure()

    ax1 = fig.add_subplot(gs[0, 1]) # row 0, col 0
    ax1.plot(cases, 'r.-')
    ax1.set(xlabel=f'Days since {startDate}', ylabel='Cases',
           title=genericTitle)

    ax2 = fig.add_subplot(gs[1, 1]) # row 0, col 1
    ax2.plot(deaths, 'm.-')
    ax2.set(xlabel=f'Days since {startDate}', ylabel='Total deaths',
           title=genericTitle)
    ax2.plot([0,1])

    ax3 = fig.add_subplot(gs[:, 0]) # col 1, span all rows
    ax3.plot(cases, 'r')
    ax3.plot(deaths, 'm')
    plt.fill_between(np.arange(0, len(cases)), deaths, cases,
                 facecolor="orange", # The fill color
                 color='r',       # The outline color
                 alpha=0.2)
    plt.fill_between(np.arange(0, len(cases)), deaths,
                 facecolor="orange", # The fill color
                 color='m',       # The outline color
                 alpha=0.2)

    ax3.set(xlabel=f'Days since {startDate}', ylabel='COVID-19 cases and deaths',
           title=f'COVID-19 Tracking\n{genericTitle}\n{startDate} - {endDate}')

    fig.set_size_inches(15, 15)
    plt.savefig(countiesPath, dpi = 100)
