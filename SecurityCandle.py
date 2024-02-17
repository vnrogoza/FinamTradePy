#Candle Data Helper
import os
import asyncio

from finam_trade_api.client import Client
from finam_trade_api.candles.model import (DayCandlesRequestModel, DayInterval, IntraDayCandlesRequestModel, IntraDayInterval)
import BaseHelper
from datetime import datetime, timedelta


token = BaseHelper.GetToken()
#Board,Sec,Tf,Num,DtFrom,DtTo

async def get_day_candles(argBoard, argSecurity, argTimeFrame, argCount, argDateFrom, argDateTo):
  client = Client(token)
  params = DayCandlesRequestModel(
    securityBoard = argBoard, #"CETS", #"TQBR",
    securityCode = argSecurity, #"USD000UTSTOM", #SBER
    timeFrame = argTimeFrame, #DayInterval.D1, #D1, W1
    intervalFrom = argDateFrom, #"2023-11-01",  # yyyy-MM-dd
    intervalTo = argDateTo #"2023-11-20",
    )
  result = await client.candles.get_day_candles(params)
  return result


async def get_in_day_candles(argBoard, argSecurity, argTimeFrame, argCount, argDateFrom, argDateTo):
    client = Client(token)
    params = IntraDayCandlesRequestModel(
        securityBoard = argBoard, 
        securityCode = argSecurity,
        timeFrame = argTimeFrame,
        intervalFrom = argDateFrom,
        intervalTo = argDateTo
        )
    return await client.candles.get_in_day_candles(params)

def LoadSecurityCandle(argSecFileName):
    if (argSecFileName==None) or (argSecFileName==None):
        print('File not specified')
        quit()
    retSecurityCandleTable = []
    #file = open(secFileName,"r")
    file = open(argSecFileName,"r")
    for line in file:
        line = line.rstrip()
        scLine = line.split(';')
        board = scLine[0] if len(scLine)>=1 else None
        security = scLine[1] if len(scLine)>=2 else None
        timeframe = scLine[2] if len(scLine)>=3 else None    
        datefrom = datetime.fromisoformat(scLine[3]) if len(scLine)>=4 else None
        dateto = datetime.fromisoformat(scLine[4]) if len(scLine)>=5 else None    
        num = scLine[5] if len(scLine)>=6 else None
        flag = scLine[6] if len(scLine)>=7 else None
        if board == '':
            print('Board not specified')
            quit()
        if security == '':
            print('Security not specified')
            quit()
        if timeframe == '':
            print('Timeframe not specified')
            quit()
        if timeframe in ['']:
            print(f'Wrong timeframe {timeframe}')
            quit()
        #if num is None and datefrom is None and dateto is None:
        #    print('Num of candels / Datefrom-Dateto interval not specified')
        #    quit()
        #if num is None:
        if dateto==None:
            dateto = BaseHelper.DateNow(timeframe)
        if datefrom==None:
            if num == None:
                num = 250
            datefrom = BaseHelper.DateAdd(dateto, -num, timeframe)
            num = 250
        else:
            num = BaseHelper.DateInterval(datefrom, dateto, timeframe)
        SecCandle = [board, security, timeframe, datefrom, dateto, num, flag]
        retSecurityCandleTable.append(SecCandle)    
        
    #file = open(secFileName,"w")
    for line in SecurityCandleTable:
        file.write(line[0]+';'+line[1]+';'+str(line[2])+';'+str(line[3])+';'+str(line[4])+';'+str(line[5])+';'+str(line[6])+'\n')    
    #file.close()

    file.close()
    return retSecurityCandleTable

