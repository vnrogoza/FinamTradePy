#Candle Data Mgt
import os
import asyncio

#from finam_trade_api.client import Client
#from finam_trade_api.candles.model import (DayCandlesRequestModel, DayInterval, IntraDayCandlesRequestModel, IntraDayInterval)
from finam_trade_api import Client
from finam_trade_api import TokenManager
from finam_trade_api.instruments.model import BarsRequest, TimeFrame
import BaseMgt
from datetime import datetime


#token = BaseMgt.LoadToken()

#NEW VERSION - API V2 Helper
async def GetCandles(Board, Security, TimeFrame, DateFrom, DateTo):
    
    #token = BaseMgt.LoadToken()
    #client = Client(TokenManager(token))
    #await BaseMgt.RefreshToken()
    client = await BaseMgt.GetClient()
    TimeFrameConverter ={"M5":"TIME_FRAME_M5","M15":"TIME_FRAME_M15","H1":"TIME_FRAME_H1","D1":"TIME_FRAME_D","W1":"TIME_FRAME_W"}
    DateFrom = BaseMgt.Loc2Utc(DateFrom)
    DateTo = BaseMgt.Loc2Utc(DateTo)
    params = BarsRequest(
        symbol= Security+'@'+Board,
        start_time=DateFrom,
        end_time=DateTo,
        timeframe=TimeFrameConverter[TimeFrame]
    )
    result =  await client.instruments.get_bars(params)    
    return result.bars

#NEW - Загрузка свечек из АПИ Финама 
def LoadCandels(argSecurityCandleTable):

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
        quantity = SecCandle[5]
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
            num = 0
            intervals = BaseMgt.GetDateIntervals(datefrom, dateto, timeframe, quantity)
            for interval in intervals:                
                candles = asyncio.run( GetCandles(board, security, timeframe, interval["DateFrom"], interval["DateTo"]) ) 
                num += len(candles)
                for line in candles:                    
                    if timeframe in ["D1","W1"]:
                        T = str(line.date)
                    else:
                        T = BaseMgt.Utc2Loc(str(line.timestamp))
                    O = line.open.value
                    H = line.high.value
                    L = line.low.value
                    C = line.close.value
                    V = line.volume.value
                    candle = [security, timeframe, T, O, H, L, C, V]
                    retCandleTable.append(candle) 

        if loadMode == 'F':
            candleFile = open(candleFileName, "r")
            num = 0 
            for line in candleFile:
                num += 1
                #security, timeframe
                items = line.rstrip().split(";")
                security = items[0]
                timeframe = items[1]
                #T = datetime.fromisoformat(items[2])
                T = items[2]
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


#OLD VERSION - API V1 Helper
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

#OLD VERSION - API V1 Helper
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

#OLD VER - Загрузка свечек из файла
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
            dateto = BaseMgt.DateNow(timeframe)
        if datefrom==None:
            if num == None:
                num = 250
            datefrom = BaseMgt.DateAdd(dateto, -num, timeframe)
            num = 250
        else:
            num = BaseMgt.DateInterval(datefrom, dateto, timeframe)
        SecCandle = [board, security, timeframe, datefrom, dateto, num, flag]
        retSecurityCandleTable.append(SecCandle)    
    file.close()
    return retSecurityCandleTable

#OLD VER - Загрузка свечек из АПИ Финама
def LoadCandelsOld(argSecurityCandleTable):
    #пишет в файлы свечки Candles
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
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
        quantity = SecCandle[5]
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
            '''
            if dateto in [None,'']:
                dateto = BaseMgt.DateNow(timeframe)
            if datefrom in [None,'']:
                if num in [None, 0]:
                    num = 400
                datefrom = BaseMgt.DateAdd(dateto, -num, timeframe)                
            else:
                num = BaseMgt.DateInterval(datefrom, dateto, timeframe)

            #k, m = divmod(len(row), lenth)  #k-частное, m-остаток
            partNumbers = {'W1':40,'D1':200,'H1':300,'M15':400,'M5':400}
            #деление длинног интервала на пачки                 
            size = partNumbers[timeframe]
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
                    dt0 = BaseMgt.DateAdd(datefrom, n0, timeframe)
                dt1 = BaseMgt.DateAdd(datefrom, n1, timeframe)                 
                if timeframe in ["D1","W1"]:
                    #candles = asyncio.run( get_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )
                    candles = asyncio.run( get_day_candles(board, security, timeframe, 0, dt0, dt1) )
                else:
                    #candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )   
                    candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, dt0, dt1) )
                    print(dt0,dt1)
                num += len(candles)
                for line in candles:
                    #security, timeframe                        
                    if timeframe in ["D1","W1"]:
                        T = str(line.date)
                    else:
                        T = BaseMgt.Utc2Loc(line.timestamp)
                    O = line.open.num/10**line.open.scale
                    H = line.high.num/10**line.high.scale
                    L = line.low.num/10**line.low.scale
                    C = line.close.num/10**line.close.scale
                    V = line.volume
                    candle = [security, timeframe, T, O, H, L, C, V]
                    retCandleTable.append(candle)                       
                
            n0 = (i+1)*size
            #n1 = num
            dt0 = BaseMgt.DateAdd(datefrom, n0, timeframe)
            dt1 = dateto             
            if timeframe in ["D1","W1"]:
                #candles = asyncio.run( get_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )
                candles = asyncio.run( get_day_candles(board, security, timeframe, 0, dt0, dt1) )
            else:
                #candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )   
                candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, dt0, dt1) )
                print(dt0,dt1)
            '''
            num = 0
            intervals = BaseMgt.GetDateIntervals(datefrom, dateto, timeframe, quantity)
            for interval in intervals:
                dt0 = interval["DateFrom"]
                dt1 = interval["DateTo"]
                if timeframe in ["D1","W1"]:
                    #candles = asyncio.run( get_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )
                    candles = asyncio.run( get_day_candles(board, security, timeframe, 0, interval["DateFrom"], interval["DateTo"]) )
                else:
                    #candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, str(dt0), str(dt1)) )   
                    candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, interval["DateFrom"], interval["DateTo"]) )
                num += len(candles)
                for line in candles:
                    #security, timeframe
                    #T = datetime.fromisoformat(line.date) 
                    if timeframe in ["D1","W1"]:
                        T = str(line.date)
                    else:
                        T = BaseMgt.Utc2Loc(line.timestamp)                        
                    O = line.open.num/10**line.open.scale
                    H = line.high.num/10**line.high.scale
                    L = line.low.num/10**line.low.scale
                    C = line.close.num/10**line.close.scale
                    V = line.volume
                    candle = [security, timeframe, T, O, H, L, C, V]
                    retCandleTable.append(candle) 

        if loadMode == 'F':
            candleFile = open(candleFileName, "r")
            num = 0 
            for line in candleFile:
                num += 1
                #security, timeframe
                items = line.rstrip().split(";")
                security = items[0]
                timeframe = items[1]
                #T = datetime.fromisoformat(items[2])
                T = items[2]
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
    