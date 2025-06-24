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


    '''
    for candle in CandleTable:    
        #['CNYRUB_TOM', 'D1', datetime.datetime(2024, 5, 10, 0, 0), 12.6255, 12.6975, 12.6135, 12.692, 2100703000]
        #candle = [security, timeframe, T, O, H, L, C, V]    
        #item = [i, candle[5], candle[3], candle[6], candle[4]]
        item = [candle[2], candle[5], candle[3], candle[6], candle[4]]
        data.append(item)

    HtmlReportHelper.Start()
    HtmlReportHelper.AddChart("chart_div", data, 'CNY_RUB')
    HtmlReportHelper.Finish()
    HtmlReportHelper.Show()
    '''

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
    GetCandleData()