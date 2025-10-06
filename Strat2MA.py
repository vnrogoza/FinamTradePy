#Стратегия 2МА
#RunOnce() - одна свеча
#Test() - прогон на исторических данных
#CreateReport() - формирование отчёта
import sqlite3, HtmlReportMgt, OrderMgt, AccountMgt

def RunOnce(Candle, TestMode=False):
    if Candle==None:
        raise Exception('Candle-param is empty')    
    if type(Candle[0]) == list:
        raise Exception('Candle-param has more 1 items or [[]]')
    retValue = ''
    #Candle=() - use it, argTestCandle=None - from table
    #[Security, Timeframe, "DateTime", Open, High, Low, Close, Volume]
    # 0         1           2          3     4     5    6      7
    #TestMode - table names    
    #Strategy params
    StgyCode = '2MA_01'
    Class="MISX"    
    #Account="L01+00000F00"
    Account="1908434"
    Security="GAZP"
    orderQty = 10
    Period = "M5"
    ma1period = 9
    ma2period = 21
    

    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor() 

    
    candTable = 'Candles' 
    stCandTable = 'StgyCandles' 
    stValTable = 'StgyValues'
    if TestMode:
        stCandTable = 'StgyTestCandles'
        stValTable = 'StgyTestValues'

    #LastCandle    
    sqlParams = [Security, Period]
    cursor.execute('SELECT [DateTime] FROM '+stCandTable+' WHERE Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 1', sqlParams)
    lastCandle = cursor.fetchone()    
    if lastCandle is not None:
        lastCandleDT = lastCandle[0]
        currCandelDT = Candle[2]
        if currCandelDT <= lastCandleDT:
            connection.close()
            return 'No action (no new candles)'
        
    sqlParams = [Class, Security]
    cursor.execute('SELECT Code, ShortName, Decimals, LotSize FROM Security WHERE Board=? AND Code=? ', sqlParams)
    secInfo = cursor.fetchone()  #->()
    if secInfo is None:
        raise Exception('Instrument info is not found')        

    inData = Candle
    #sqlParams = [StgyCode, Security, Period, inData[0],inData[1],inData[2],inData[3],inData[4],inData[5], inData[1],inData[2],inData[3],inData[4],inData[5]]
    sqlParams = [StgyCode, inData[0],inData[1],inData[2],inData[3],inData[4],inData[5],inData[6],inData[7]]
    cursor.execute(' INSERT INTO '+stCandTable+' (Strategy, Security, TimeFrame, DateTime, Open, High, Low, Close, Volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ', sqlParams)
    #stCandNum = cursor.rowcount
    connection.commit()
    
    currTime = inData[2]  #DateTime
    currPrice = inData[6]  #Close

    sqlParams = [StgyCode, Security, Period]
    cursor.execute('SELECT Security, Timeframe, "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 21', sqlParams)
    stData = cursor.fetchall()  #->[()]
    
    #CalcValues            
    ma1 = 0
    ma2 = 0
    if len(stData)>=ma1period:
        for item in stData[:ma1period]:
            #Переделать свечки на Класс чтобы не думать об этом
            ma1 += item[6]
        ma1 = round(ma1/ma1period, secInfo[2])
    if len(stData)>=ma2period:
        for item in stData[:ma2period]:
            ma2 += item[6]
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
    currBalance = 0
    currBalPrice = 0
    if TestMode:
        sqlParams = [StgyCode, currTime, 'Bal']        
        cursor.execute('SELECT Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND DateTime<? AND Name=? ORDER BY DateTime DESC LIMIT 1', sqlParams)
        result  = cursor.fetchone()
        if result is None:
            currBalance = 0
            currBalPrice = 0
        else:    
            currBalance = result[0]
            currBalPrice = result[1]
    else:
        CurrPosition = AccountMgt.GetCurrentPosition(account_id=Account, security_id=Security+'@'+Class)
        currBalance = CurrPosition["quantity"]
        currBalPrice = CurrPosition["avgprice"]

    #Trade Logic
    retValue = 'No action'
    sqlParams = [StgyCode, Security, Period]
    #This SELECT only for what?
    cursor.execute('SELECT Security, Timeframe, "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 22', sqlParams)    
    stData = cursor.fetchall()  #->[()]
    if len(stData)>=ma2period:
        #STRATEGY 2 MA Cross
        #sqlParams = [StgyCode, currTime, 'MA1']
        #cursor.execute('SELECT Value FROM '+stValTable+' WHERE Strategy=? AND DateTime=? AND Name=?', sqlParams)
        sqlParams = [StgyCode, 'MA']
        cursor.execute('SELECT Value, Value2 FROM '+stValTable+' WHERE Strategy=? AND Name=? ORDER BY "DateTime" DESC LIMIT 2', sqlParams)
        maVal = cursor.fetchall()
        if len(maVal) == 2:            
            #Long Open        
            newMA1 = maVal[0][0]; newMA2 = maVal[0][1]; oldMA1 = maVal[1][0]; oldMA2 = maVal[1][1]
            #if maVal[1][0]<maVal[1][1] and maVal[0][0]>maVal[0][1] and currBalance==0: 
            if oldMA1<=oldMA2 and newMA1>newMA2 and currBalance==0:
                #CreateOrder(1, StgyCode=StgyCode, currTime=currTime, stValTable=stValTable, cursor=cursor, TestMode=argTestMode)  #BuyOrder            
                #CreateOrder(orderQty, currPrice, Params=OrderParams)  
                #BuyOrder
                CreateOrder(orderQty, currPrice, cursor=cursor, TestMode=TestMode, 
                            account_id=Account, security_id=Security+'@'+Class,
                            StgyCode=StgyCode, stValTable=stValTable, order_time=currTime)
                currBalance = orderQty
                currBalPrice = currPrice                
                retValue = f'Buy order: Q={orderQty} P={currPrice}'
            #Long Close
            #if maVal[1][0]>maVal[1][1] and maVal[0][0]<maVal[0][1] and currBalance>0:
            if oldMA1>=oldMA2 and newMA1<newMA2 and currBalance>0:
                #CreateOrder(-1, StgyCode=StgyCode, currTime=currTime, stValTable=stValTable, cursor=cursor, TestMode=argTestMode)  #SellOrder            
                #CreateOrder(-currBalance, currPrice, Params=OrderParams)  
                #SellOrder 
                CreateOrder(-currBalance, currPrice, cursor=cursor, TestMode=TestMode,
                            account_id=Account, security_id=Security+'@'+Class,
                            StgyCode=StgyCode, stValTable=stValTable, order_time=currTime)                            
                currBalance = 0
                currBalPrice = 0
                retValue = f'Sell order: Q={orderQty} P={currPrice}'
            
        sqlValues = [StgyCode, currTime, 'Bal', currBalance, currBalPrice]
        cursor.execute('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value, Value2) VALUES (?, ?, ?, ?, ?) ', sqlValues)
        connection.commit()
        connection.close()
        return retValue


