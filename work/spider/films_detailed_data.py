import redis
import pymysql
import requests
from lxml import etree
import config
import get_random_ip
import decryptData
import re
import time
import random
from multiprocessing import Pool
import os
import sys

headers = config.headers
db = pymysql.connect("localhost", "root", "TYGCUANG123", "maoyan", charset="utf8")
cursor = db.cursor()
# cursor.execute("DROP TABLE IF EXISTS maoyanfilms")
# cursor.execute(config.sql1)

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)


def films_data(filmsId):
    print("子进程--------", os.getpid())
    # time.sleep(random.randint(5, 10) + random.random())
    url = 'https://maoyan.com/films/' + str(filmsId)
    # proxies1 = {'http': 'http://' + get_random_ip.random_ip()}
    r = requests.get(url, headers=headers, timeout=20)
    if r.url != url:
        print("返回的真实链接与url不一样，需要手动处理一下验证模块")
        print(r.url)
        red.rpush('idError', filmsId)  # 未能正确解析的放入另一个数据库，后期再解析
        red.lrem('filmsId', 0, filmsId)
        time.sleep(10)
    else:
        # 获取详细内容部分
        resp = r.text
        html = etree.HTML(resp)
        # 电影名
        films_name = ','.join(html.xpath('//div[@class="movie-brief-container"]/h1/text()'))
        # 电影类型
        films_type = ','.join(html.xpath('//div[@class="movie-brief-container"]/ul/li['
                                         '1]/a/text()'))
        if films_name == '':
            print("获取数据异常，可能是403异常，检查一下")
            print(url)
            red.rpush('idError', filmsId)  # 未能正确解析的放入另一个数据库，后期再解析
            red.lrem('filmsId', 0, filmsId)
            time.sleep(10)
        else:
            font_dict = decryptData.total(resp)
            for key in font_dict.keys():
                resp = resp.replace(key, font_dict[key])
            body = etree.HTML(resp)  # 这里的resp经过上面的循环处理过的，注意不要和上面混淆
            mark_info = body.xpath('//div[@class="movie-index"]/div')
            mark = mark_info[0].xpath('string(.)').replace(' ', '')
            mark = re.sub(r'\n+', '|', mark)[1:-1].split('|')
            if len(mark) < 2:
                films_score = ''
                films_comment_num = ''
            else:
                films_score = mark[0]
                films_comment_num = mark[1][:-3]
            films_box_office = mark_info[1].xpath('string(.)').replace(' ', '').replace('\n', '')
            # films_data_dict = {'评分': films_score, '评分人数': films_comment_num, '累计票房': films_box_office}
            films_area_duration = ','.join(body.xpath('//div[@class="movie-brief-container"]/ul/li['
                                                      '2]/text()')).split('/')
            # 上映地区
            films_area = films_area_duration[0].strip()
            # 时长
            films_duration = films_area_duration[1].strip()
            # 首映时间
            film_first_time = ','.join(body.xpath('//div[@class="movie-brief-container"]/ul/li['
                                                  '3]/text()'))
            # 电影简介
            films_introduction = ','.join(body.xpath('//span[@class="dra"]/text()'))
            # 导演
            films_director = ','.join(
                body.xpath('//div[@class="celebrity-container clearfix"]/div[1]/ul/li/div/a/text()')).strip()
            # 主演
            films_actor = ','.join(
                body.xpath('//div[@class="celebrity-container clearfix"]/div[2]/ul//li/div/a/text()')).replace('\n',
                                                                                                               '').replace(
                '\r',
                '').strip()
            # 评论
            films_comment = ','.join(body.xpath('//div[@class="comment-content"]/text()'))
            try:
                cursor.execute(config.sql2, (filmsId, films_name, films_type, films_area,
                                             films_duration, film_first_time,
                                             films_score, films_comment_num,
                                             films_box_office, films_director,
                                             films_actor, films_introduction, films_comment))
                db.commit()
                print("已经成功插入数据库--------", filmsId)
                red.lrem('filmsId', 0, filmsId)
            except Exception as e:
                db.rollback()
                s = str(e)[1:5]
                print("未插入，异常编号---------", s)
                if s == '1062':
                    red.lrem("filmsId", 0, filmsId)
                    print("主键重复，已删除-------", filmsId)
                else:
                    red.rpush("idError", filmsId)
                    red.lrem("filmsId", 0, filmsId)
                    print("数据异常，已插入idError-------", filmsId)


if __name__ == '__main__':

    print("父进程--------", os.getpid())
    films_id_list = red.lrange('filmsId', 0, -1)
    print("key原长度---", len(films_id_list))
    films_id_list = list(set(films_id_list))
    print("key去重后长度---", len(films_id_list))
    p = Pool(4)
    for eid in films_id_list[::-1]:
        p.apply_async(films_data, args=(eid,))
    p.close()
    p.join()
    db.close()
    print('主进程结束-----')
