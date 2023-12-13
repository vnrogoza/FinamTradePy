import os
import asyncio
from finam_trade_api.client import Client
import basemgt 


async def main():
    #client = Client(os.getenv("TOKEN"))    
    token = basemgt.GetToken()    
    client = Client(token)    
    return await client.access_tokens.check_token()


if __name__ == "__main__":        
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    print(asyncio.run(main()))