def Test():
    StgyCode = '2MA_01'
    Security="GAZP"
    Period = "M5"
    candTable = 'Candles'    
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()      
    cursor.execute('DELETE FROM StgyTestCandles WHERE Strategy="'+StgyCode+'"')
    cursor.execute('DELETE FROM StgyTestValues WHERE Strategy="'+StgyCode+'"')
    connection.commit()
    #Update candles
    import MarketMgt
    SecurityCandleTable = [["MISX",Security,Period,'2025-09-28','2025-09-30 23:50',None,'W']]
    CandleTable = MarketMgt.LoadCandels(SecurityCandleTable)
    res = SaveToDB(CandleTable)
    if __name__ == "__main__":
        print(res)
    #LIMIT 200
    sqlParams = [Security, Period, 200]
    cursor.execute('SELECT * FROM (SELECT Security, Timeframe, "DateTime", Open, High, Low, Close, Volume FROM '+candTable+' WHERE Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT ?) ORDER BY "DateTime"  ', sqlParams)
    candleData = cursor.fetchall()    
    connection.close()    
    for candle in candleData:        
        RunOnce(Candle=candle, TestMode=True)


def Run():
    StgyCode = '2MA_01'
    Security="GAZP"
    Period = "M5"  
    RetValue = ''  
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()
    sqlParams = [Security, Period]
    cursor.execute('SELECT COUNT(*) FROM StgyCandles WHERE Security=? AND Timeframe=?', sqlParams)
    result = cursor.fetchone() 
    if result[0] < 21:
        cursor.execute('DELETE FROM StgyCandles WHERE Strategy="'+StgyCode+'"')
        cursor.execute('DELETE FROM StgyValues WHERE Strategy="'+StgyCode+'"')
        sqlParams = [StgyCode, Security, Period, 21]
        cursor.execute('INSERT INTO StgyCandles (Strategy, Security, Timeframe, "DateTime", Open, High, Low, Close, Volume) '+
                       'SELECT ?, Security, Timeframe, "DateTime", Open, High, Low, Close, Volume '+
                       'FROM (SELECT Security, Timeframe, "DateTime", Open, High, Low, Close, Volume FROM '+
                       'Candles WHERE Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT ?) ORDER BY "DateTime" ', sqlParams)
        connection.commit()
        RetValue += '\n Tables was refreshed'
        
    sqlParams = [Security, Period, 1]
    cursor.execute('SELECT * FROM (SELECT Security, Timeframe, "DateTime", Open, High, Low, Close, Volume FROM Candles WHERE Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT ?) ORDER BY "DateTime"  ', sqlParams)
    candleData = cursor.fetchone()
    connection.close()
    RetValue += '\n '+str(candleData)
    result = RunOnce(Candle=candleData)
    RetValue += '\n '+str(result)
    return RetValue
        
