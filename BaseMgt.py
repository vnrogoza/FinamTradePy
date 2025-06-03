title = "Привет"
def start():
  print("Starting...")

def LoadToken():
  file = open("token.txt", "r")
  token = file.readline()
  return token

def LoadJwtToken():
  file = open("tokenjwt.txt", "r")
  date = file.readline()
  token = file.readline()
  file.close
  return date,token

def SaveJwtToken(date, token):
  file = open("tokenjwt.txt", "w")  
  file.write(date)
  file.write(token)
  file.close

def RefreshToken(client):    
    from datetime import datetime 
    if client == None:
      raise('Client is not innitialized')      
    
    renew = False
    validTime = None    
    client.access_tokens.get_jwt_token()
    try:
        resp = client.access_tokens.get_jwt_token_details()        
        validTime = Utc2Loc(str(resp.expiresAt)) 
        nowTime = str(datetime.now())
        if nowTime > validTime:
            renew = True
    except Exception as e:
        if str(e).find('Token is expired'):
            renew = True
        else:
            raise(e)        
    if renew:
        print(f'Token is expired ({validTime}). New token released')
        client.access_tokens.set_jwt_token()
    else:
        print(f'Token is valid till {validTime}')


def DateInterval(argDatetime0, argDatetime1, argTimeFrame):
  from datetime import datetime, timedelta
  argDatetime0 = datetime.fromisoformat(argDatetime0)
  argDatetime1 = datetime.fromisoformat(argDatetime1)
  if argDatetime0 > argDatetime1:
    print("DateDiff: First date must be smaller then second")
    return None
  if argTimeFrame not in  ["M5","M15","H1","D1","W1"]:
    print("DateDiff: Wrong timeframe")
    return None
  #Индекс 10-18
  #Валюта  7-18
  #Акции1 10-23
  #Акции2 10-18
  #Фьючер  9-23

  m1sec = 60
  m5sec = m1sec*5
  m15sec = m1sec*15
  h1sec = m1sec*60
  d1sec = h1sec*24
  dayHrs = 14  #в 1 дне максимум 14 часов
  dayH1 = dayHrs * 1
  dayM15 = dayH1 * 4
  dayM5 = dayH1 * 12  
  delta = argDatetime1 - argDatetime0    
  if argTimeFrame == "W1":
    return delta.days//7
  #Считаем количество рабочих дней  
  holidays = [datetime(2023, 3, 8)]  
  currDate = argDatetime0.date()
  workDays = 0
  currDate += timedelta(days=1)
  while currDate <= argDatetime1.date():
    if currDate.weekday() < 5 and currDate not in holidays:
        workDays += 1
    currDate += timedelta(days=1)      
  if argTimeFrame == "M5":
    retValue = workDays * dayM5
    retValue = retValue + delta.seconds//m5sec
  if argTimeFrame == "M15":
    retValue = workDays * dayM15
    retValue = retValue + delta.seconds//m15sec
  if argTimeFrame == "H1":
    retValue = workDays * dayH1  #delta.days
    retValue = retValue + delta.seconds//h1sec
  if argTimeFrame == "D1":
    retValue = workDays+1  #7.12 - 6.12 = 2д
  return retValue

