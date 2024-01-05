title = "Привет"
def start():
    print("Starting...")

def GetToken():
  file = open("token.txt", "r")
  token = file.readline()
  return token

def DateInterval(argDatetime0, argDatetime1, argTimeFrame):
  from datetime import datetime, timedelta
  if argDatetime0 > argDatetime1:
    print("DateDiff: First date must be smaller then second")
    return None
  if argTimeFrame not in  ["M15","H1","D1"]:
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
  dayHrs = 14
  dayH1 = dayHrs * 1
  dayM15 = dayH1 * 4
  dayM5 = dayH1 * 12
  delta = argDatetime1 - argDatetime0
  #Считаем количество рабочих дней  7.12 - 6.12 = 1д
  holidays = [datetime(2023, 3, 8)]
  currDate = argDatetime0.date()
  workDays = 0
  currDate += timedelta(days=1)
  while currDate <= argDatetime1.date():
    if currDate.weekday() < 5 and currDate not in holidays:
        workDays += 1
    currDate += timedelta(days=1)      
  if argTimeFrame == "M15":
    retValue = workDays * dayM15
    retValue = retValue + delta.seconds//m15sec
  if argTimeFrame == "H1":
    retValue = workDays * dayH1  #delta.days
    retValue = retValue + delta.seconds//h1sec
  if argTimeFrame == "D1":
    retValue = workDays        
  return retValue

def DateAdd(argDatetime, argInterval, argTimeFrame):
  from datetime import datetime, timedelta
  if argInterval == 0:
    print("DateDiff: Wrong interval value")
    return None
  if argTimeFrame not in  ["M15","H1","D1"]:
    print("DateDiff: Wrong timeframe")
    return None  
  holidays = [datetime(2023, 3, 8)]
  workDays = [0,1,2,3,4]
  workHours = range(10, 24)
  currDate = argDatetime
  i = 0  
  if argInterval > 0:
    while i < argInterval:
      if argTimeFrame == "M15":
        currDate += timedelta(minutes=15)
      if argTimeFrame == "H1":
        currDate += timedelta(hours=1)
      if argTimeFrame == "D1":
        currDate += timedelta(days=1)
      if argTimeFrame in  ["M15","H1"]:
        if (currDate.weekday() in workDays) and (currDate not in holidays) and (currDate.hour in workHours):
          i += 1
      if argTimeFrame in  ["D1"]:
        if (currDate.weekday() in workDays) and (currDate not in holidays):
          i += 1
        #print(i, currDate, currDate.weekday())
  if argInterval < 0:
    while i > argInterval:
      if argTimeFrame == "M15":
        currDate -= timedelta(minutes=15)
      if argTimeFrame == "H1":
        currDate -= timedelta(hours=1)
      if argTimeFrame == "D1":
        currDate -= timedelta(days=1)
      if argTimeFrame in  ["M15","H1"]:
        if (currDate.weekday() in workDays) and (currDate not in holidays) and (currDate.hour in workHours):
          i -= 1
      if argTimeFrame in  ["D1"]:
        if (currDate.weekday() in workDays) and (currDate not in holidays):
          i -= 1      
        #print(i, currDate, currDate.weekday())
  return currDate

def DateNow(argTimeFrame):
  if argTimeFrame not in  ["M15","H1","D1"]:
      print("DateDiff: Wrong timeframe")
      return None
  from datetime import datetime  
  ct = datetime.now()
  if argTimeFrame == "D1":
    return datetime(ct.year, ct.month, ct.day)
  if argTimeFrame in ["H1", "M15"]:
    return datetime(ct.year, ct.month, ct.day, ct.hour)  
    




if __name__ == "__main__":    
    start()
    #print(GetToken())