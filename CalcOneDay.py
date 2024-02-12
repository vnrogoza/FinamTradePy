from datetime import datetime, timedelta
import SecurityCandle

#Empty tables
SecurityCandleTable = []
CandleTable = []

#Load Security list table
#secFileName = "SecurityCandle.txt"
#secFileName = "GC.txt"

#SecurityCandleTable = SecurityCandle.LoadSecurityCandle(secFileName)

SecurityCandleTable = [["ITEM","GC","D1",None,None,None,None]]
#SecurityCandleTable = [["ITEM","GC","D1",None,None,None,None],["CETS","USD000UTSTOM","D1",None,None,None,None]]

#Load Candle table
CandleTable = SecurityCandle.LoadCandels(SecurityCandleTable)


#for sec in SecurityCandleTable:

table = {}
tablew = {}
xd = []
yd = []
xwd = []
ywd = []
for candle in CandleTable:    
    #['GC', 'D1', datetime.datetime(2023, 12, 29, 0, 0), 2079.2, 2084.1, 2067.6, 2075.3, 76467]
    sec = candle[0]
    tf = candle[1]
    T = candle[2]
    O = candle[3]
    H = candle[4]
    L = candle[5]
    C = candle[6]
    V = candle[7]
    d = T.day
    wd = T.weekday() #0..6
    #item = [O, C]
    up = C-O
    up = round(up, 3)
    #For statistics
    if table.get(d) == None:
        table[d]=[]
    if tablew.get(wd) == None:
        tablew[wd]=[]
    table[d].append(up)  #[31,N]
    tablew[wd].append(up) #[5,N]
    #For plotting
    xd.append(d)
    yd.append(up)
    xwd.append(wd)
    ywd.append(up)

table = dict(sorted(table.items()))

#Calc statistics
import statistics
mean=[]
gmean=[]
for key, values in table.items():
    m = statistics.mean(values)
    values2 = []
    for v in values:
        if v != 0:
            values2.append(abs(v))
    g = statistics.geometric_mean(values2)
    mean.append(m)
    gmean.append(g)

import matplotlib.pyplot as plt
import matplotlib as mpl
#import pandas as pd

if len(SecurityCandleTable) > 1:
    nrows = len(SecurityCandleTable)
    ncols = 2
    fig,  ax = plt.subplots(nrows=nrows, ncols=ncols)
    #plt.figure(figsize=[10,5])
    for i in range(nrows):    
        #Day data
        ax[i][0].scatter(xd, yd, s=0.5)
        x0 = [1, 31]
        y0 = [0, 0]
        ax[i][0].plot(x0, y0, 'y', linewidth=1)
        ax[i][0].scatter(range(1, len(mean)+1), mean, cmap="red")
        ax[i][0].set_title(SecurityCandleTable[i][1]+" Day")
        #WeekDay data
        ax[i][1].scatter(xwd, ywd, s=0.5)
        x0 = [0, 4]
        y0 = [0, 0]
        ax[i][1].plot(x0, y0, 'y', linewidth=1)
        ax[i][1].set_title(SecurityCandleTable[i][1]+" WeekDay")
    plt.show()
if len(SecurityCandleTable) == 1:        
    ncols = 2
    fig,  ax = plt.subplots(ncols=ncols)        
    #Day data
    ax[0].scatter(xd, yd, s=0.5)
    x0 = [1, 31]
    y0 = [0, 0]
    ax[0].plot(x0, y0, 'y', linewidth=1)
    ax[0].scatter(range(1, len(mean)+1), mean, cmap="red")
    ax[0].set_title(SecurityCandleTable[0][1]+" Day")
    #WeekDay data
    ax[1].scatter(xwd, ywd, s=0.5)
    x0 = [0, 4]
    y0 = [0, 0]
    ax[1].plot(x0, y0, 'y', linewidth=1)
    ax[1].set_title(SecurityCandleTable[0][1]+" WeekDay")
    plt.show()