def DateAdd(argDatetime, argInterval, argTimeFrame):
  from datetime import datetime, timedelta
  if argInterval == 0:
    raise Exception("DateAdd: Wrong interval value")
    return None
  if argTimeFrame not in  ["M5","M15","H1","D1","W1"]:
    raise Exception("DateAdd: Wrong timeframe")
    return None  
  holidays = [datetime(2023, 3, 8)]
  workDays = [0,1,2,3,4]
  workHours = range(10, 24)  
  #currDate = argDatetime
  currDate = datetime.fromisoformat(argDatetime)
  i = 0  
  if argInterval > 0:
    while i < argInterval:
      if argTimeFrame == "M5":
        currDate += timedelta(minutes=5)
      if argTimeFrame == "M15":
        currDate += timedelta(minutes=15)
      if argTimeFrame == "H1":
        currDate += timedelta(hours=1)
      if argTimeFrame == "D1":
        currDate += timedelta(days=1)
      if argTimeFrame in  ["M5","M15","H1"]:
        if (currDate.weekday() in workDays) and (currDate not in holidays) and (currDate.hour in workHours):
          i += 1
      if argTimeFrame == "D1":
        if (currDate.weekday() in workDays) and (currDate not in holidays):
          i += 1
      if argTimeFrame == "W1":
        i += 1
        #print(i, currDate, currDate.weekday())
  if argInterval < 0:
    while i > argInterval:
      if argTimeFrame == "M5":
        currDate -= timedelta(minutes=5)
      if argTimeFrame == "M15":
        currDate -= timedelta(minutes=15)
      if argTimeFrame == "H1":
        currDate -= timedelta(hours=1)
      if argTimeFrame == "D1":
        currDate -= timedelta(days=1)
      if argTimeFrame in  ["M5","M15","H1"]:
        if (currDate.weekday() in workDays) and (currDate not in holidays) and (currDate.hour in workHours):
          i -= 1
      if argTimeFrame == "D1":
        if (currDate.weekday() in workDays) and (currDate not in holidays):
          i -= 1 
        #print(i, currDate, currDate.weekday())
      if argTimeFrame == "W1":        
        i -= 1 
  #return str(currDate)
  ct = currDate
  if argTimeFrame in ["D1","W1"]:    
    return str(datetime(ct.year, ct.month, ct.day))[0:10]
  if argTimeFrame in ["M5","M15","H1"]:    
    return str(datetime(ct.year, ct.month, ct.day, ct.hour, ct.minute))

