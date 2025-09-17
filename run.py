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
  retValue = GetCandleData.GetCandleDataV2(params.timeframe)
  print(retValue)
  return 'retValue'

register_pipeline(
    id="get_candle_data H1",
    description="get every new H1 candles",
    tasks=[get_candle_data],
    params=InputParams,
    triggers=[
        Trigger(
            id="h1",
            name="Every H1",
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
    id="get_candle_data D1",
    description="get every day candles",
    tasks=[get_candle_data],
    params=InputParams,
    triggers=[
        Trigger(
            id="d1",
            name="Every D1",
            description="Run the pipeline every day",
            params=InputParams(timeframe="D1"),
            schedule=IntervalTrigger(days=1),
            #schedule=DateTrigger(run_date='2025-09-03 22:01:00'),
            #schedule=CronTrigger(day_of_week='mon-sat', hour='8-23', minute="0/5")
            #schedule=CronTrigger(day_of_week='mon-sat', hour='8-23')
            #0/5 10-23 * * Mon-Sat   Every 5 minutes, between 10:00 AM and 11:59 PM, Monday through Saturday
            #use https://crontab.cronhub.io/  to create param line
            
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