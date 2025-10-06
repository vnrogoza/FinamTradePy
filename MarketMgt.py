#Candle Data Mgt
import os
import asyncio
from finam_trade_api.instruments.model import BarsRequest, TimeFrame
import BaseMgt
from datetime import datetime


#NEW - Загрузка свечек из АПИ Финама 
def LoadCandels(argSecurityCandleTable):
    #SecurityCandleTable = [["MISX","SBER","D1",'2025-08-16','2025-09-24',None,'W']]
    retCandleTable = []
    idx = 0
    for SecCandle in argSecurityCandleTable:
        #SecCandle = [board, security, timeframe, datefrom, dateto]
        loadMode = ''
        board = SecCandle[0]
        security = SecCandle[1]
        timeframe = SecCandle[2]    
        datefrom = SecCandle[3]
        dateto = SecCandle[4]
        quantity = SecCandle[5]
        flag = SecCandle[6]               
        if board in ['', None]:
            raise Exception('Board not specified')            
        if security in ['', None]:
            raise Exception('Security not specified')            
        if timeframe in ['', None]:
            raise Exception('Timeframe not specified')            
        if not timeframe in ['W1','D1','H1','M15','M5']:
            raise Exception('Wrong timeframe interval')
        
        candleFileName = f'DB\{security}_{timeframe}.txt'
        if os.path.exists(candleFileName):
            loadMode = 'F'  #local File,Local
            if os.path.getsize(candleFileName) == 0:
                loadMode = 'W'  #Finam
        else:
            loadMode = 'W'  #Finam Web
        if flag in ['1','W']:   #перезагрузка
            loadMode = 'W'  #Finam

        if loadMode == 'W':
            #Check and redefine dates, LoadSecurityCandle()    
            num = 0
            intervals = BaseMgt.GetDateIntervals(datefrom, dateto, timeframe, quantity)
            for interval in intervals:                
                candles = asyncio.run( GetCandles(board, security, timeframe, interval["DateFrom"], interval["DateTo"]) ) 
                num += len(candles)
                for line in candles:                    
                    if timeframe in ["D1","W1"]:
                        #T = str(line.date)
                        T = str(line.timestamp)[0:10]
                    else:
                        T = BaseMgt.Utc2Loc(str(line.timestamp))
                    O = line.open.value
                    H = line.high.value
                    L = line.low.value
                    C = line.close.value
                    V = line.volume.value
                    candle = [security, timeframe, T, O, H, L, C, V]
                    retCandleTable.append(candle) 

        if loadMode == 'F':
            candleFile = open(candleFileName, "r")
            num = 0 
            for line in candleFile:
                num += 1
                #security, timeframe
                items = line.rstrip().split(";")
                security = items[0]
                timeframe = items[1]
                #T = datetime.fromisoformat(items[2])
                T = items[2]
                O = float(items[3])
                H = float(items[4])
                L = float(items[5])
                C = float(items[6])
                V = int(items[7])
                candle = [security, timeframe, T, O, H, L, C, V]
                #candleFile.write(line.open.num+';'+line.high+';'+line.low+';'+line.low+'\n') 
                retCandleTable.append(candle) 
            candleFile.close()

        #update SecurityCandleTable        
        argSecurityCandleTable[idx][3] = datefrom
        argSecurityCandleTable[idx][4] = dateto    
        argSecurityCandleTable[idx][5] = num
        argSecurityCandleTable[idx][6] = ''  #flag 
        idx += 1
    return retCandleTable


#NEW VERSION - API V2 Helper
async def GetCandles(Board, Security, TimeFrame, DateFrom, DateTo):    
    #token = BaseMgt.LoadToken()
    #client = Client(TokenManager(token))
    #await BaseMgt.RefreshToken()
    client = await BaseMgt.GetClient()
    TimeFrameConverter ={"M5":"TIME_FRAME_M5","M15":"TIME_FRAME_M15","H1":"TIME_FRAME_H1","D1":"TIME_FRAME_D","W1":"TIME_FRAME_W"}
    DateFrom = BaseMgt.Loc2Utc(DateFrom)
    DateTo = BaseMgt.Loc2Utc(DateTo)
    params = BarsRequest(
        symbol= Security+'@'+Board,
        start_time=DateFrom,
        end_time=DateTo,
        timeframe=TimeFrameConverter[TimeFrame]
    )
    result =  await client.instruments.get_bars(params)    
    return result.bars


#OLD VER - Загрузка свечек из файла
def LoadSecurityCandle(argSecFileName):
    if (argSecFileName==None) or (argSecFileName==None):
        print('File not specified')
        quit()
    retSecurityCandleTable = []
    #file = open(secFileName,"r")
    file = open(argSecFileName,"r")
    for line in file:
        line = line.rstrip()
        scLine = line.split(';')
        board = scLine[0] if len(scLine)>=1 else None
        security = scLine[1] if len(scLine)>=2 else None
        timeframe = scLine[2] if len(scLine)>=3 else None    
        datefrom = datetime.fromisoformat(scLine[3]) if len(scLine)>=4 else None
        dateto = datetime.fromisoformat(scLine[4]) if len(scLine)>=5 else None    
        num = scLine[5] if len(scLine)>=6 else None
        flag = scLine[6] if len(scLine)>=7 else None
        if board == '':
            print('Board not specified')
            quit()
        if security == '':
            print('Security not specified')
            quit()
        if timeframe == '':
            print('Timeframe not specified')
            quit()
        if timeframe in ['']:
            print(f'Wrong timeframe {timeframe}')
            quit()
        #if num is None and datefrom is None and dateto is None:
        #    print('Num of candels / Datefrom-Dateto interval not specified')
        #    quit()
        #if num is None:
        if dateto==None:
            dateto = BaseMgt.DateNow(timeframe)
        if datefrom==None:
            if num == None:
                num = 250
            datefrom = BaseMgt.DateAdd(dateto, -num, timeframe)
            num = 250
        else:
            num = BaseMgt.DateInterval(datefrom, dateto, timeframe)
        SecCandle = [board, security, timeframe, datefrom, dateto, num, flag]
        retSecurityCandleTable.append(SecCandle)    
    file.close()
    return retSecurityCandleTable

    
if __name__ == "__main__":
    SecurityCandleTable = [["MISX","SBER","D1",'2025-09-16','2025-09-24',None,'W']]
    CandleTable = LoadCandels(SecurityCandleTable)
    print(CandleTable)