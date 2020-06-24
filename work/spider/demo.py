import requests
import decryptData
from lxml import etree
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/81.0.4044.138 '
                  'Safari/537.36 '
}

url = "https://maoyan.com/films/1218273"

r = requests.get(url,headers=headers)
resp = r.text
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
films_data_dict = {'评分': films_score, '评分人数': films_comment_num, '累计票房': films_box_office}
print("爬取的URL为", url)
print(films_data_dict)