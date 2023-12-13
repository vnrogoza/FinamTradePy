import os
import asyncio
import pickle
from finam_trade_api.client import Client
import basemgt

#token = os.getenv("TOKEN", "")
token = basemgt.GetToken()
client = Client(token)
SecurityList = []

async def get_all_data():
    return await client.securities.get_data()

async def get_data_by_code(code: str):
    return await client.securities.get_data(code)

def GetSecurityList():
    #TQBR;GAZP;10.0;2
    filePath = "DB\SecurityList.txt"        
    if os.path.exists(filePath):
        secCard = []
        secList = []
        file = open(filePath, 'r')
        for line in file:
            line = line.rstrip()
            sec = line.split(";")
            secCard = [sec[0], sec[1], sec[2], sec[3]]
            secList.append(secCard)
        file.close()
    else:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        resp = asyncio.run(get_all_data())    
        secCard = []
        secList = []
        security_board = 'TQBR'  
        security_codes = ('SBER', 'VTBR', 'GAZP') #, 'MTLR', 'LKOH', 'PLZL', 'SBERP', 'BSPB', 'POLY', 'RNFT',
                      #'GMKN', 'AFLT', 'NVTK', 'TATN', 'YNDX', 'MGNT', 'ROSN', 'AFKS', 'NLMK', 'ALRS',
                      #'MOEX', 'SMLT', 'MAGN', 'CHMF', 'CBOM', 'MTLRP', 'SNGS', 'BANEP', 'MTSS', 'IRAO',
                      #'SNGSP', 'SELG', 'UPRO', 'RUAL', 'TRNFP', 'FEES', 'SGZH', 'BANE', 'PHOR', 'PIKK')  
        for i in range(len(resp.data.securities)):
            sec = resp.data.securities[i]
            if (sec.board in security_board) and (sec.code in security_codes):
                secCard = [sec.board, sec.code, sec.lotSize, sec.decimals]
                secList.append(secCard)               
        #with open("secList.txt", 'w', encoding='utf-8') as f:
        with open(filePath, 'w') as f:
            for secLine in secList:
                f.write(secLine[0]+';'+secLine[1]+';'+str(secLine[2])+';'+str(secLine[3])+'\n')                
        f.close
    return secList

def GetAllSecurityList():    
    filePath = "DB\AllSecurityList.txt"        
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    resp = asyncio.run(get_all_data())    
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write('board;code;market;decimals;lotSize;minStep;currency;shortName\n') 
        for i in range(len(resp.data.securities)):
        #for i in range(100):
            sec = resp.data.securities[i]             
            #f.write(str(sec)+'\n') 
            s = sec.board+';'+sec.code+';'+sec.market+';'+str(sec.decimals)+';'+str(sec.lotSize)+';'+str(sec.minStep)+';'+sec.currency+';'+sec.shortName+'\n'
            f.write(s)
        f.close  

if __name__ == "__main__":        
    ##SecurityList = GetSecurityList()
    ##    # print(SecurityList)
    GetAllSecurityList()
