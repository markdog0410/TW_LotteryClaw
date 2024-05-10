import sqlite3
from lottery_history import TaiwanLotteryHistoryCrawler

crawler = TaiwanLotteryHistoryCrawler()
con = sqlite3.connect('lottery_data.db')
cur = con.cursor()
# cur.execute('CREATE TABLE SUPER_LOTTERY(title,date,num1,num2,num3,num4,num5,num6,numS)')
# cur.execute("INSERT INTO SUPER_LOTTERY VALUES ('112000001','1120101','1','2','3','4','5','6','7')")
# con.commit()

res = cur.execute('SELECT * FROM SUPER_LOTTERY')

# rows = res.fetchall()
# for row in rows:
#     print(row)

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print(tables)