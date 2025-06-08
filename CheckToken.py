import asyncio
from datetime import datetime
from finam_trade_api.client import Client
from finam_trade_api import TokenManager
import BaseMgt 


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
        print(f'Token is expired ({jwt_date}).')
        await client.access_tokens.reset_jwt_token()                
        resp = await client.access_tokens.get_jwt_token_details()
        jwt_date = BaseMgt.Utc2Loc(str(resp.expiresAt)) 
        jwt_token = client.access_tokens.get_jwt_token()
        
         #payload={"secret": self._token_manager.token},
        BaseMgt.SaveJwtToken(jwt_date, jwt_token)        
    else:
        client.access_tokens.set_jwt_token(jwt_token)
        print(f'Token is valid till {jwt_date}')        


if __name__ == "__main__":        
    asyncio.run(main())
