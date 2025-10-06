#Загрузка свечек за период и вывод на график
def Test():
    import MarketMgt, HtmlReportMgt

    SecurityCandleTable = [["MISX","GAZP","M5", None, None, 10,'W']]
    #SecurityCandleTable = [["MISX","GAZP","D1",'2025-08-16','2025-09-24',None,'W']]        
    CandleTable = MarketMgt.LoadCandels(SecurityCandleTable)
    #for candle in CandleTable[-2:-1]:  #Только предпоследняя
    #for candle in CandleTable[:-1]:  #Все кроме предпоследней
    data = []
    data.append(['T','GAZP','O','C','H'])
    for candle in CandleTable:   
        item = [candle[2], float(candle[5]), float(candle[3]), float(candle[6]), float(candle[4])]  #T,LOCH
        data.append(item)
    HtmlReportMgt.Start()
    HtmlReportMgt.AddChart("chart_div", data, 'Sberbank')    
    HtmlReportMgt.Finish()
    HtmlReportMgt.Show()


#ДЛЯ АВТОЗАДАНИЙ. Получение данных и загрузка в БД - последние свечки. 
def GetCandleDataV3(timeframe=None):
    #Загрузка исторических данных (свечек) в БД
    import MarketMgt
    import sqlite3
    retValue = ''; counter = 0

    #Load Security list from DB    
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()
    if timeframe is None:
        cursor.execute('SELECT Board, Security, TimeFrame, DateFrom, DateTo, Quantity FROM SecurityList WHERE Active = 1')
    else:
        if not timeframe in ['W1','D1','H1','M15','M5']:
            raise Exception('Wrong timeframe')
        cursor.execute('SELECT Board, Security, TimeFrame, DateFrom, DateTo, Quantity FROM SecurityList WHERE Active = 1 AND TimeFrame = "'+timeframe+'"')
    result = cursor.fetchall()    
    if len(result) == 0:        
        raise Exception('SecurityCandle table result is emmpty')
    
    #Load Candle 
    for line in result:    
        SecurityCandleTable =[[line[0],line[1],line[2],line[3],line[4],line[5],'']]
        retValue = '\n '+str(SecurityCandleTable)      
        CandleTable = MarketMgt.LoadCandels(SecurityCandleTable)    
        cursor.executemany('INSERT OR IGNORE INTO Candles (Security, TimeFrame, DateTime, Open, High, Low, Close, Volume, Date, Time, ModifyDT) VALUES (?, ?, ?, ?, ?, ?, ?, ?, "", "", datetime("now","localtime"))', CandleTable)        
        counter += cursor.rowcount
    #Finish    
    connection.commit()
    connection.close()    
    retValue += '\n '+str(counter)+' lines were updated'
    return retValue


#Получение данных и загрузка в БД. 
def GetCandleDataV2(timeframe=None):
    #Загрузка исторических данных (свечек) в БД
    import MarketMgt, BaseMgt
    import sqlite3
    retValue = ''

    #Empty tables
    SecurityCandleTable = []
    CandleTable = []
    
    #Load Security list from DB    
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()
    if timeframe is None:
        cursor.execute('SELECT Board, Security, TimeFrame, DateFrom, DateTo, Quantity FROM SecurityList WHERE Active = 1')
    else:
        if not timeframe in ['W1','D1','H1','M15','M5']:
            raise Exception('Wrong timeframe')
        cursor.execute('SELECT Board, Security, TimeFrame, DateFrom, DateTo, Quantity FROM SecurityList WHERE Active = 1 AND TimeFrame = "'+timeframe+'"')
    result = cursor.fetchall()
    connection.close()
    for line in result:    
        SecurityCandleTable.append([line[0],line[1],line[2],line[3],line[4],line[5],'']) 
    retValue = str(SecurityCandleTable)
    if len(SecurityCandleTable) == 0:        
        raise Exception('SecurityCandleTable is emmpty')
        
    #Load Candle 
    CandleTable = MarketMgt.LoadCandels(SecurityCandleTable)

    #Save
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
    retValue += '\n '+str(counter)+' lines were updated'
    return retValue
    


def GetCandleData():
    #Загрузка исторических данных (свечек) в БД
    import MarketMgt, BaseMgt
    import sqlite3

    #Empty tables
    SecurityCandleTable = []
    CandleTable = []

    #board,security,timeframe,datefrom,dateto,num,flag (1,W)
    SecurityCandleTable = [["CETS","CNYRUB_TOM","D1",'2025-03-01','2025-03-31',None,'W']]


    #Load Security list from filee
    #secFileName = "DB\\SecurityCandle.txt"
    #SecurityCandleTable = SecurityCandle.LoadSecurityCandle(secFileName)

    #Load Security list from DB
    SecurityCandleTable = []
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Board, Security, TimeFrame, DateFrom, DateTo, Quantity FROM SecurityList WHERE Active = 1')
    result = cursor.fetchall()
    connection.close()
    for line in result:    
        SecurityCandleTable.append([line[0],line[1],line[2],line[3],line[4],line[5],''])
    #print(SecurityCandleTable)
    print(SecurityCandleTable)

    if len(SecurityCandleTable) == 0:
        print('SecurityCandleTable is emmpty')
        quit()

    #Load Candle tablepip
    CandleTable = MarketMgt.LoadCandels(SecurityCandleTable)

    print("Save data to DB...")
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
    print(counter, 'lines were updated')


if __name__ == "__main__":    
    #GetCandleDataV2()
    #Test()
    RetValue = GetCandleDataV3("M5")
    print(RetValue)