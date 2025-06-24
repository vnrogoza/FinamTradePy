import os
from pprint import pprint

#from finam_trade_api import Client
#from finam_trade_api import TokenManager
from finam_trade_api.account import GetTransactionsRequest, GetTradesRequest

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
        positions.append({"Security":symbol, "Quantity":float(pos.quantity.value), "AvgPrice":float(pos.averagePrice.value), "Price":float(pos.currentPrice.value)})
    return positions


async def main():
    #client = Client(TokenManager(token))
    #await client.access_tokens.set_jwt_token()
    client = await BaseMgt.GetClient()
    acc = await client.account.get_account_info(account_id)
    #pprint(type(res))
    print(acc.accountId, acc.equity.value)
    for pos  in acc.positions:
        print(pos.symbol, pos.quantity.value, pos.averagePrice.value, pos.currentPrice.value)
    

    '''
    pprint(await client.account.get_transactions(GetTransactionsRequest(
        account_id=account_id,
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-03-15T00:00:00Z",
        limit=10,
    )))

    pprint(await client.account.get_trades(GetTradesRequest(
        account_id=account_id,
        start_time="2024-01-01T00:00:00Z",
        end_time="2025-03-15T00:00:00Z",
    )))
    '''

if __name__ == "__main__":
    import asyncio
    account_id = '1908434'
    security = 'LQDT'
    #asyncio.run(main())
    #res = asyncio.run(GetAccountPositions(account_id))
    res = GetCurrentPosition(security_id=security, account_id=account_id)
    print(res)
