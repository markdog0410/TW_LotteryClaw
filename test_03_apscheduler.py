from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

zone = pytz.timezone('Asia/Taipei')

print(datetime.now(zone))
taipei_zoe = datetime.now(zone)
year = taipei_zoe.year - 1911
month = taipei_zoe.month
current_time = str(year) + taipei_zoe.strftime("/%m/%d")
print(current_time)
