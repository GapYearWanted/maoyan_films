import redis
import time
import random
import requests
from lxml import etree
# from multiprocessing import Process, Queue
from multiprocessing import Pool
import os
import sys

sys.path.append('..')
import config
import get_random_ip

headers = config.headers
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)

link_list = []
link_list = red.lrange('links', 0, -1)

"""
多进程
从每个页面的详细url获取每部电影第一的id
"""


def crawler(url):
    print("子进程---------", os.getpid())
    try:
        time.sleep(random.randint(5, 15) + random.random())
        proxies1 = {'http': 'http://' + get_random_ip.random_ip()}
        r = requests.get(url, headers=headers, proxies=proxies1, timeout=20)
        real_url = r.url  # 猫眼会有验证模块，需要手动处理一下
        if real_url != url:
            print("真实链接与访问链接不一样，需要手动验证一下")
            print(r.url)
            red.rpush("filmsIdError", url)
            red.lrem('links', 0, url)
            time.sleep(3)

        else:
            html = etree.HTML(r.text)
            movie_id = html.xpath('//div[@class="channel-detail movie-item-title"]/a/@data-val')
            if len(movie_id) == 0:
                mss = ','.join(html.xpath('//p[@class="not-found-message"]/text()')).encode("ISO-8859-1").decode("utf-8")
                if mss == config.reError:
                    print("403异常-------")
                    print(url)
                    red.rpush('filmsIdError', url)
                    red.lrem('links', 0, url)
                else:
                    print("未在此页面找到内容----，注意检查")
                    print(url)
                    red.rpush('filmsIdError', url)
                    red.lrem('links', 0, url)
            else:
                for each in range(len(movie_id)):
                    film_id = movie_id[each][9:len(movie_id[each]) - 1]
                    red.rpush("filmsId", film_id)
                    print("插入成功:", film_id)
                print("成功插入", len(movie_id), "个")
                red.lrem('links', 0, url)
                time.sleep(random.randint(4, 9) + random.random())
    except Exception as e:
        print(url, 'Error: ', e)
        red.rpush("filmsIdError", url)
        print(url, "插入filmsIdError成功")


if __name__ == '__main__':

    print("父进程--------", os.getpid())
    p = Pool(4)
    for url in link_list:
        p.apply_async(crawler, args=(url,))
    p.close()
    p.join()
    print('主进程结束-----')
