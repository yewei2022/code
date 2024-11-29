# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 21:34:11 2024

@author: yewei
"""
import pandas as pd
import requests

data_dir = r'D:\YEWEI\project'
url = "http://10.1.64.146/disaster/webDirectReport/directList"
# url = "http://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"
df = pd.read_html(url,encoding ="utf8")[0]
df.to_csv(data_dir +"\爬取.csv",index = True)


#%%

# import requests
# from BS4 import Beautifulsoup
# from selenium import webdriver
# #设置韧始页码和总页数
# current_page = 1
# total_pages = 18
# #创建一个chrome浏览器实例
# driver = webdriver. Chrome()
# while current_page <= total_pages:
#     #构造当前页的URL
#     url = "http://permit.mee.gov.cn/perxxgkinfo/syssb/xkgg/xkgg!licenseInformation.action"
#     #发送HTTP请求获取网页内容
#     response = requests.get(url)
#     html = response.text
#     #解行网页内容
#     soup = Beautifulsoup(html,"html.parser")
#     products = soup.find_all( "div" , class_= "product")
#     #瘫职商品信息并存储
#     for product in products:
#         name = product.find("h2").text
#         price = product.find( "span" , class_="price " ).text
#         #存储到文件或数据库
    
#     #判断是否有下一页
#     next_button = driver.find_element_by_class_name( 'next')
#     if next_button:
#         #点击下一页按钮
#         next_button.click()
#         current_page += 1
#     else:
#         break

# #关闭浏览器实例
# driver.quit()
