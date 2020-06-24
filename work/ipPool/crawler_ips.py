import requests
from lxml import etree
import config
from ExceptionError.error1 import error1
import random
import time


class get_ips():
    def __init__(self):
        self.headers = config.headers

    def check_ip(self, ip_port):
        # link = 'http://icanhazip.com/'
        # proxy = "https://" + ip_port
        link = 'https://www.baidu.com/'
        proxy = "http://" + ip_port
        proxies = {'http': proxy}
        try:
            r = requests.get(link, headers=self.headers, proxies=proxies, timeout=10)
        except Exception as e:
            return 0
        else:
            code = r.status_code
            # if r.text == str(ip_port):
            if code == 200:
                return 1
            else:
                return 0
        time.sleep(random.random())

    def Crawling_ips(self, dictSetting):
        ips_list = []
        for i in range(0, len(dictSetting['link_list'])):
            url = dictSetting['link_list'][i]
            count = 0
            try:
                r = requests.get(url, headers=self.headers)
                if r.status_code != 200:
                    raise error1(r.status_code)
            except error1 as e:
                print("异常状态码：", e.status_code)
            else:
                html = etree.HTML(r.text)
                ip = html.xpath(dictSetting['ip'])
                port = html.xpath(dictSetting['port'])
                for j in range(0, len(ip)):
                    ip_port = ip[j] + ':' + port[j]
                    code = self.check_ip(ip_port)
                    if code == 1:
                        ips_list.append(ip_port)
                        count += 1
                print("在此网页已经爬到", count, "个可用代理")
            time.sleep(random.random())
        return ips_list
