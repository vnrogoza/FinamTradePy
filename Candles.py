import os
import asyncio

from finam_trade_api.client import Client
from finam_trade_api.candles.model import (
    DayCandlesRequestModel,
    DayInterval,
    IntraDayCandlesRequestModel,
    IntraDayInterval
)
import basemgt

token = basemgt.GetToken()

async def get_day_candles():
    client = Client(token)
    params = DayCandlesRequestModel(
        securityBoard="CETS", #"TQBR",
        securityCode="USD000UTSTOM", #//"SBER",
        timeFrame=DayInterval.D1,
        intervalFrom="2023-11-01",
        intervalTo="2023-11-20",
    )
    return await client.candles.get_day_candles(params)


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
res = asyncio.run(get_day_candles())

print(res);
print(type(res));
'''
if __name__ == "__main__":
    

    print(asyncio.run(get_day_candles()))

    #print(asyncio.run(get_in_day_candles()))
'''
