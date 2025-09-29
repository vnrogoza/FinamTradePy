import os
from pprint import pprint

#from finam_trade_api import Client
#from finam_trade_api import TokenManager
from finam_trade_api.account import GetTransactionsRequest, GetTradesRequest
from finam_trade_api.order import OrderRequest, OrderResponse, OrderType, Side

#token = os.getenv("TOKEN")
#account_id = os.getenv("ACCOUNT_ID")
import BaseMgt


def GetCurrentPosition(account_id, security_id):
    positions = asyncio.run(GetAccountPositions(account_id))    
    for position in positions:
        if position["Security"]==security_id:
            return position["Quantity"]


async def GetAccountPositions(account_id):
    client = await BaseMgt.GetClient()
    
    accResponse = await client.account.get_account_info(account_id)
    positions = []
    for pos in accResponse.positions:
        i = pos.symbol.find('@')
        symbol = pos.symbol[:i]
        positions.append({"Security":symbol, "Quantity":float(pos.quantity.value), "AvgPrice":float(pos.average_price.value), "Price":float(pos.current_price.value)})
        
    return positions

async def GetAccountInfo(account_id):
    client = await BaseMgt.GetClient()

    # Получение списка транзакций
    pprint('get_transactions')
    pprint(await client.account.get_transactions(GetTransactionsRequest(
        account_id=account_id,
        start_time="2025-09-20T00:00:00Z",
        end_time="2025-09-30T00:00:00Z",
        limit=10,
    )))
    

    # Получение списка сделок    
    pprint('get_trades')
    pprint(await client.account.get_trades(GetTradesRequest(
        account_id=account_id,
        start_time="2025-09-20T00:00:00Z",
        end_time="2025-09-30T00:00:00Z",
    )))

    # Получение информации об аккаунте
    pprint('get_account_info')
    pprint(await client.account.get_account_info(account_id))

async def CreateOrder():
    client = await BaseMgt.GetClient()
    resp = await client.orders.place_order(OrderRequest(
        account_id="1922179", 
        symbol="MISX@LQDT",
        quantity="1",
        type=OrderType.MRK,
        side=Side.BUY
    ))
        

if __name__ == "__main__":
    import asyncio
    account_id = '1922179'  #'1908434'
    security = 'LQDT'  #'LQDT'

    #asyncio.run(main())
    #res = asyncio.run(GetAccountPositions(account_id))
    
    #res = GetCurrentPosition(security_id=security, account_id=account_id)
    #print('\n Quantity ', res)

    #asyncio.run( GetAccountInfo("994942") )

    asyncio.run(  CreateOrder()  )

    


#LQDT@MISX'
#NRV5@RTSX