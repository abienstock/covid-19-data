# author: Alex Bienstock

import csv
import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import mplcursors

if(len(sys.argv) != 4):
    print("python graphs.py [state] [county] [new/cummulative]")
    exit()

state = str(sys.argv[1])
county = str(sys.argv[2])

with open('us-counties.csv') as csvfile:
    reader = csv.reader(csvfile)
    data = []
    dates = []
    for row in reader:
        if row[1] == county and row[2] == state:
            dates.append(row[0])
            data.append((row[4], row[5]))

    date_indices = []
    nth_dates = []
    num_dates = len(dates)
    for i,date in enumerate(reversed(dates)):
        if i % 5 == 0:
            date_indices.append(i)
            nth_dates.append(date)
    for i,date in enumerate(date_indices):
        date_indices[i] = num_dates - date_indices[i]
    date_indices = date_indices
    nth_dates = nth_dates

    npdata = np.asarray(data, dtype=np.int16)
    indices = np.arange(npdata.shape[0])
    if str(sys.argv[3]) == "new":
        dates = dates[1:]
        for i,index in enumerate(date_indices):
            date_indices[i] -= 2
        indices = indices[1:]
        firstday = npdata[:-1]
        secondday = npdata[1:]
        diff = np.subtract(secondday, firstday)
        fig, ax = plt.subplots()
        cases = plt.scatter(dates, diff[:,0], label='cases', s=7)
        deaths = plt.scatter(dates, diff[:,1], label='deaths', s=7)
        ax.set_title("New Cases and Deaths in " + county + " County, " + state)
        ax.set(xticks=date_indices, xticklabels=nth_dates)
        plt.xticks(rotation=45)
        ax.legend()
        cursor = mplcursors.cursor(hover=True)

        @cursor.connect("add")
        def on_add(sel):
            i = sel.target.index
            if sel.artist == cases:
                sel.annotation.set_text(dates[i] + '\n' + str(diff[i,0]) + ' new cases')
            else:
                sel.annotation.set_text(dates[i] + '\n' + str(diff[i,1]) + ' new deaths')
                
        plt.plot(dates, diff[:,0])
        plt.plot(dates, diff[:,1])        
        plt.show()
    else:
        for i,index in enumerate(date_indices):
            date_indices[i] -= 1        
        fig, ax = plt.subplots()
        cases = plt.scatter(dates, npdata[:,0], label='cases', s=7)
        deaths = plt.scatter(dates, npdata[:,1], label='deaths', s=7)
        ax.set_title("Cummulative Cases and Deaths in " + county + " County, " + state + " cummulative")
        ax.set(xticks=date_indices, xticklabels=nth_dates)
        plt.xticks(rotation=45)
        ax.legend()
        cursor = mplcursors.cursor(hover=True)

        @cursor.connect("add")
        def on_add(sel):
            i = sel.target.index
            if sel.artist == cases:
                sel.annotation.set_text(dates[i] + '\n' + str(npdata[i,0]) + ' cases')
            else:
                sel.annotation.set_text(dates[i] + '\n' + str(npdata[i,1]) + ' deaths')
        
        plt.plot(dates, npdata[:,0])
        plt.plot(dates, npdata[:,1])        
        plt.show()