def DateNow(argTimeFrame):
  if argTimeFrame not in  ["M5","M15","H1","D1","W1"]:
      raise Exception("DateNow: Wrong timeframe")      
  from datetime import datetime
  ct = datetime.now()
  if argTimeFrame in ["D1","W1"]:
    #return datetime(ct.year, ct.month, ct.day)
    return str(datetime(ct.year, ct.month, ct.day))[0:10]
  if argTimeFrame in ["M5","M15","H1"]:
    #return datetime(ct.year, ct.month, ct.day, ct.hour)
    if argTimeFrame=="H1":
      ctm = 0
    elif argTimeFrame=="M15":
      ctm = (ct.minute//15)*15
    elif argTimeFrame=="M5":
      ctm = (ct.minute//5)*5
    return str(datetime(ct.year, ct.month, ct.day, ct.hour, ctm))[0:16]
  
def Utc2Loc(argDateTime):
  from datetime import datetime, timezone
  ##timestamp - дата и время свечи в формате yyyy-MM-ddTHH:mm:ssZ в поясе UTC
  if len(argDateTime)>10:
    T = argDateTime.rstrip('Z')
    T = datetime.fromisoformat(T)
    T = T.replace(tzinfo=timezone.utc) 
    T = T.astimezone() 
    T = str(T)[:16]
    return T
  return argDateTime

def Loc2Utc(argDateTime):
  from datetime import datetime, timezone
  ##timestamp - дата и время свечи в формате yyyy-MM-ddTHH:mm:ssZ в поясе UTC
  if len(argDateTime)>10:    
    T = datetime.fromisoformat(argDateTime)
    T = T.astimezone(timezone.utc)  #2025-05-09 09:45:39+00:00  
    T = str(T).replace(' ','')  #2025-06-0117:47:00+00:00
    T = T[:10]+'T'+T[10:18]+'Z'
    return T
  return argDateTime


def GetDateIntervals(argFromDate, argToDate, argTimeframe, argQuantity):
    from  datetime import datetime, timedelta
    if argFromDate is None:
      argFromDate=''
    if argToDate is None:
      argToDate=''
    if argQuantity is None:
      argQuantity=0
    if argFromDate=='' and argToDate=='' and argQuantity==0:
      return
    if argTimeframe not in ['M5','M15','H1','D1','W1']:
      return
    
    #Максимальное значение count 500 штук
    #Для дневных свечей максимальный интервал 365 дней
    #Для внутридневных свечей максимальный интервал 30 дней
    seriesLenth = {'W1':40,'D1':200,'H1':300,'M15':400,'M5':400}
    seriesDelta = {'W1':timedelta(weeks=40),'D1':timedelta(days=200),'H1':timedelta(hours=300),'M15':timedelta(minutes=15)*400,'M5':timedelta(minutes=5)*400}
    timeFrameDelta = {'W1':timedelta(weeks=1),'D1':timedelta(days=1),'H1':timedelta(hours=1),'M15':timedelta(minutes=15),'M5':timedelta(minutes=5)}        
    oneDelta = timeFrameDelta[argTimeframe]  #timedelta: 1-hour
    resultRange = []
    if argFromDate!='' and argToDate!='':      
      argFromDate = datetime.fromisoformat(argFromDate)
      argToDate = datetime.fromisoformat(argToDate)      
      totalLenth = argToDate - argFromDate  #timedelta: N-days L-hours M-minutes
      if totalLenth < 0:
        return
      interval = seriesDelta[argTimeframe]  #timedelta: 300-hours   
      k, m = divmod(totalLenth, interval)  #k-частное, m-остаток      
      #Основные блоки
      for i in range(k):        
        d0 = argFromDate+(i*interval)
        d1 = argFromDate+((i+1)*interval)        
        #print(d0,'->',d1,'=',d1-d0, (d1-d0)/oneDelta)
        if argTimeframe in ['W1','D1']:
          resultRange.append({'DateFrom':str(d0)[:10],'DateTo':str(d1)[:10]})
        else:
          resultRange.append({'DateFrom':str(d0)[:16],'DateTo':str(d1)[:16]})
      #Остаток
      if m > 0:
        d0 = argFromDate+(k*interval)
        d1 = argFromDate+(k*interval+m) 
      #print(d0,'->',d1,'=',d1-d0, (d1-d0)/oneDelta)      
      if argTimeframe in ['W1','D1']:
        resultRange.append({'DateFrom':str(d0)[:10],'DateTo':str(d1)[:10]})
      else:
        resultRange.append({'DateFrom':str(d0)[:16],'DateTo':str(d1)[:16]})
      return resultRange 
    if argFromDate=='' and argToDate=='' and argQuantity>0:  # not in [None,'',0]:      
      argToDate = DateNow(argTimeframe)
      argToDate = datetime.fromisoformat(argToDate)
      interval = seriesLenth[argTimeframe]  #300 
      k, m = divmod(argQuantity, interval)  #k-частное, m-остаток      
      #Основные блоки
      for i in range(k):        
        d1 = argToDate-(i*seriesDelta[argTimeframe])
        d0 = argToDate-((i+1)*seriesDelta[argTimeframe])
        #print(d0,'->',d1,'=',d1-d0, (d1-d0)/oneDelta)        
        if argTimeframe in ['W1','D1']:
          resultRange.append({'DateFrom':str(d0)[:10],'DateTo':str(d1)[:10]})
        else:
          resultRange.append({'DateFrom':str(d0)[:16],'DateTo':str(d1)[:16]})
      #Остаток
      if m > 0:
        d1 = argToDate-(k*seriesDelta[argTimeframe])
        d0 = argToDate-(k*seriesDelta[argTimeframe]+m*oneDelta)
      #print(d0,'->',d1,'=',d1-d0, (d1-d0)/oneDelta)      
      if argTimeframe in ['W1','D1']:
        resultRange.append({'DateFrom':str(d0)[:10],'DateTo':str(d1)[:10]})
      else:
        resultRange.append({'DateFrom':str(d0)[:16],'DateTo':str(d1)[:16]})
      #revert order
      resultRange2 = []
      for item in reversed(resultRange):
        resultRange2.append(item)      
      return resultRange2


def SplitListByLenth(row, lenth):
    k, m = divmod(len(row), lenth)  #k-частное, m-остаток
    result = ( row[i*lenth : (i+1)*lenth] for i in range(k) )   
    result = list(result)    
    result.append(row[k*lenth : k*lenth+m])
    return(result)

  
if __name__ == "__main__":    
    #start()
    #print(GetToken())
    for item in GetDateIntervals('','','H1',1000):
      print(item)