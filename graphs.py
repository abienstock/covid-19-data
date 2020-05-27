# author: Alex Bienstock

import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

if(len(sys.argv) != 4):
    print("python graphs.py [state] [county] [new/cummulative]")
    exit()

state = str(sys.argv[1])
county = str(sys.argv[2])

with open('us-counties.csv') as csvfile:
    reader = csv.reader(csvfile)
    data = []
    for row in reader:
        if row[1] == county and row[2] == state:
            data.append((row[4], row[5]))
    npdata = np.asarray(data, dtype=np.int16)
    indices = np.arange(npdata.shape[0])
    if str(sys.argv[3]) == "new":
        indices = indices[1:]
        firstday = npdata[:-1]
        secondday = npdata[1:]
        diff = np.subtract(secondday, firstday)
        fig, ax = plt.subplots()
        print(indices.shape, npdata.shape)
        plt.scatter(indices, diff[:,0], label='cases', s=5)
        plt.plot(indices, diff[:,0])
        plt.scatter(indices, diff[:,1], label='deaths', s=5)
        plt.plot(indices, diff[:,1])
        ax.set_title("New Cases and Deaths in " + county + " County, " + state)
        ax.legend()
        plt.show()
    else:
        fig, ax = plt.subplots()
        plt.scatter(indices, npdata[:,0], label='cases', s=5)
        plt.plot(indices, npdata[:,0])
        plt.scatter(indices, npdata[:,1], label='deaths', s=5)
        plt.plot(indices, npdata[:,1])
        ax.set_title("Cummulative Cases and Deaths in " + county + " County, " + state + " cummulative")
        ax.legend()
        plt.show()

