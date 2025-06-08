import os
from pprint import pprint

from finam_trade_api import Client
from finam_trade_api import TokenManager
from finam_trade_api.instruments.model import BarsRequest, TimeFrame

import BaseMgt
from datetime import datetime

#token = os.getenv("TOKEN")
jwt_token = None
jwt_date = None


async def main():
    token = BaseMgt.LoadToken()
    client = Client(TokenManager(token))    
    jwt_date, jwt_token = BaseMgt.LoadJwtToken()    
    refresh = False
    if (jwt_date in (None, '')) or (jwt_token in (None, '')):
        refresh = True    
    else:
        nowTime = str(datetime.now())
        if nowTime > jwt_date:
            refresh = True            
    if refresh:
        await client.access_tokens.reset_jwt_token()
        resp = await client.access_tokens.get_jwt_token_details()
        jwt_date = BaseMgt.Utc2Loc(str(resp.expiresAt)) 
        jwt_token = client.access_tokens.get_jwt_token()
        
         #payload={"secret": self._token_manager.token},
        BaseMgt.SaveJwtToken(jwt_date, jwt_token)        
    else:
        client.access_tokens.set_jwt_token(jwt_token)

    params = BarsRequest(
        symbol="YDEX@MISX",
        start_time="2025-05-20T07:00:00Z",
        end_time="2025-05-31T23:00:00Z",
        timeframe=TimeFrame.TIME_FRAME_H1,
    )
    
    #pprint(await client.instruments.get_bars(params))
    resp = await client.instruments.get_bars(params)
    print(len(resp.bars))
    #pprint(await client.instruments.get_last_quote("YDEX@MISX"))
    #pprint(await client.instruments.get_last_trades("YDEX@MISX"))
    #pprint(await client.instruments.get_order_book("YDEX@MISX"))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
