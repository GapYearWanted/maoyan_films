import threading
import time
from db import db
from crawler_ips import get_ips
import config


# 定时检查主ip池
def time_ip():
    while True:
        len1 = db().check_db('ipList1')
        print("主ip池长度为：", len1)
        if len1 < config.ipList1_min:
            len2 = round((config.ipList1_max + config.ipList1_min) / 2) - len1
            if db().check_db('ipList2') >= len2:
                db().db_move_ip('ipList2', 'ipList1', len2)
            else:
                print("备用池的ip数量不够，准备从网上抓取---")
                ips_list_k = get_ips().Crawling_ips(config.kuaidaili)
                ips_list_x = get_ips().Crawling_ips(config.xicidaili)
                ips_list = ips_list_x + ips_list_k
                db().insert_db(ips_list)
        print(config.ipList1_check_interval_time, '秒后再检查数据库')
        time.sleep(config.ipList1_check_interval_time)


# 定时检查备用ip池
def time_ips():
    while True:
        if db().check_db('ipList2') < config.ipList2_min:
            print("备用池存储数据少于临界值，准备填数据")
            ips_list_k = get_ips().Crawling_ips(config.kuaidaili)
            ips_list_x = get_ips().Crawling_ips(config.xicidaili)
            ips_list = ips_list_x + ips_list_k
            db().insert_db(ips_list)
        else:
            print("备用池数据充足")
        print(config.ipList2_check_interval_time, '秒后再检查数据库')
        time.sleep(config.ipList2_check_interval_time)


def total():
    t1 = threading.Thread(target=time_ip)
    t1.start()
    t2 = threading.Thread(target=time_ips)
    t2.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    total()