def CreateReport(TestMode=False, StartEquity=10000):
    StgyCode = '2MA_01'
    Class="MISX"
    Security="GAZP"
    Period = "M5"
    ma1period = 9
    ma2period = 21    
    stCandTable = 'StgyCandles' 
    stValTable = 'StgyValues'
    if TestMode:
        stCandTable = 'StgyTestCandles'
        stValTable = 'StgyTestValues'
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor() 
    sqlParams = [Class, Security]
    cursor.execute('SELECT Code, ShortName, Decimals, LotSize FROM Security WHERE Board=? AND Code=? ', sqlParams)
    secInfo = cursor.fetchone()  #->()
        
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
    cursor.execute('SELECT V1."DateTime", V1.Name, V1.Value, V1.Value2, V2.Name, V2.Value, V2.Value2 FROM '+stValTable+' V1 '+
        ' LEFT JOIN StgyTestValues V2 ON V2.Strategy=V1.Strategy AND V2."DateTime"=V1."DateTime" AND V2.Name IN ("Buy","Sell") '+
        ' WHERE V1.Strategy=? AND V1.Name = "Bal" ORDER BY V1."DateTime" ', [StgyCode] )
    valData = cursor.fetchall()
    connection.close()
    balQty = 0
    balAmound = 0    
    tradeAmount = 0
    tradeData=[]
    equity = StartEquity
    equityMax = 0
    equityMin = StartEquity
    StartEquity
    equityData=[]    
    for item in valData:  
        #every time        
        balQty = int(item[2])  #0/1
        balPrice = item[3]  #0/123
        order =  item[4]  #null/Buy/Sell
        orderQty = item[5]  #null/1/-1
        orderPrice = item[6]  #null/123
        if order=='Buy' and balQty>0:
            balAmound = balQty * balPrice
        if order=='Sell' and balQty==0:
            tradeAmount = abs(orderQty)*orderPrice - balAmound
            tradeAmount = round(tradeAmount, secInfo[2])
            equity += tradeAmount            
            if tradeAmount>=0:
                tradeData.append({"x":item[0], "value":tradeAmount, "value2":None})
            else:
                tradeData.append({"x":item[0], "value":None, "value2":tradeAmount})    
            #[{x:'2025-04-04 23:00', value:105000}]                
            equityData.append({"x":item[0], "value":equity})
            if equity < equityMin:
                equityMin = equity
            if equity > equityMax:
                equityMax = equity
    HtmlReportMgt.AnychartAddTrades(id=2, data=tradeData)    
    HtmlReportMgt.AnychartEndChart(StgyCode+'  '+Security+'  '+Period)
    #Equity
    HtmlReportMgt.AnychartAddColumnChart(id=2, data=equityData, maxY=equityMax*1.01, minY=equityMin*0.99)
    HtmlReportMgt.Finish()
    HtmlReportMgt.Show()


def SaveToDB(CandleTable):
    import BaseMgt
    counter = 0
    dataParts = BaseMgt.SplitListByLenth(CandleTable, 1000)
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()    
    for part in dataParts:               
        cursor.executemany('INSERT OR IGNORE INTO Candles (Security, TimeFrame, DateTime, Open, High, Low, Close, Volume, Date, Time, ModifyDT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "", "", datetime("now","localtime"))', part)
        #['CNYRUB_TOM', 'D1', '2025-03-03', 12.14, 12.256, 12.087, 12.0945, 9012011000]    
        counter += cursor.rowcount
        connection.commit()
    connection.close()    
    retValue = str(counter)+' lines were updated'
    return retValue


def CreateOrder(Qty, Price, **Params):
    if Qty in (0,None):
        raise Exception('Wrong Qty param')
    if Price in (0,None):
        raise Exception('Wrong Price param')            
    if Params == None:
        raise Exception('Params expected')            
    #cursor = Kwargs["cursor"]
    #nonlocal cursor, stValTable, StgyCode, TestMode
    TestMode = Params['TestMode']
    cursor = Params['cursor']    
    stValTable = Params['stValTable']
    StgyCode = Params['StgyCode']
    currTime = Params['order_time']    
    if Qty>0:
        sqlValues = [StgyCode, currTime, 'Buy', Qty, Price]
    if Qty<0:
        sqlValues = [StgyCode, currTime, 'Sell', Qty, Price]
    #cursor.execute('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value) VALUES (?, ?, ?, ?) '+
    #' ON CONFLICT(Strategy, DateTime, Name) DO UPDATE SET Value=? ', sqlValues)
    cursor.execute('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value, Value2) VALUES (?, ?, ?, ?, ?) ', sqlValues)
    if not TestMode:
        if Qty>0:
            OrderMgt.CreateOrder(account_id=Params['account_id'], symbol=Params['security_id'], quantity=Qty, side=OrderMgt.Side.BUY,
                                type=OrderMgt.OrderType.MARKET)
        if Qty<0:
            OrderMgt.CreateOrder(account_id=Params['account_id'], symbol=Params['security_id'], quantity=abs(Qty), side=OrderMgt.Side.SELL,
                                type=OrderMgt.OrderType.MARKET)            


if __name__ == "__main__":    
    #Test()    
    CreateReport()
    #result = Run()
    #print(result)
