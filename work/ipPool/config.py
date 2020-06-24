ipList1_check_interval_time = 180  # ipList1 定时检查时间间隔
ipList2_check_interval_time = 420

ipList1_max = 50  # ipList1 最大存储ip数
ipList2_max = 150

ipList1_min = 20  # ipList1 最小存储ip数，小于则备用池向主池填充
ipList2_min = 40  # 小于再在网上爬取

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/81.0.4044.138 '
                  'Safari/537.36 '
}

xicidaili = {
    'pageEnd': 6,
    'link': 'https://www.xicidaili.com/nt/',
    'ip': '//tr[@class="odd"]/td[2]/text()',
    'port': '//tr[@class="odd"]/td[3]/text()'
}

kuaidaili = {
    'pageEnd': 6,  # 爬取页数
    'link': 'https://www.kuaidaili.com/free/inha/1/',
    'ip': '//td[@data-title="IP"]/text()',  # ip的xpath解析方式
    'port': '//td[@data-title="PORT"]/text()'  # port 的解析方式
}


def kuaidaili_url_format():
    link_list = []
    for i in range(1, kuaidaili['pageEnd'] + 1):
        link = kuaidaili['link'].replace('1', str(i))
        link_list.append(link)
    kuaidaili['link_list'] = link_list


def xicidaili_url_format():
    link_list = []
    for i in range(1, xicidaili['pageEnd'] + 1):
        link = xicidaili['link'] + str(i)
        link_list.append(link)
    xicidaili['link_list'] = link_list


# if __name__ == '__main__':
# 不能使用这条语句  否则在其他文件调用config.py
# 的时候下面的函数不能执行
kuaidaili_url_format()
xicidaili_url_format()
