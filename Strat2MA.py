#Стратегия 2МА
#OnRun() - одна свеча
#Test() - прогон на исторических данных
#CreateReport() - формирование отчёта
import sqlite3, HtmlReportMgt

def OnRun(argTestCandle=None, argTestMode=False):
    #argTestCandle=() - use it, argTestCandle=None - from table
    #argTestMode - table names    
    #Init
    StgyCode = '2MA_01'
    Class="TQBR"
    Firm="MC0061900000"
    Client="S7912/S7912"
    Account="L01+00000F00"
    Security="SBER"
    Period = "H1"
    ma1period = 9
    ma2period = 21
    candTable = 'Candles' 
    stCandTable = 'StgyCandles' 
    stValTable = 'StgyValues'    
        
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor() 
        
    #LastCandle   
    if argTestMode:
        stCandTable = 'TestStgyCandles'
        stValTable = 'TestStgyValues'        
    if argTestCandle == None:
        #raise Exception('Параметр argTestCandle пустой')
        sqlParams = [Security, Period]
        cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+candTable+' WHERE Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 1', sqlParams)
        inData = cursor.fetchone()  #->()
        #TEST empty
    else:
        inData = argTestCandle
    sqlParams = [StgyCode, Security, Period, inData[0],inData[1],inData[2],inData[3],inData[4],inData[5], inData[1],inData[2],inData[3],inData[4],inData[5]]
    cursor.execute(' INSERT INTO '+stCandTable+' (Strategy, Security, TimeFrame, DateTime, Open, High, Low, Close, Volume) '+
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)  ON CONFLICT(Strategy,Security,TimeFrame,DateTime) DO UPDATE '+
        ' SET Open=?, High=?, Low=?, Close=?, Volume=? ', sqlParams)
    #stCandNum = cursor.rowcount
    connection.commit()
    
    currTime = inData[0]    
    sqlParams = [Class, Security]
    cursor.execute('SELECT Code, ShortName, Decimals, LotSize FROM Security WHERE Board=? AND Code=? ', sqlParams)
    secInfo = cursor.fetchone()  #->()
    sqlParams = [StgyCode, Security, Period]
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 21', sqlParams)
    stData = cursor.fetchall()  #->[()]
    #CalcValues            
    ma1 = 0
    ma2 = 0
    if len(stData)>=ma1period:
        for item in stData[:ma1period]:
            ma1 += item[4]
        ma1 = round(ma1/ma1period, secInfo[2])
    if len(stData)>=ma2period:
        for item in stData[:ma2period]:
            ma2 += item[4]
        ma2 = round(ma2/ma2period, secInfo[2])
    if ma1 == 0:
        ma1 = None
    if ma2 == 0:
        ma2 = None 
    sqlValues = [[StgyCode, currTime, 'MA1', ma1, ma1], [StgyCode, currTime, 'MA2', ma2, ma2]]
    #cursor.executemany('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value) VALUES (?, ?, ?, ?) ', sqlValues)
    cursor.executemany('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value) VALUES (?, ?, ?, ?) '+
        ' ON CONFLICT(Strategy, DateTime, Name) DO UPDATE SET Value=? ', sqlValues)
    connection.commit()
    #Curr Balance
    if argTestMode:
        sqlParams = [StgyCode, currTime, 'Bal']
        cursor.execute('SELECT Value FROM '+stValTable+' WHERE Strategy=? AND DateTime=? AND Name=?', sqlParams)
        currBalance = cursor.fetchone()
        if currBalance is None:
            currBalance=0

    #Trade Logic
    sqlParams = [StgyCode, Security, Period]
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 22', sqlParams)    
    stData = cursor.fetchall()  #->[()]
    if len(stData)>=ma2period+1:
        #MA Cross
        #sqlParams = [StgyCode, currTime, 'MA1']
        #cursor.execute('SELECT Value FROM '+stValTable+' WHERE Strategy=? AND DateTime=? AND Name=?', sqlParams)
        sqlParams = [StgyCode, 'MA1']
        cursor.execute('SELECT Value FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" DESC LIMIT 2', sqlParams)
        ma1val = cursor.fetchall()
        sqlParams = [StgyCode, 'MA2']
        cursor.execute('SELECT Value FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" DESC LIMIT 2', sqlParams)
        ma2val = cursor.fetchall()    
        if ma1val[1]<ma2val[1] and ma1val[0]>ma2val[0] and currBalance==0: 
            CreateOrder(1, StgyCode=StgyCode, currTime=currTime, stValTable=stValTable, cursor=cursor, TestMode=argTestMode)  #BuyOrder
        if ma1val[1]>ma2val[1] and ma1val[0]<ma2val[0] and currBalance>0:
            CreateOrder(-1, StgyCode=StgyCode, currTime=currTime, stValTable=stValTable, cursor=cursor, TestMode=argTestMode)  #SellOrder
        connection.commit()
        connection.close()

