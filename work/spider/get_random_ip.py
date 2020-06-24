import requests


def random_ip():
    r = requests.get('http://127.0.0.1:5000/random')
    ip = r.text
    return ip
