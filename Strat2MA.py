#Стратегия 2МА
#OnRun() - одна свеча
#Test() - прогон на исторических данных
#CreateReport() - формирование отчёта
import sqlite3, HtmlReportMgt
testMode = False

def OnRun(argTestCandle=None):    
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
    global testMode
        
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor() 
        
    #LastCandle   
    if testMode:
        if argTestCandle == None:
            raise Exception('Параметр argTestCandle пустой')
        stCandTable = 'TestStgyCandles' 
        stValTable = 'TestStgyValues' 
        
        sqlParams = [StgyCode, Security, Period]
        cursor.execute('SELECT COUNT(1) FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ', sqlParams)
        stCandNum = cursor.fetchone()[0]

        inData = argTestCandle
    else:  
        #Prepare
        sqlParams = [Security, Period]
        cursor.execute('SELECT COUNT(1) FROM '+candTable+' WHERE Security=? AND Timeframe=? ', sqlParams)
        inpCandNum = cursor.fetchone()[0]
        if inpCandNum < ma2period:
            raise Exception('Недостаточно данных в таблице '+candTable)

        sqlParams = [StgyCode, Security, Period]
        cursor.execute('SELECT COUNT(1) FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ', sqlParams)
        stCandNum = cursor.fetchone()[0]
        if stCandNum == 0:
            sqlParams = [StgyCode, Security, Period]
            cursor.execute(''' INSERT INTO StgyCandles (Strategy, Security, TimeFrame, DateTime, Open, High, Low, Close, Volume) 
                SELECT ?, Security, TimeFrame, DateTime, Open, High, Low, Close, Volume FROM Candles 
                WHERE Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 21''', sqlParams)
            stCandNum = cursor.rowcount
            connection.commit()
        if stCandNum < ma2period:             
            raise Exception('Недостаточно данных в таблице '+stCandTable)

        sqlParams = [Security, Period]
        cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+candTable+' WHERE Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 1', sqlParams)
        inData = cursor.fetchone()  #->()    
    #LastStgyCandle
    sqlParams = [StgyCode, Security, Period]
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 1', sqlParams)
    stData = cursor.fetchone()  #->()
    if stData == None:
        stData = ['',0,0,0,0,0]


    if inData[0]>stData[0]:  #new interval
        currTime = inData[0]
        sqlParams = [StgyCode, Security, Period, inData[0], inData[1], inData[2], inData[3], inData[4], inData[5]]
        cursor.execute('INSERT INTO '+stCandTable+' (Strategy, Security, TimeFrame, DateTime, Open, High, Low, Close, Volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) ', sqlParams)
        sqlParams = [Class, Security]
        cursor.execute('SELECT Code, ShortName, Decimals, LotSize FROM Security WHERE Board=? AND Code=? ', sqlParams)
        secInfo = cursor.fetchone()  #->()
        sqlParams = [StgyCode, Security, Period]
        cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+stCandTable+' WHERE Strategy=? AND Security=? AND Timeframe=? ORDER BY "DateTime" DESC LIMIT 21', sqlParams)
        stData = cursor.fetchall()  #->[()]        
        #CalcValues            
        if stCandNum>=ma1period:
            m1 = 0
            m2 = 0
            for item in stData[:ma1period]:
                m1 += item[4]
            m1 = round(m1/ma1period, secInfo[2])
            if stCandNum>=ma2period:
                for item in stData[:ma2period]:
                    m2 += item[4]
                m2 = round(m2/ma2period, secInfo[2])
            if m1 == 0:
                m1 = None
            if m2 == 0:
                m2 = None 
            sqlValues = [[StgyCode, currTime, 'MA1', m1], [StgyCode, currTime, 'MA2', m2]]
            cursor.executemany('INSERT INTO '+stValTable+' (Strategy, DateTime, Name, Value) VALUES (?, ?, ?, ?) ', sqlValues)
            #Curr Balance

            #Trade Logic

    connection.commit()
    connection.close()

def Test():        
    global testMode
    testMode = True
    Security="SBER"
    Period = "H1"
    candTable = 'Candles'
    connection = sqlite3.connect('DB\\finam.db')
    cursor = connection.cursor()  
    sqlParams = [Security, Period]
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+candTable+' WHERE Security=? AND Timeframe=? ORDER BY "DateTime"', sqlParams)
    cursor.execute('SELECT "DateTime", Open, High, Low, Close, Volume FROM '+candTable+' WHERE Security=? AND Timeframe=? ORDER BY "DateTime"', sqlParams)
    candleData = cursor.fetchall()    
    connection.close()
    for candle in candleData:
        OnRun(candle)


def CreateReport():
    StgyCode = '2MA_01'    
    Security="SBER"
    Period = "H1"
    ma1period = 9
    ma2period = 21    
    stCandTable = 'StgyCandles' 
    stValTable = 'StgyValues' 
    testMode = True 
    if testMode:    
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
    #Test()
    CreateReport()
