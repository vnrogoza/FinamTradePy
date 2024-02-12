from datetime import datetime, timedelta
import SecurityCandle
import statistics
import matplotlib.pyplot as plt
import matplotlib as mpl

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

CandleTable2 = {}  #{Sec:[Candles]}
for candle in CandleTable:    
    sec = candle[0]
    if CandleTable2.get(sec) == None:  
        CandleTable2[sec]=[]
    CandleTable2[sec].append(candle)


for SecurityCandle in SecurityCandleTable: 
    sec = SecurityCandle[1]
    CandleTable3 = CandleTable2[sec]

    #aggregate data x and y
    table = {}  #{day:[values]}
    tablew = {} #weekday
    xd = []
    yd = []
    xwd = []
    ywd = []    
    for candle in CandleTable3:   
        #['GC', 'D1', datetime.datetime(2023, 12, 29, 0, 0), 2079.2, 2084.1, 2067.6, 2075.3, 76467]
        #sec = candle[0]
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
        
        if table.get(d) == None:   #list for sec-day
            table[d] = []        
        if tablew.get(wd) == None:   
            tablew[wd] = []        
        table[d].append(up)        
        tablew[wd].append(up)

        #This is for plotting only        
        xd.append(d)  #day points        
        yd.append(up)
        xwd.append(wd)  #weekday points        
        ywd.append(up)

    #Calc statistics
    trend={}
    table = dict(sorted(table.items()))  #sorted 1,2,3..
    for day, values in table.items():
        q = statistics.quantiles(values, n = 4)
        if q[0]>0 or q[2]<0:
            m = statistics.mean(values)
            trend[day] = m
      

    fig,  ax = plt.subplots(nrows=1, ncols=2)           
    i = 0
        
    #Day data
    ax[0].scatter(xd, yd, s=0.5)
    x0 = [min(xd), max(xd)]
    y0 = [0, 0]
    ax[0].plot(x0, y0, 'y', linewidth=1)
    ax[0].scatter(trend.keys(), trend.values(), cmap="red")
    ax[0].set_title(sec+" Day")
        
    #WeekDay data
    ax[1].scatter(xwd, ywd, s=0.5)    
    x0 = [min(xwd), max(ywd)]
    y0 = [0, 0]
    ax[1].plot(x0, y0, 'y', linewidth=1)
    ax[1].set_title(sec+" WeekDay")

    plt.show()

wait = input()

