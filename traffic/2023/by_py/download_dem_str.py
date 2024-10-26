# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 14:30:49 2023
批量生成文件网页下载目录
处理字符
找出两个列表不同的元素
@author: yewei
"""
import pandas as pd
import os

data = pd.read_table(r"C:\Users\yewei\Desktop\dem_下载.txt",header = None,
                     names = ['url'])
#将url字符串中包含“图片”或“中心经度”字符的行设为None
data["url"].mask(data.url.str.contains(".*?图片")|data.url.str.contains(".*?中心经度"), None, inplace=True)

#删除url为空的行
df = data.dropna(axis=0,how='any')
# 字符串内的 特定字符删去  regex = True 必须
df['url'].replace(['数据标识： '], '',regex = True, inplace=True)
df.loc[:,'url'] = 'https://bjdl.gscloud.cn/sources/download/310/'+\
    df['url']+'?sid=kW_SgQSzE-7DqiaHgW5emWO2oGNvc23_gkOin-JWOtszFQ&uid=927236'

# df.to_csv(r"C:\Users\yewei\Desktop\下载.txt",index = False,header =False,
#           sep=' ',na_rep=32700)

files = os.listdir(r'D:\搜狗高速下载\dem')
files1 = pd.DataFrame(files,columns = ['url'])
files1['url'].replace(['.img.zip'], '',regex = True, inplace=True)
files1.loc[:,'url'] = 'https://bjdl.gscloud.cn/sources/download/310/'+\
    files1['url']+'?sid=kW_SgQSzE-7DqiaHgW5emWO2oGNvc23_gkOin-JWOtszFQ&uid=927236'
    
set1 = set(files1['url'].tolist())
set2 = set(df['url'].tolist())
diff = set1 ^ set2
print(diff)