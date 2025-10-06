from finam_trade_api.base_client.models import FinamDecimal, FinamMoney
from finam_trade_api.account import (GetTransactionsRequest, GetTradesRequest)

#token = os.getenv("TOKEN")
#account_id = os.getenv("ACCOUNT_ID")
import BaseMgt


def GetCurrentPosition(account_id, security_id):
    import asyncio
    positions = asyncio.run(GetAccountPositions(account_id))    
    for position in positions:
        if position["Security"]==security_id:
            return {"quantity":position["Quantity"], "price":position["Price"], "avgprice":position["AvgPrice"]}
    return {"quantity": 0, "price": None, "avgprice":None}


async def GetAccountPositions(account_id):
    client = await BaseMgt.GetClient()
    
    accResponse = await client.account.get_account_info(account_id)
    positions = []
    for pos in accResponse.positions:
        #i = pos.symbol.find('@')
        #symbol = pos.symbol[:i]
        symbol = pos.symbol
        
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


async def GetOrders():
    client = await BaseMgt.GetClient()
    resp = await client.orders.get_orders(account_id="1922179")
    pprint(resp)


if __name__ == "__main__":
    import asyncio
    account_id = '1908434'  #'1908434'
    security = 'LQDT@MISX'  #'LQDT'    
    #res = GetCurrentPosition(security_id=security, account_id=account_id)
    #print('\n Quantity ', res)
    positions = asyncio.run(GetAccountPositions(account_id))    
    for position in positions:
        print(position)
