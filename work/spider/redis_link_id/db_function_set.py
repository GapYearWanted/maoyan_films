import redis

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)

"""
本文件用来定义一些redis数据库各个key之间的操作
比如复制key
等等
可以自定义、自添加函数
使用的时候只有在main函数调用即可
"""


def copy_key_db(db_name, to_db_name):  # 复制key函数
    db_len = red.llen(db_name)
    for i in range(db_len):
        median = red.lindex(db_name, i)
        red.rpush(to_db_name, median)


def delete_link_range(db_name, linkStr, start, end):  # 删除key中部分link,根据link的规律来自定义
    for i in range(start, end):
        link = linkStr + str(30 * i)
        red.lrem(db_name, 0, link)


def key_len(db_name):  # 查看可以的长度
    return red.llen(db_name)


def key_len_noRepeat(db_name):  # 去重后的长度
    db_list = red.lrange(db_name, 0, -1)
    db_list = list(set(db_list))
    return len(db_list)


def key_value_move(db_name, to_db_name):
    db_lsit = red.lrange(db_name, 0, -1)
    for one in db_lsit:
        red.rpush(to_db_name, one)
        red.lrem(db_name, 0, one)


if __name__ == '__main__':
    print(key_len('filmsId'))
    print(key_len_noRepeat('filmsId'))
    # key_value_move('idError', 'filmsId')
    # list_a = red.lrange('filmsId',0,-1)
    # list_b = list(set(list_a))
    # for i in list_b:
    #     red.rpush('idError', i)