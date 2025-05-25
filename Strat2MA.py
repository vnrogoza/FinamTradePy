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

    def CreateOrder(Qty, Price):
        if Qty == None:
            return
        #cursor = Kwargs["cursor"]
        nonlocal cursor, stValTable, StgyCode, argTestMode
        if argTestMode: 
            if Qty==1:
                sqlValues = [StgyCode, currTime, 'Buy', Qty, Price]
            if Qty==-1:
                sqlValues = [StgyCode, currTime, 'Sell', Qty, Price]
            #cursor.execute('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value) VALUES (?, ?, ?, ?) '+
            #' ON CONFLICT(Strategy, DateTime, Name) DO UPDATE SET Value=? ', sqlValues)
            cursor.execute('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value, Value2) VALUES (?, ?, ?, ?, ?) ', sqlValues)

        
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
    
    currTime = inData[0]  #DateTime
    currPrice = inData[4]  #Close
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
    sqlValues = [StgyCode, currTime, 'MA', ma1, ma2]
    cursor.execute('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value, Value2) VALUES (?, ?, ?, ?, ?) ', sqlValues)
    #cursor.executemany('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value) VALUES (?, ?, ?, ?) '+
    #    ' ON CONFLICT(Strategy, DateTime, Name) DO UPDATE SET Value=? ', sqlValues)
    connection.commit()
    #Curr Balance
    if argTestMode:
        sqlParams = [StgyCode, currTime, 'Bal']
        #cursor.execute('SELECT Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND DateTime=? AND Name=?', sqlParams)
        cursor.execute('SELECT Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND DateTime<? AND Name=? ORDER BY DateTime DESC LIMIT 1', sqlParams)
        result  = cursor.fetchone()
        if result is None:
            currBalance = 0
            currBalPrice = 0
        else:    
            currBalance = result[0]
            currBalPrice = result[1]

    #Trade Logic
    sqlParams = [StgyCode, Security, Period]
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 22', sqlParams)    
    stData = cursor.fetchall()  #->[()]
    if len(stData)>=ma2period+1:
        #STRATEGY 2 MA Cross
        #sqlParams = [StgyCode, currTime, 'MA1']
        #cursor.execute('SELECT Value FROM '+stValTable+' WHERE Strategy=? AND DateTime=? AND Name=?', sqlParams)
        sqlParams = [StgyCode, 'MA']
        cursor.execute('SELECT Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" DESC LIMIT 2', sqlParams)
        maVal = cursor.fetchall()        
        #if ma1val[1]<ma2val[1] and ma1val[0]>ma2val[0] and currBalance==0: 
        if maVal[1][0]<maVal[1][1] and maVal[0][0]>maVal[0][1] and currBalance==0: 
            #CreateOrder(1, StgyCode=StgyCode, currTime=currTime, stValTable=stValTable, cursor=cursor, TestMode=argTestMode)  #BuyOrder
            CreateOrder(1, currPrice)  #BuyOrder
            currBalance = 1
            currBalPrice = currPrice
        if maVal[1][0]>maVal[1][1] and maVal[0][0]<maVal[0][1] and currBalance>0:
            #CreateOrder(-1, StgyCode=StgyCode, currTime=currTime, stValTable=stValTable, cursor=cursor, TestMode=argTestMode)  #SellOrder            
            CreateOrder(-1, currPrice)  #SellOrder         
            currBalance = 0
            currBalPrice = 0
        sqlValues = [StgyCode, currTime, 'Bal', currBalance, currBalPrice]
        cursor.execute('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value, Value2) VALUES (?, ?, ?, ?, ?) ', sqlValues)

        connection.commit()
        connection.close()



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
    #Lines
    cursor.execute('SELECT "DateTime", Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" ', [StgyCode, 'MA'])
    valData = cursor.fetchall()
    valData1 = [list([item[0], item[1]]) for item in valData]
    HtmlReportMgt.AnychartAddLine(id=1, data=valData1, color="#ff3300")
    valData2 = [list([item[0], item[2]]) for item in valData]
    HtmlReportMgt.AnychartAddLine(id=2, data=valData2, color="#4444ff")
    #Orders
    id = 0
    cursor.execute('SELECT "DateTime", Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" ', [StgyCode, 'Buy'])
    valData = cursor.fetchall()
    for item in valData:
        HtmlReportMgt.AnychartAddOrder(id=id, time=item[0], price=item[2], type='Buy')
        id += 1
    cursor.execute('SELECT "DateTime", Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" ', [StgyCode, 'Sell'])
    valData = cursor.fetchall()
    for item in valData:
        HtmlReportMgt.AnychartAddOrder(id=id, time=item[0], price=item[2], type='Sell')
        id += 1
    #Trades
    cursor.execute('SELECT "DateTime", Name, Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND Name IN ("Buy","Sell","Bal") ORDER BY "DateTime" ', StgyCode)
    valData = cursor.fetchall()
    balQty = 0
    balAmound = 0
    tradeQty = 0
    tradeAmount = 0
    for item in valData:
        name = item[1]
        qty = int(item[2])
        price = item[3]
        if name == 'Bal':
            bal = qty
        if name == 'Buy':
            tradeQty = qty
            tradeAmount = price
            '''
            --SELECT * FROM TestStgyValues WHERE Name IN ("Buy","Sell","Bal") ORDER BY "DateTime"
SELECT V1.DateTime, V1.Name, V1.Value, V1.Value2, V2.Name, V2.Value, V2.Value2 FROM TestStgyValues V1 
  LEFT JOIN TestStgyValues V2 ON V2.Strategy=V1.Strategy AND V2.DateTime=V1.DateTime AND V2.Name IN ("Buy","Sell")
  WHERE V1.Strategy="2MA_01" AND V1.Name = "Bal"
  --ORDER BY "DateTime"
            '''

    #HtmlReportMgt.AnychartAddOrder(id=id, time=item[0], price=item[2], type='Sell')
    


    connection.close()
    HtmlReportMgt.AnychartFinish("График Сбербанка")
    HtmlReportMgt.Show()


if __name__ == "__main__":
    #OnRun()
    Test()
    CreateReport(argTestMode=True)



