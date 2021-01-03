import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import datetime

#months = [i for i in dates if i.split('/')[1] == '01']
size = 9


def dateFormat(nytDate):
    return '/'.join(nytDate.split('-')[1:] + [nytDate.split('-')[0]])

def plotCovid(rows, state='', county='', plotsPath=''):
    cases = [int(i[-2]) for i in rows[1:]]
    deaths = [int(i[-1]) for i in rows[1:]]
    dates = [dateFormat(i[0]) for i in (rows[0], rows[-1])]

    startDate = dates[0]
    endDate = dates[-1]


    togetherTitle = f'COVID-19 Tracking\n{county.title()}, {state.title()}\n{startDate} - {endDate}'

    gs = gridspec.GridSpec(3, 2) # Create 3x2 sub plots
    fig = plt.figure()

#-----------------------------------------------------------------------------------------------------------------------

    ax1 = fig.add_subplot(gs[0, 1 ]) # row 0, col 0
    ax1.set_title('title', style='italic')

    ax1.plot(cases, 'r.-')
    ax1.set(xlabel=f'Days since {startDate}',
            ylabel='Cases',
            title='$f(x) = cases(days)$')

#-----------------------------------------------------------------------------------------------------------------------

    ax2 = fig.add_subplot(gs[2, 1]) # row 0, col 1
    ax2.set_title('title', )#style='italic')
    ax2.plot(deaths, 'm.-')
    ax2.set(xlabel=f'Days since {startDate}', ylabel='Total deaths',
           title='$f(x) = deaths(day)$')

#-----------------------------------------------------------------------------------------------------------------------

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
    ax3.set(xlabel=f'Days since {startDate}',
    ylabel='COVID-19 cases and deaths',
           title=togetherTitle)

#-----------------------------------------------------------------------------------------------------------------------\

    axfatality = fig.add_subplot(gs[1, 1])

    fatalityRates = [100 * (deaths[i]) / float(cases[i]) for i in range(len(cases))]
    axfatality.plot(fatalityRates, 'g.-')
    axfatality.text(.98, 0.05,
        f'Fatality rate\nCurrent: {round(fatalityRates[-1], 1)} %',
        verticalalignment='bottom', horizontalalignment='right',
        transform=axfatality.transAxes,
        color='black', fontsize=8, style='italic')

#-----------------------------------------------------------------------------------------------------------------------

    fig.set_size_inches(size, size)
    plt.subplots_adjust(hspace=.3, wspace=.75)
    plt.savefig(plotsPath, dpi = 200)
    plt.close() # Don't forget or it memory leaks.
