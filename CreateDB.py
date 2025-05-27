import sqlite3
# Устанавливаем соединение с базой данных
connection = sqlite3.connect('DB\\finam.db')
cursor = connection.cursor()

#ОСНОВНЫЕ ТАБЛИЦЫ
cursor.execute('''
CREATE TABLE IF NOT EXISTS Candles (    
    Security TEXT NOT NULL,
    Timeframe TEXT NOT NULL,
    DateTime TEXT NOT NULL,
    Open REAL NOT NULL,
    High REAL NOT NULL,
    Low REAL NOT NULL,
    Close REAL NOT NULL,
    Volume INTEGER NOT NULL,
    Date TEXT,
    Time TEXT,
    ModifyDT TEXT,
    CONSTRAINT "PK" PRIMARY KEY (Security, Timeframe, DateTime)
    );
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Security (    
    Code TEXT NOT NULL,
    Board TEXT NOT NULL,
    Market TEXT NOT NULL,
    Decimals INTEGER NOT NULL,
    LotSize INTEGER NOT NULL,
    MinStep	INTEGER NOT NULL,
    Currency TEXT,
    ShortName TEXT,
    Properties INTEGER,
    TimeZoneName TEXT,
    BpCost INTEGER,
    AccruedInterest INTEGER,
    PriceSign TEXT,
    Ticker TEXT,
    LotDivider INTEGER,
    Active INTEGER,
    ModifyDT TEXT,
    PRIMARY KEY("Code","Board")
    );
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS "SecurityList" (
	"Security"	TEXT NOT NULL,
	"Board"	TEXT NOT NULL,
	"TimeFrame"	TEXT NOT NULL,
	"Quantity"	INTEGER,
	"DateFrom"	TEXT,
	"DateTo"	TEXT,	
	"Active"	INTEGER,
	"ModifyDT"	TEXT,
	PRIMARY KEY("Security", "TimeFrame") 
    );
''')

#СТРАТЕГИИ
cursor.execute('''
CREATE TABLE IF NOT EXISTS StgyCandles (
    Strategy TEXT NOT NULL,
    Security TEXT NOT NULL,
    Timeframe TEXT NOT NULL,
    DateTime TEXT NOT NULL,
    Open REAL NOT NULL,
    High REAL NOT NULL,
    Low REAL NOT NULL,
    Close REAL NOT NULL,
    Volume INTEGER NOT NULL,
    PRIMARY KEY (Strategy, Security, Timeframe, DateTime)
    );
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS "StgyValues" (
	"Strategy"	TEXT NOT NULL,
	"DateTime"	TEXT NOT NULL,
	"Name"	TEXT NOT NULL,
	"Value"	REAL,
    "Value2" REAL,
	PRIMARY KEY("Strategy","DateTime","Name")
);
''')
#ТЕСТОВЫЕ
cursor.execute('''
CREATE TABLE IF NOT EXISTS TestCandles (
    Security TEXT NOT NULL,
    Timeframe TEXT NOT NULL,
    DateTime TEXT NOT NULL,
    Open REAL NOT NULL,
    High REAL NOT NULL,
    Low REAL NOT NULL,
    Close REAL NOT NULL,
    Volume INTEGER NOT NULL,
    Date TEXT,
    Time TEXT,
    ModifyDT TEXT,
    CONSTRAINT "PK" PRIMARY KEY (Security, Timeframe, DateTime)
    );
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS TestStgyCandles (
    Strategy TEXT NOT NULL,
    Security TEXT NOT NULL,
    Timeframe TEXT NOT NULL,
    DateTime TEXT NOT NULL,
    Open REAL NOT NULL,
    High REAL NOT NULL,
    Low REAL NOT NULL,
    Close REAL NOT NULL,
    Volume INTEGER NOT NULL,
    PRIMARY KEY (Strategy, Security, Timeframe, DateTime)
    );
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS "TestStgyValues" (
	"Strategy"	TEXT NOT NULL,
	"DateTime"	TEXT NOT NULL,
	"Name"	TEXT NOT NULL,
	"Value"	REAL,
    "Value2"	REAL,
	PRIMARY KEY("Strategy","DateTime","Name")
);
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()


'''
DROP TRIGGER "main"."seclist_onupdate";
CREATE TRIGGER seclist_onupdate UPDATE ON SecurityList BEGIN
	UPDATE SecurityList SET ModifyDT = datetime("now","localtime");
END

'''