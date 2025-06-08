import os, datetime
import BaseMgt
from finam_trade_api import Client
from finam_trade_api import TokenManager

async def main():
    #token = os.getenv("TOKEN")    
    token = BaseMgt.LoadToken()
    client = Client(TokenManager(token))    
    renew = False
    validTime = None        

    try:
        #Здесь нужно сначала прописать jwttoken в client        
        resp = await client.access_tokens.get_jwt_token_details()                
        validTime = BaseMgt.Utc2Loc(str(resp.expiresAt)) 
        nowTime = str(datetime.datetime.now())
        if nowTime > validTime:
            renew = True
    except Exception as e:
        if str(e).find('Token is expired'):
            renew = True
        else:
            raise(e)        
    if renew:
        #print(f'Token is expired ({validTime}). New token released')
        #await client.access_tokens.reset_jwt_token()
        print(f'Token is expired ({validTime}).')
    else:
        print(f'Token is valid till {validTime}')



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    