def CreateOrder(Qty, **Kwargs):
    if Qty == None:
        return
    cursor = Kwargs["cursor"]
    if Kwargs["TestMode"]: 
        if Qty==1:
            sqlValues = [Kwargs["StgyCode"], Kwargs["currTime"], 'Bal', Qty, Qty]
        if Qty==-1:
            sqlValues = [Kwargs["StgyCode"], Kwargs["currTime"], 'Bal', 0, 0]
        cursor.execute('INSERT INTO '+Kwargs["stValTable"]+' (Strategy, DateTime, Name, Value) VALUES (?, ?, ?, ?) '+
        ' ON CONFLICT(Strategy, DateTime, Name) DO UPDATE SET Value=? ', sqlValues)


def Test():
    StgyCode = '2MA_01'
    Security="SBER"
    Period = "H1"
    candTable = 'Candles'
    stCandTable = 'TestStgyCandles'
    stValTable = 'TestStgyValues'
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()      
    cursor.execute('DELETE FROM '+stCandTable+' WHERE Strategy="'+StgyCode+'"')
    cursor.execute('DELETE FROM '+stValTable+' WHERE Strategy="'+StgyCode+'"')
    connection.commit()
    sqlParams = [Security, Period]
    #LIMIT 200
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+candTable+' WHERE Security=? AND Timeframe=? ORDER BY "DateTime"  LIMIT 200 ', sqlParams)
    candleData = cursor.fetchall()    
    connection.close()
    for candle in candleData:
        OnRun(argTestCandle=candle, argTestMode=True)


def CreateReport(argTestMode=False):
    StgyCode = '2MA_01'
    Security="SBER"
    Period = "H1"
    ma1period = 9
    ma2period = 21    
    stCandTable = 'StgyCandles' 
    stValTable = 'StgyValues'
    if argTestMode:
        stCandTable = 'TestStgyCandles'
        stValTable = 'TestStgyValues'
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor() 
        
    HtmlReportMgt.AnychartStart(StgyCode+' '+Security+' '+Period)  #Title
    #Data
    sqlParams = [StgyCode, Security, Period]
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" ', sqlParams)
    stData = cursor.fetchall()    
    reportData = [list(item) for item in stData]
    HtmlReportMgt.AnychartAddChart(data=reportData, security=Security)
    cursor.execute('SELECT "DateTime", Value FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" ', [StgyCode, 'MA1'])
    valData = cursor.fetchall()
    valData = [list(item) for item in valData]    
    HtmlReportMgt.AnychartAddLine(id=1, data=valData)
    cursor.execute('SELECT "DateTime", Value FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" ', [StgyCode, 'MA2'])
    valData = cursor.fetchall()            
    valData = [list(item) for item in valData]
    HtmlReportMgt.AnychartAddLine(id=2, data=valData)

    connection.close()
    HtmlReportMgt.AnychartFinish("График Сбербанка")
    HtmlReportMgt.Show()


if __name__ == "__main__":
    #OnRun()
    Test()
    CreateReport(argTestMode=True)



