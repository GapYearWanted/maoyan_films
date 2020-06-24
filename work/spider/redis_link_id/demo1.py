import pymysql
import redis
db = pymysql.connect("localhost", "root", "TYGCUANG123", "maoyan", charset="utf8")
cursor = db.cursor()
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)


sql = """
SELECT films_id
FROM maoyanfilms
"""
cursor.execute(sql)
datalist = []
alldata = cursor.fetchall()
for s in alldata:
    datalist.append(s[0])
print(datalist)
print(len(datalist))
it = red.lrange('filmsId', 0, -1)
ie = red.lrange('idError',0,-1)
print(len(ie))
for tt in ie:
    if tt in datalist:
        print("在，删除--", tt)
        red.lrem('idError', 0, tt)
    else:
        print("------------", tt)

db.close()