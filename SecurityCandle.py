import os
import asyncio

from finam_trade_api.client import Client
from finam_trade_api.candles.model import (
    DayCandlesRequestModel,
    DayInterval,
    IntraDayCandlesRequestModel,
    IntraDayInterval
)
import BaseHelper

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


async def get_in_day_candles():
    client = Client(token)
    params = IntraDayCandlesRequestModel(
        securityBoard="TQBR",
        securityCode="SBER",
        timeFrame=IntraDayInterval.M1,
        intervalFrom="2023-06-07 08:33:52",
        count=10
    )
    return await client.candles.get_in_day_candles(params)


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#print(asyncio.run(get_day_candles()))
#res = asyncio.run(get_day_candles('CTS','USD000UTSTOM','D1',0,'2023-12-01','2023-12-14'))
file = open("DB\SecurityCandle.txt")
for line in file:
    line = line.rstrip()
    sc = line.split(';')
    board = sc[0] if len(sc)>=1 else None
    security = sc[1] if len(sc)>=2 else None
    timeframe = sc[2] if len(sc)>=3 else None
    num = sc[3] if len(sc)>=4 else None
    datefrom = sc[4] if len(sc)>=5 else None
    dateto = sc[5] if len(sc)>=5 else None
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


    SecurityCandleTable.append(sc)


print(SecurityCandleTable)