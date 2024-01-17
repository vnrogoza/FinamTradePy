
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
import pandas as pd
f,  ax1 = plt.subplots()
f,  ax2 = plt.subplots()
#plt.figure(figsize=[10,5])
ax1.scatter(xd, yd, s=0.5)
x0 = [1, 31]
y0 = [0, 0]
ax1.plot(x0, y0, 'y', linewidth=1)
ax1.scatter(range(1, len(mean)+1), mean, cmap="red")
ax2.scatter(xwd, ywd, s=0.5)
x0 = [0, 4]
y0 = [0, 0]
ax2.plot(x0, y0, 'y', linewidth=1)
#plt.scatter(range(1, len(gmean)+1), gmean, cmap="green")

plt.show()