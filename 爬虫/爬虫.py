# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 22:35:47 2024

@author: 14779
"""

import requests
from lxml import etree


url = 'http://www.spiderbuf.cn/s04/'
html = requests.get(url).text
# 先保存在本地
f = open('data01.html', 'w', encoding='utf-8')
f.write(html)
f.close()

root = etree.HTML(html)
trs = root.xpath('//tr')

f = open('data01.txt', 'w', encoding='utf-8')
for tr in trs:
    tds = tr.xpath('./td')
    s = ''
    for td in tds:
        # print(td.text)
        s = s + str(td.text) + ' '
    print(s)
    if s != '':
        f.write(s + '\n')

f.close()

# print(html)
