from datetime import datetime, timedelta
import SecurityCandle

#Empty tables
SecurityCandleTable = []
CandleTable = []

#Load Security list table
#secFileName = "SecurityCandle.txt"
#secFileName = "GC.txt"

#SecurityCandleTable = SecurityCandle.LoadSecurityCandle(secFileName)

#SecurityCandleTable = [["ITEM","GC","D1",None,None,None,None]]
SecurityCandleTable = [["ITEM","GC","D1",None,None,None,None],["CETS","USD000UTSTOM","D1",None,None,None,None]]

#Load Candle table
CandleTable = SecurityCandle.LoadCandels(SecurityCandleTable)

#aggregate data x and y
table = {}  #{day:[values]}
xd = {}
yd = {}
tablew = {} #weekday
xwd = {}
ywd = {}
for candle in CandleTable:    #sec1, sec2...
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
    wd = T.weekday()+1 #0..6
    #item = [O, C]
    up = C-O
    up = round(up, 3)
    #For statistics: sec-day-[values] -> calc avg values
    if table.get(sec) == None:  #dic for sec
        table[sec]={}
    if table[sec].get(d) == None:   #list for sec-day
        table[sec][d] = []
    #if table.get(d) == None:
    #    table[d]=[]
    #if tablew.get(wd) == None:
    #    tablew[wd]=[]
    if tablew.get(sec) == None:  
        tablew[sec]={}
    if tablew[sec].get(wd) == None:   
        tablew[sec][wd] = []
    #table[d].append(up)  #[31,N]
    table[sec][d].append(up)
    #tablew[wd].append(up) #[5,N]
    tablew[sec][wd].append(up)

    #This is for plotting only
    if xd.get(sec)== None:
        xd[sec] = []
    xd[sec].append(d)  #day points
    if yd.get(sec)== None:
        yd[sec] = []
    yd[sec].append(up)

    if xwd.get(sec)== None:
        xwd[sec] = []
    xwd[sec].append(wd)  #weekday points
    if ywd.get(sec)== None:
        ywd[sec] = []
    ywd[sec].append(up)

table = dict(sorted(table.items()))

#Calc statistics
import statistics
trend={}
for sec in SecurityCandleTable: 
    trend[sec[1]]={}
    days  = table[sec[1]]
    days = dict(sorted(days.items()))  #sorted 1,2,3..
    for day, values in days.items():        
        q = statistics.quantiles(values, n = 4)
        if q[0]>0 or q[2]<0:
            m = statistics.mean(values)
            trend[sec[1]][day] = m
        
        

import matplotlib.pyplot as plt
import matplotlib as mpl
#import seaborn as sns
#import pandas as pd



if len(SecurityCandleTable) > 1:
    nrows = len(SecurityCandleTable)
    ncols = 2
    fig,  ax = plt.subplots(nrows=nrows, ncols=ncols)    
    #plt.figure(figsize=[10,5])
        
    i = 0
    for sec in SecurityCandleTable:    
        
        #Day data
        ax[i][0].scatter(xd[sec[1]], yd[sec[1]], s=0.5)
        x0 = [min(xd[sec[1]]), max(xd[sec[1]]) ]
        y0 = [0, 0]
        ax[i][0].plot(x0, y0, 'y', linewidth=1)
        
        #mean = {"GC":{4:10,15:5}, "USD000UTSTOM":{6:1,23:-1}}
        #ax[i][0].scatter(mean[sec[1]].keys(),mean[sec[1]].values(), cmap="red")
        ax[i][0].scatter(trend[sec[1]].keys(), trend[sec[1]].values(), cmap="red")
        ax[i][0].set_title(sec[1]+" Day")
        

        #WeekDay data
        ax[i][1].scatter(xwd[sec[1]], ywd[sec[1]], s=0.5)
        #x0 = [0, max(xwd[sec[1]]) ]
        x0 = [min(xwd[sec[1]]), max(xwd[sec[1]]) ]
        y0 = [0, 0]
        ax[i][1].plot(x0, y0, 'y', linewidth=1)
        ax[i][1].set_title(sec[1]+" WeekDay")
        i += 1

    plt.show()
    w = input()
    

