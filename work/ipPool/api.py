from flask import Flask
import redis
import random


"""
使用flask框架，搭建简答的api
想获取ip_port 
直接requests http://127.0.0.1:5000/random即可
"""
pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
red = redis.Redis(connection_pool=pool)
app = Flask(__name__)


def get_ip():
    ip = random.choice(red.lrange('ipList1', 0, -1))
    print("随机获取的ip为：", ip)
    return ip


@app.route('/')
def index():
    return 'Welcome to Proxy Pool System'


@app.route('/random')
def get_proxy():
    return get_ip()
