import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)

page = range(67, 305)
for i in page:
    link = 'https://maoyan.com/films?sourceId=2&yearId=5&showType=3&offset=' + str(30 * i)
    red.lrem('links', 0, link)
    print("删除成功",link)
