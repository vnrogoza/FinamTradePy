MyHost="127.0.0.1"
MyPort=80
from datetime import datetime
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from plombery import task, get_logger, Trigger, register_pipeline
from GetCandleData import GetCandleDataV2
from pydantic import BaseModel

class InputParams(BaseModel):
  timeframe: str

@task
def get_candle_data(params: InputParams):
    import GetCandleData
    retValue = GetCandleData.GetCandleDataV3(params.timeframe)  
    logger = get_logger()
    logger.info(retValue)

@task
def Strategy_2MA():
    import Strat2MA
    retValue = Strat2MA.Run()
    logger = get_logger()
    logger.info(retValue)

@task
def current_time():  
    import datetime
    ct = datetime.datetime.now()
    logger = get_logger()
    logger.info(ct)
    return ct


register_pipeline(
    id="CT-001",
    description="Текущее время запуска",
    tasks=[current_time],    
    triggers=[
        Trigger(
            id="m5",
            name="Every 5 min",
            description="Run the pipeline every 5 minutes",
            schedule=CronTrigger(minute="0/5")            
        ),
    ],
)

register_pipeline(
    id="Candles M5",
    description="Получение свечек M5",
    tasks=[get_candle_data],
    params=InputParams,
    triggers=[
        Trigger(
            id="m5",
            name="Every 5 min",
            description="Run the pipeline every 5 minutes",            
            params=InputParams(timeframe="M5"),            
            schedule=CronTrigger(day_of_week='mon-sun', hour='8-23', minute="0/5", second=20)            
        ),
    ],
)

register_pipeline(
    id="Candles H1",
    description="Получение свечек Ч1",
    tasks=[get_candle_data],
    params=InputParams,
    triggers=[
        Trigger(
            id="h1",
            name="Every 1 hour",
            description="Run the pipeline every 1 hour",
            params=InputParams(timeframe="H1"),
            #schedule=IntervalTrigger(hours=1),
            #schedule=DateTrigger(run_date='2025-09-03 22:01:00'),
            #schedule=CronTrigger(day_of_week='mon-sat', hour='8-23', minute="0/5")
            schedule=CronTrigger(day_of_week='mon-sat', hour='8-23')
            #0/5 10-23 * * Mon-Sat   Every 5 minutes, between 10:00 AM and 11:59 PM, Monday through Saturday
            #use https://crontab.cronhub.io/  to create param line
            
        ),
    ],
)

register_pipeline(
    id="Candles D1",
    description="Получение свечек Д1",
    tasks=[get_candle_data],
    params=InputParams,
    triggers=[
        Trigger(
            id="d1",
            name="Every day",
            description="Run the pipeline every day",
            params=InputParams(timeframe="D1"),
            schedule=IntervalTrigger(days=1),            
        ),
    ],
)


register_pipeline(
    id="2MA",
    description="Стратегия 2МА",
    tasks=[Strategy_2MA],    
    triggers=[
        Trigger(
            id="m5",
            name="Every 5 minutes",
            description="Run the pipeline every 5 minutes",            
            schedule=CronTrigger(day_of_week='mon-sun', hour='8-23', minute="0/5", second=0)
        ),
    ],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("plombery:get_app", reload=True, factory=True, host=MyHost, port=MyPort)

'''
#original example
@task
async def fetch_raw_sales_data():
    """Fetch latest 50 sales of the day"""

    # using Plombery logger your logs will be stored
    # and accessible on the web UI
    logger = get_logger()

    logger.debug("Fetching sales data...")

    sales = [
        {
            "price": randint(1, 1000),
            "store_id": randint(1, 10),
            "date": datetime.today(),
            "sku": randint(1, 50),
        }
        for _ in range(50)
    ]
    #i = 1/0

    logger.info("Fetched %s sales data rows", len(sales))

    # Return the results of your task to have it stored
    # and accessible on the web UI
    return sales


register_pipeline(
    id="sales_pipeline",
    description="Aggregate sales activity from all stores across the country",
    tasks=[fetch_raw_sales_data],
    triggers=[
        Trigger(
            id="daily",
            name="Daily",
            description="Run the pipeline every day",
            schedule=IntervalTrigger(days=1),
        ),
    ],
)
'''