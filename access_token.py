import os, datetime
import BaseMgt
from finam_trade_api import Client
from finam_trade_api import TokenManager

#from finam_trade_api.base_client import TokenManager
#from finam_trade_api.base_client.token_manager import TokenManager


async def main():
    #token = os.getenv("TOKEN")
    #token = 'a7a4dd6a-b271-463c-9367-524bbc75d8af'
    #token = 'eyJraWQiOiI2NjUzYTU1NC1jZGQ4LTQ2OTUtYjBhMy03NTUzNTdjY2NjM2YiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJwYXJlbnQiOiJjMmE0NWQ5ZS1iZTI2LTQ1N2UtYmVmZS0wZTU1MWVkZWM3YzUiLCJhcGlUb2tlblByb3BlcnRpZXMiOiJINHNJQUFBQUFBQUFfeTJTUFpMYk1BeUZkMHc1OXJoRXVlV204MHdLei00RktJcVVGSnVTekI5YlRxTm02NlRJYVhLWEhDSUhTSm1aRkxsRUhnZzEzd01KUUFBQjdYXy0tX0huN3l0dDl1cjV0OXB2WHA2T3U4UDJZNmhEVTR6NzNVekhENGRLLTNrc0dzek1XdXNVaTk2OFk3WHo1Rmw3TzdkRm5jMml1Y1Q1UHBhOGNVeW02QlIwMFdTdXJGTV9tRlZMWEVnU0g3TG9ySDBValhaVnVhOUhMeHF5YUJhX3FkMnFTZFFhVVM5LW0wSlJKMzNNclphNDd1eFdMZS1ZTDgwZ3V1WmQxbnFYVWU2OWJvb09Xdm9ialBpSGRqMnZmUS1QOWY0aDUwbExfZGhKblhpWDk2Uno1TUV2OVdCS3c0dkJnUG5DNWxBWHdfdjZTekdHS1pTZExOSDB4LTFCTFhFcTkzRmFBLUwwZmlwR0NqWS1fMUo3UlVyYkdZaVdjV1hnaUdVQ1Z3WTdNRUtxNm05ZjMybkxfRTRLdzJRZ3dIUTk0QzBEbWVabWFkZDg3b2VHUDJ2elREdm5fT0xEaVNyWEQ1b09UTDgwT1QxbzYwYXNsWlJEa1kxRGZHc0RxYzdoWTVnMnFkNW1JQ1BpWWg0QVY3bHdRNWd4WUpEaFVhYnlYcU1KSDI2a01IWEFNMkxQOEF5OEMtTm1GQXZlTVdwU0dEbVZId3c4eDFQaGEtRWJuRndvR0R3eHBKcTJJWnNhelVVOUFqWXk0SW90Y29GUE1Mc082RkVsSmpTRzlaRktEVjZSTGplcUVucUVPZUlUNllGUFpBMzNuVXZNU0tsNHV5UTc1a055aFJFMGh0M1lPY25HY1dnYlRiSjFrdDJTTFBUbDZUOUQtcVl3dlFNQUFBIiwiemlwcGVkIjp0cnVlLCJjcmVhdGVkIjoiMTc0ODY2OTU4NyIsInJlbmV3RXhwIjoiMTc4MDIwNTY0NyIsInNlc3MiOiJINHNJQUFBQUFBQUEvMU1LNDFKSnRFZzFOMGcyTWRKTlMwdE8welZKTXpIV3RUUktUZEpOdFRTeFNFNHpOMDR6VFVrVjRyb3c2Y0tHQzFzdTdMaXdSNHJud29JTCt5NXNCdUx0RnpZb2laUWxwbVRteGhmbHArZFhKVHJrSm1ibTZCV1ZBZ0NqTEFCdFdBQUFBQSIsImlzcyI6InR4c2VydmVyIiwia2V5SWQiOiI2NjUzYTU1NC1jZGQ4LTQ2OTUtYjBhMy03NTUzNTdjY2NjM2YiLCJ0eXBlIjoiVHJhZGVBcGkyMCIsInNlY3JldHMiOiJNc1pVQlRmT2JVOUpRWDRvR2NhMU1RPT0iLCJ0c3RlcCI6ImZhbHNlIiwiZXhwIjoxNzgwMjA1NTg3LCJqdGkiOiJhN2E0ZGQ2YS1iMjcxLTQ2M2MtOTM2Ny01MjRiYmM3NWQ4YWYifQ.YYmWRZh9d9zpMqYR8YTqu7iIIrjtlnDq9SyDN3_abIqNOQVX30O81nFlXt9VxPGqEz_8IJ-BuGjr_sIF7rsjSA'
    token = BaseMgt.LoadToken()
    client = Client(TokenManager(token))
    #await client.access_tokens.set_jwt_token()   #Этом модуль доработан. См.VNR
    renew = False
    validTime = None    
    

    try:
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
        print(f'Token is expired ({validTime}). New token released')
        await client.access_tokens.set_jwt_token()
    else:
        print(f'Token is valid till {validTime}')



if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    