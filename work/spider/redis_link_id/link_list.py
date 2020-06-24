from multiprocessing import Process, Queue
import time
import requests
import random
import redis
from lxml import etree
import sys

sys.path.append('..')
import config
import get_random_ip

""""
多线程
把将要爬取的每个页面的url链接整理好
放入数据库中，爬的时候直接从数据库中取得每个页面的url
"""

link_list = []
sourceId_list = [2, 10, 13]
yearId_list = range(5, 15)
for s in sourceId_list:
    for y in yearId_list:
        link = 'https://maoyan.com/films?sourceId=' + str(s) + '&yearId=' + str(y) + "&showType=3"
        link_list.append(link)
"""
以上是数据预处理
但是上面的url(link)只涉及到电影的年份，地区，
下面还要获取电影列表的每一页的url
"""

headers = config.headers
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)


class MyProcess(Process):
    def __init__(self, q):
        Process.__init__(self)
        self.q = q

    def run(self):
        # print("Starting ", self.pid)
        while not self.q.empty():
            crawler(self.q)
        # print("Exiting ", self.pid)


def crawler(q):
    url = q.get(timeout=2)
    try:
        proxies1 = {'http': 'http://' + get_random_ip.random_ip()}
        time.sleep(random.randint(3, 6) + random.random())
        r = requests.get(url, headers=headers, proxies=proxies1)
        real_link = r.url
        if url != real_link:
            print("访问的链接与真实返回的链接不一样，需要手动验证一下")
            print(r.url)
            red.rpush("linkError", url)
            """
            猫眼会有验证模块，需要手动处理一下
            这里还需要注意一下，某个url运行到了这个地方
            那么他就不能再往下面继续解析了
            也就得不到每个页面的详细url
            所以要把进来的url放入linkError数据库
            之后再对linkError进行处理
            不然会缺失运行到这里的url
            """
        else:
            time.sleep(random.randint(0, 3) + random.random())
            html = etree.HTML(r.text)
            # 这里要寻找每个类型的最大页数
            page_list = html.xpath('//ul[@class="list-pager"]//li//text()')
            if len(page_list) == 0:  # 频繁的访问可能会返回403，也就解析不出相要的数据，下面做一下处理
                print("解析出的list为空，可能访问异常403\n", "将url插入存放error的数据库", url)
                red.rpush("linkError", url)
            else:
                pages = [x.strip() for x in page_list if x.strip() != '']  # 去掉返回的空白和转行符
                pages.remove("下一页")  # 去掉这个list最后一个元素就是页面最大页数了
                max_page = pages[-1]
                offset_list = range(0, int(max_page))
                for offset in offset_list:
                    detailed_url = url + "&offset=" + str(30 * offset)
                    red.rpush("links", detailed_url)
                    print("插入成功", detailed_url)
                print("成功插入", len(offset_list), "个")
                time.sleep(random.randint(1, 4) + random.random())
    except Exception as e:
        print(q.qsize(), url, 'Error: ', e)
        red.rpush("linkError", url)
        print(url, "插入linkError成功")


if __name__ == '__main__':
    ProcessNames = ["Process-1", "Process-2", "Process-3"]
    workQueue = Queue(2000)

    # 填充队列
    for url in link_list:
        workQueue.put(url)

    for i in range(0, 3):
        p = MyProcess(workQueue)
        # p.daemon = True
        p.start()
        p.join()

    print('Main process Ended!')
