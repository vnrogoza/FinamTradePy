#ORDER MANAGEMENT - orders, trades, transactions
from finam_trade_api.base_client.models import FinamDecimal, FinamMoney
from finam_trade_api.order import (OrderRequest, OrderResponse, OrderType, Side)
import BaseMgt, AccountMgt
import asyncio

def CreateOrder(account_id, symbol, quantity, side, type, price=None, duration=None, label=None):
    #asyncio.run(PlaceOrder(account_id, symbol, quantity, side, type, price, duration, label))    
    client = asyncio.run( BaseMgt.GetClient() )
    asyncio.run( client.orders.place_order(OrderRequest(account_id=account_id, symbol=symbol, 
                                                        quantity=FinamDecimal(value=str(quantity)), 
                                                        side=side, type=type, 
                                                        price=FinamMoney(units=str(price)),
                                                        time_in_force=duration, client_order_id=label))   )
#def CreateOrder(*args):
#    asyncio.run(PlaceOrder(args[0], args[1], args[2], args[3], args[4]))
#def CreateOrder(**args):
#    asyncio.run(PlaceOrder(args['account_id'], args['symbol'], args['quantity'], args['side'], args['type']))
    

async def PlaceOrder(account_id, symbol, quantity, side, type, price=None, duration=None, label=None):
    client = await BaseMgt.GetClient()
    #await client.orders.place_order(OrderRequest(account_id="1922179", symbol="LQDT@MISX", quantity=FinamDecimal(value="1"), side=Side.SELL, type=OrderType.MARKET))
    await client.orders.place_order(OrderRequest(account_id=account_id, symbol=symbol, quantity=quantity, side=side, type=type, price=price,
                                                 time_in_force=duration, client_order_id=label)) 


async def GetOrders():
    client = await BaseMgt.GetClient()
    resp = await client.orders.get_orders(account_id="1908434")
    print(resp)


if __name__ == "__main__":        
    CreateOrder(account_id="1908434", symbol="GAZP@MISX", 
                price=115.0,
                quantity=1, side=Side.BUY, type=OrderType.LIMIT)
    print(AccountMgt.GetCurrentPosition(account_id="1908434", security_id="GAZP@MISX"))

