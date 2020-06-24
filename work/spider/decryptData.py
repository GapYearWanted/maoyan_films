import requests
from bs4 import BeautifulSoup
from fontTools.ttLib import TTFont
from os import remove
import numpy as np
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0;Win64;x64) AppleWebKit/537.36 (KHTML, likeGecko) Chrome/81.0.4044.138 '
                  'Safari/537.36 '
}
maoyan_dict = {
    'uniE164': '2',
    'uniE9F7': '1',
    'uniEFAF': '6',
    'uniEEB6': '7',
    'uniE1AE': '3',
    'uniE314': '4',
    'uniEAE4': '0',
    'uniE7D1': '5',
    'uniF7F4': '8',
    'uniEC28': '9',
}


# 获取坐标的函数
def getAxis(font):
    uni_list = font.getGlyphOrder()[2:]
    font_axis = []
    for uni in uni_list:
        axis = []
        for i in font['glyf'][uni].coordinates:
            axis.append(i)
        font_axis.append(axis)
    return font_axis


# 获取对比文字base的字体以及坐标
base_font = TTFont('base.woff')
uni_base_list = base_font.getGlyphOrder()[2:]
base_axis = getAxis(base_font)
base_font = None


def get_woff_link(re_text):
    soup = BeautifulSoup(re_text.replace("&#x", ""), 'lxml')
    woffs = soup.select('head > style')
    wofflist = str(woffs[0]).split('\n')
    woff_link = wofflist[5].replace(' ', '').replace('url(\'//', '').replace('format(\'woff\');', '').replace(
        '\')', '')
    return woff_link


# 获取动态网页的数据
def getFont(woff_link):
    font_url = 'http://' + woff_link
    try:
        font_file = requests.get(font_url).content
    except Exception as e:
        print("Error:", e)
        print("可能访问的页面异常403")
    else:
        with open("demo.woff", "wb") as code:
            code.write(font_file)
    return parseFont()


# 获取当前页面动态字体的字典
def parseFont():
    # print('open:\t' + cur_path)
    cur_font = TTFont('demo.woff')
    uni_list = cur_font.getGlyphOrder()[2:]
    cur_axis = getAxis(cur_font)
    font_dict = {}
    for i in range(len(uni_list)):
        min_avg, uni = 99999, None
        for j in range(len(uni_base_list)):
            avg = compare_axis(cur_axis[i], base_axis[j])
            if avg < min_avg:
                min_avg = avg
                uni = uni_base_list[j]
        font_dict['&#x' + uni_list[i][3:].lower() +';'] = maoyan_dict[uni]
    remove('demo.woff')
    return font_dict


# 使用欧式距离计算
def compare_axis(axis1, axis2):
    if len(axis1) < len(axis2):
        axis1.extend([0, 0] for _ in range(len(axis2) - len(axis1)))
    elif len(axis2) < len(axis1):
        axis2.extend([0, 0] for _ in range(len(axis1) - len(axis2)))
    axis1 = np.array(axis1)
    axis2 = np.array(axis2)
    return np.sqrt(np.sum(np.square(axis1 - axis2)))


def total(re_text):
    woff_link = get_woff_link(re_text)
    return getFont(woff_link)


if __name__ == "__main__":
    total()
