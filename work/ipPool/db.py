import redis
from crawler_ips import get_ips
import config
import time
from multiprocessing import Pool
import requests
import random

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)


class db():
    def __init__(self):
        # 创建redis数据库连接池
        self.pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        self.red = redis.Redis(connection_pool=self.pool)

    def insert_db(self, ips_list):
        """
        将爬取到的ip_port插入redis数据库
        ipList1 ->主ip池
        ipList2 -> 备用ip池
        优先插入ipList1
        ipList1满后再插入ipList2

        :param ips_list:
        :return:
        """
        db_ip_list1 = self.red.lrange('ipList1', 0, -1)  # 局部list,用来判断将插入的值是否已经在数据库中
        for eachIP in ips_list:
            try:
                if eachIP in db_ip_list1:
                    print("该ip已经在数据库中:", eachIP)
                else:
                    if self.red.llen('ipList1') < config.ipList1_max:  # 主ip池最大容量，便于维护
                        self.red.rpush('ipList1', eachIP)
                        db_ip_list1.append(eachIP)
                        print("成功插入ip_port", eachIP)
                    else:
                        break
            except Exception as e:
                print("错误", e)

        # 备用ip池的插入
        if len(ips_list) > config.ipList1_max:
            db_ip_list2 = self.red.lrange('ipList2', 0, -1)
            for ip_index in range(config.ipList1_max, len(ips_list)):
                try:
                    if ips_list[ip_index] in db_ip_list2:
                        print("该ip已经在数据库中:", ips_list[ip_index])
                    else:
                        if self.red.llen('ipList2') < config.ipList2_max:
                            self.red.rpush('ipList2', ips_list[ip_index])
                            db_ip_list2.append(ips_list[ip_index])
                            print("成功插入ip_port", ips_list[ip_index])
                        else:
                            break
                except Exception as e:
                    print("错误", e)
        else:
            print("没有足够的ip_port插入备用池了")

    def check_db(self, db_name):
        db_len = self.red.llen(db_name)
        for i in range(0, db_len):
            ip_port = self.red.lindex(db_name, i)
            code = get_ips().check_ip(ip_port)
            if code == 0:
                self.red.lrem(db_name, 0, ip_port)

        db_len_after = self.red.llen(db_name)
        return db_len_after

    def db_move_ip(self, db_name, to_db_name, num):  # 这里有 备用池为零的情况做个分支
        if self.red.lrange(db_name, 0, -1) != 0:
            for i in range(num + 1):
                ip_port = self.red.lpop(db_name)
                self.red.rpush(to_db_name, ip_port)
        else:
            print("备用的数量为空")

    def get_db(self, db_name):
        return self.red.lrange(db_name, 0, -1)


"""
#单线程检查数据库长度
#多次测试： 检查一个ip平均花时 0.5s
"""

"""
def check_ip(ip_port, db_name):
    link = 'https://www.baidu.com/'
    proxy = "http://" + ip_port
    proxies = {'http': proxy}
    r = requests.get(link, headers=config.headers, proxies=proxies, timeout=5)
    if r.status_code != 200:
        red.lrem(db_name, 0, ip_port)
    time.sleep(random.random())


def multi_progress_check_db(db_name):
    p = Pool(4)
    list_p = red.lrange(db_name, 0, -1)
    for one in list_p:
        p.apply_async(check_ip, args=(one, db_name,))
    len_after = red.llen(db_name)
    return len_after


s_t = time.time()
# h = db().check_db('ipList1')
h = multi_progress_check_db('ipList1')
print(h)
e_t = time.time()
print("花时：", e_t - s_t)
"""
