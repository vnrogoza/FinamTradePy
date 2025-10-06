#GetSecurityList() загрузка списка выбранных инструментов из веб в файл
#GetAllSecurityList() загрузка списка всех инструментов из веб в файл
#LoadAllSecurityList()  загрузка/обновление списка всех инструментов из веб в БД

import os, asyncio, sqlite3
#import pickle
from finam_trade_api.client import Client
from datetime import datetime
import BaseMgt

#token = os.getenv("TOKEN", "")
#token = BaseMgt.GetToken()
#client = Client(token)
SecurityList = []


def GetAllSecurityListV2():
    client = asyncio.run( BaseMgt.GetClient() )
    resonse = asyncio.run( client.assets.get_assets() )
    return


#OLD VERSION - API V1 Helper
async def get_all_data():
    return await client.securities.get_data()
#OLD VERSION - API V1 Helper
async def get_data_by_code(code: str):
    return await client.securities.get_data(code)

#OLD  - Загрузка списка инструментов из файла или АПИ Финам
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

#OLD  - Загрузка списка всех инструментов из АПИ Финам и сохранение в файл
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

def LoadAllSecurityList():    
    filePath = "DB\AllSecurityList.txt"        
    #asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
 
    resp = asyncio.run(get_all_data())
    print("Save data to file...")
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write('board;code;market;decimals;lotSize;minStep;currency;shortName\n') 
        for i in range(len(resp.data.securities)):
            sec = resp.data.securities[i]
            s = sec.board+';'+sec.code+';'+sec.market+';'+str(sec.decimals)+';'+str(sec.lotSize)+';'+str(sec.minStep)+';'+sec.currency+';'+sec.shortName+'\n'
            f.write(s)
        f.close  

    print("Save data to DB...")
    counter = 0
    dataParts = BaseMgt.SplitListByLenth(resp.data.securities, 1000)
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()    
    for part in dataParts:
        #dtNow = str(datetime.now())[:-7]
        updateData = []
        for item in part:            
            #item.market = item.market.value                        
            ditem = dict(item)
            updateData.append(ditem)                
        cursor.executemany('INSERT OR IGNORE INTO Security (Code, Board, Market, Decimals, LotSize, MinStep, Currency, Properties, TimeZoneName, BpCost, AccruedInterest, PriceSign, Ticker, LotDivider, ShortName,  ModifyDT) VALUES (:code, :board, :market, :decimals, :lotSize, :minStep, :currency, :properties, :timeZoneName, :bpCost, :accruedInterest, :priceSign, :ticker, :lotDivider, :shortName, datetime("now","localtime") ) ; ', updateData)
        #cursor.executemany('UPDATE Security SET ModifyDT=datetime("now","localtime") WHERE Code=:code', updateData)
        counter += len(updateData)
        connection.commit()
    connection.close()  
    print(counter, 'lines were updated')

    
if __name__ == "__main__":    
    #GetAllSecurityList()
    #LoadAllSecurityList()
    GetAllSecurityListV2()
    
