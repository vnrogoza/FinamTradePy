import os
import asyncio

from finam_trade_api.client import Client
from finam_trade_api.candles.model import (DayCandlesRequestModel, DayInterval, IntraDayCandlesRequestModel, IntraDayInterval)
import BaseHelper
from datetime import datetime, timedelta

token = BaseHelper.GetToken()
#Board,Sec,Tf,Num,DtFrom,DtTo
SecurityCandleTable = []

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


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#print(asyncio.run(get_day_candles()))
#res = asyncio.run(get_day_candles('CTS','USD000UTSTOM','D1',0,'2023-12-01','2023-12-14'))
file = open("DB\SecurityCandle.txt","r+")
for line in file:
    line = line.rstrip()
    scLine = line.split(';')
    board = scLine[0] if len(scLine)>=1 else None
    security = scLine[1] if len(scLine)>=2 else None
    timeframe = scLine[2] if len(scLine)>=3 else None
    flag = scLine[3] if len(scLine)>=4 else None
    num = scLine[4] if len(scLine)>=5 else None
    datefrom = datetime.fromisoformat(scLine[5]) if len(scLine)>=6 else None
    dateto = datetime.fromisoformat(scLine[6]) if len(scLine)>=7 else None
    if board == '':
        print('Board not specified')
        quit()
    if security == '':
        print('Security not specified')
        quit()
    if timeframe == '':
        print('Timeframe not specified')
        quit()
    #if num is None and datefrom is None and dateto is None:
    #    print('Num of candels / Datefrom-Dateto interval not specified')
    #    quit()
    #if num is None:
    SecCandle = [board, security, timeframe, flag, num, datefrom, dateto]
    SecurityCandleTable.append(SecCandle)

i = 0
for SecCandle in SecurityCandleTable:
    #SecCandle = [board, security, timeframe, datefrom, dateto]
    board = SecCandle[0]
    security = SecCandle[1]
    timeframe = SecCandle[2]
    flag = SecCandle[3]
    num = SecCandle[4]
    datefrom = SecCandle[5]
    dateto = SecCandle[6]
    if dateto==None:
        dateto = BaseHelper.DateNow(SecCandle[2])
    if datefrom==None:
        datefrom = BaseHelper.DateAdd(dateto, -250, SecCandle[2])
    if flag == '1':    
        if timeframe in ["D1","W1"]:
            candles = asyncio.run( get_day_candles(board, security, timeframe, 0, str(datefrom.date()), str(dateto.date())) )
        else:
            candles = asyncio.run( get_in_day_candles(board, security, timeframe, 0, str(datefrom), str(dateto)) )
    
        # print(candles)
        candleFileName = f'DB\{security}_{timeframe}.txt'
        #file_name = f'{datapath}{security_board}.{security_code}_{tf}.txt'
        candleFile = open(candleFileName,"w")
        for line in candles:        
            candleFile.write(line.open.num+';'+line.high+';'+line.low+';'+line.low+'\n') 


    flag = 0
    
    SecCandle[3] = flag 
    SecCandle[4] = num
    SecCandle[5] = datefrom
    SecCandle[6] = dateto
    SecurityCandleTable[i] = SecCandle
    i += 1

print(SecurityCandleTable)

#file = open("DB\SecurityCandle.txt","w")
for line in SecurityCandleTable:
    file.write(line[0]+';'+line[1]+';'+line[2]+';'+str(line[3])+';'+str(line[4])+';'+str(line[5])+';'+str(line[6])+'\n')
file.close