def LoadCandels(argSecurityCandleTable):
    #пишет в файлы свечки Candles
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    retCandleTable = []
    idx = 0
    for SecCandle in argSecurityCandleTable:
        #SecCandle = [board, security, timeframe, datefrom, dateto]
        loadMode = ''
        board = SecCandle[0]
        security = SecCandle[1]
        timeframe = SecCandle[2]    
        datefrom = SecCandle[3]
        dateto = SecCandle[4]
        num = SecCandle[5]
        flag = SecCandle[6]               
        if board in ['', None]:
            print('Board not specified')
            quit()
        if security in ['', None]:
            print('Security not specified')
            quit()
        if timeframe in ['', None]:
            print('Timeframe not specified')
            quit()
        
        candleFileName = f'DB\{security}_{timeframe}.txt'            
        if os.path.exists(candleFileName):
            loadMode = 'F'  #local File,Local
            if os.path.getsize(candleFileName) == 0:
                loadMode = 'W'  #Finam
        else:
            loadMode = 'W'  #Finam Web
        if flag in ['1','W']:   #перезагрузка
            loadMode = 'W'  #Finam
       
        if loadMode == 'W':
            #Check and redefine dates, LoadSecurityCandle()
            if dateto==None:
                dateto = BaseHelper.DateNow(timeframe)
            if datefrom==None:
                if num == None:
                    num = 250
                datefrom = BaseHelper.DateAdd(dateto, -num, timeframe)
                num = 250
            else:
                num = BaseHelper.DateInterval(datefrom, dateto, timeframe)

            if timeframe in ["D1","W1"]:
                datefrom = datefrom.date()
                dateto = dateto.date()

            if num <= 250:
                #1 request            
                if timeframe in ["D1","W1"]:
                    candles = asyncio.run( get_day_candles(board, security, timeframe, 0, str(datefrom), str(dateto)) )
                else:
                    candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, str(datefrom), str(dateto)) )   
                num = candles.count()
                candleFile = open(candleFileName, "w")
                for line in candles:             
                    #security, timeframe
                    T = datetime.fromisoformat(line.date)
                    O = line.open.num/10**line.open.scale
                    H = line.high.num/10**line.high.scale
                    L = line.low.num/10**line.low.scale
                    C = line.close.num/10**line.close.scale
                    V = line.volume
                    candle = [security, timeframe, T, O, H, L, C, V]
                    retCandleTable.append(candle)
                    candleFile.write(security+';'+timeframe+';'+str(T)+';'+str(O)+';'+str(H)+';'+str(L)+';'+str(C)+';'+str(V)+'\n') 
                candleFile.close()
            else:
                #N-request
                #деление длинног интервала на пачки 
                candleFile = open(candleFileName, "w")
                size = 250
                #numCount = num//size
                #lastNum = num%size
                numCount = int(num/size)+1
                size = int(num/numCount)
                num = 0
                for i in range(numCount-1):
                    n0 = i*size
                    n1 = (i+1)*size-1
                    if i == 0:
                        dt0 = datefrom
                    else:    
                        dt0 = BaseHelper.DateAdd(datefrom, n0, timeframe)
                    dt1 = BaseHelper.DateAdd(datefrom, n1, timeframe)                 
                    if timeframe in ["D1","W1"]:
                        candles = asyncio.run( get_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )
                    else:
                        candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )   
                    num += len(candles)
                    for line in candles:
                        #security, timeframe
                        T = datetime.fromisoformat(line.date)
                        O = line.open.num/10**line.open.scale
                        H = line.high.num/10**line.high.scale
                        L = line.low.num/10**line.low.scale
                        C = line.close.num/10**line.close.scale
                        V = line.volume
                        candle = [security, timeframe, T, O, H, L, C, V]
                        retCandleTable.append(candle)
                        candleFile.write(security+';'+timeframe+';'+str(T)+';'+str(O)+';'+str(H)+';'+str(L)+';'+str(C)+';'+str(V)+'\n') 
                    
                n0 = (i+1)*size
                #n1 = num
                dt0 = BaseHelper.DateAdd(datefrom, n0, timeframe)
                dt1 = dateto             
                if timeframe in ["D1","W1"]:
                    candles = asyncio.run( get_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )
                else:
                    candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )   
                num += len(candles)
                for line in candles:
                    #security, timeframe
                    T = datetime.fromisoformat(line.date)
                    O = line.open.num/10**line.open.scale
                    H = line.high.num/10**line.high.scale
                    L = line.low.num/10**line.low.scale
                    C = line.close.num/10**line.close.scale
                    V = line.volume
                    candle = [security, timeframe, T, O, H, L, C, V]
                    retCandleTable.append(candle)
                    candleFile.write(security+';'+timeframe+';'+str(T)+';'+str(O)+';'+str(H)+';'+str(L)+';'+str(C)+';'+str(V)+'\n') 
                candleFile.close()


        if loadMode == 'F':
            candleFile = open(candleFileName, "r")
            num = 0 
            for line in candleFile:
                num += 1
                #security, timeframe
                items = line.rstrip().split(";")
                security = items[0]
                timeframe = items[1]
                T = datetime.fromisoformat(items[2])
                O = float(items[3])
                H = float(items[4])
                L = float(items[5])
                C = float(items[6])
                V = int(items[7])
                candle = [security, timeframe, T, O, H, L, C, V]
                #candleFile.write(line.open.num+';'+line.high+';'+line.low+';'+line.low+'\n') 
                retCandleTable.append(candle) 
            candleFile.close()

        #update SecurityCandleTable        
        argSecurityCandleTable[idx][3] = datefrom
        argSecurityCandleTable[idx][4] = dateto    
        argSecurityCandleTable[idx][5] = num
        argSecurityCandleTable[idx][6] = ''  #flag 
        idx += 1
    return retCandleTable
    