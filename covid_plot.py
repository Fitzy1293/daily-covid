from nytimes_covid import dateFormat
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
from nytimes_covid import dateFormat
import datetime

def plotCovid(rows, state='', county='', countiesPath=''):
    cases = [int(i[-2]) for i in rows[1:]]
    deaths = [int(i[-1]) for i in rows[1:]]
    dates = [dateFormat(i[0]) for i in rows[1:]]

    startDate = dates[0]
    endDate = dates[-1]
    months = [i for i in dates if i.split('/')[1] == '01']


    countyTitle = county.title()
    stateTitle = state.title()
    togetherTitle = f'COVID-19 Tracking\n{countyTitle},{stateTitle}\n{startDate} - {endDate}'



    gs = gridspec.GridSpec(3, 2) # Create 2x2 sub plots

    fig = plt.figure()

    ax1 = fig.add_subplot(gs[0, 1 ]) # row 0, col 0
    ax1.set_title('title', style='italic')

    ax1.plot(cases, 'r.-')
    ax1.set(xlabel=f'Days since {startDate}',
            ylabel='Cases',
            title='f(x) = cases(days)')

    ax2 = fig.add_subplot(gs[2, 1]) # row 0, col 1
    ax2.set_title('title', style='italic')
    ax2.plot(deaths, 'm.-')
    ax2.set(xlabel=f'Days since {startDate}', ylabel='Total deaths',
           title='f(x) = deaths(days)')
    ax2.plot([0,1])

    ax3 = fig.add_subplot(gs[:, 0]) # col 1, span all rows:
    ax3.plot(cases, 'r', linewidth=3)
    ax3.plot(deaths, 'm', linewidth=3)

    plt.fill_between(np.arange(0, len(cases)), deaths, cases,
                 facecolor="orange", # The fill color
                 color='r',       # The outline color
                 alpha=.3)
    plt.fill_between(np.arange(0, len(cases)), deaths,
                facecolor="green", # The fill color
                color='m',       # The outline color
               alpha=.5)

    ax3.set_title('Combined title', style='italic')
    ax3.set_ylabel('Active Wee1')
    ax3.set(xlabel=f'Days since {startDate}',
    ylabel='COVID-19 cases and deaths',
           title=togetherTitle)


    ax4 = fig.add_subplot(gs[1, 1 ]) # row 0, col 0
    #ax4.axis('off')


    fatalityRates = [100 * (deaths[i] / cases[i]) for i in range(len(cases))]
    ax4.plot(fatalityRates, 'g.-')

    ax4.text(.98, 0.05, f'Fatality rate\nCurrent: {round(fatalityRates[-1], 1)} %',
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax4.transAxes,
        color='black', fontsize=8, style='italic')




    fig.set_size_inches(12, 12)
    plt.subplots_adjust(wspace=.5)
    plt.savefig(countiesPath, dpi = 250)
