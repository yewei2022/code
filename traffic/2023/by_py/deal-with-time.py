# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 19:17:14 2021

@author: Lenovo
"""


import os
import datetime
import pandas as pd


#%%  读time，tc_id，#读取BOB每个个例时间信息，每个个例后面再加一天
#按照3h/1h一次计算总时次

# def calculate_tim_3h(utc):
#     time = pd.Series(pd.to_datetime(utc,format='%Y%m%d%H')) #字符串变时间
#     day_of_year=time.dt.dayofyear
#     hh0=pd.DataFrame(utc)
#     hh1=pd.DataFrame(hh0[0].astype(str).str[8:10])
#     hh2=hh1[0].astype(int)
#     hh3=hh2/3+1
#     hours=(day_of_year-1)*24/3+hh3  
#     return hours

# def calculate_tim_1h(utc):
#     time = pd.Series(pd.to_datetime(utc,format='%Y%m%d%H')) #字符串变时间
#     day_of_year=time.dt.dayofyear
#     hh0=pd.DataFrame(utc)
#     hh1=pd.DataFrame(hh0[0].astype(str).str[8:10])
#     hh2=hh1[0].astype(int)
#     hh3=hh2/1+1
#     hours=(day_of_year-1)*24/1+hh3    
#     return hours

# utc_init = []
# utc_end = []
# tc_id   = []
# path='F:\\snow_sts_data\\BOB\\'
# f_list = os.listdir(path)  # 得到文件夹下的所有文件名称
# #print(len(f_list))

# for file in f_list:
#     filename1=path+file
#     #print(filename1)
#     with open(filename1, 'r', encoding='UTF-8') as f1:
#         lines = f1.readlines()  # 按行给lines
#         s0=len(lines)
#         s=s0-1
#         i=0
#         for line in lines:
#             data=line.split(',')
#             if i==0:
#                 utc_init.append(data[2].strip())
#                 tc_id.append(file[3:9])
#             if i==s:
#                 utc0=data[2].strip()
#                 # print(utc0)
#                 utc1= datetime.datetime.strptime(utc0, '%Y%m%d%H') #字符串变时间
#                 utc2=utc1+datetime.timedelta(days=1) #往后一天
#                 utc3=utc2.strftime('%Y%m%d%H') #时间变字符串
#                 # print(utc_3)
#                 utc_end.append(utc3)
#             i=i+1


# 计算时次
# times_init=calculate_tim_1h(utc_init).astype(int)
# times_end =calculate_tim_1h(utc_end).astype(int)
# #%%  step 2   写入文件
# tc_times=pd.DataFrame(list(zip(tc_id,utc_init,utc_end,times_init,times_end)),
#                           columns=['tc_id','utc_init','utc_end','tims_init',
#                                     'tims_end'])
# tc_times.loc[:,'times']=tc_times['tims_end']-tc_times['tims_init']+1

# tc_times.to_csv(r"F:\\snow_sts_data\\tc_tims_1h.txt",index = False,
#                 sep='\t',encoding = "utf-8")

#%%  生成固定间隔的时间序列，generate a time list
# tim_list_1 = pd.date_range("2020-05-15 06:00","2020-05-22 06:00",
#                               freq="H").strftime("%Y%m%d%H").to_list()
# tim_list_2 = pd.date_range("2020-11-22 06:00","2020-11-28 12:00",
#                               freq="H").strftime("%Y%m%d%H").to_list()
# tim_list_3 = pd.date_range("2020-11-29 12:00","2020-12-06 06:00",
#                               freq="H").strftime("%Y%m%d%H").to_list()
# lst=tim_list_1+tim_list_2+tim_list_3 
# tim=pd.DataFrame(lst)
# tim1=tim[0].astype(str).str[2:10]
# tim1.to_csv(r"F:\\snow_sts_data\\2020_tctimfortbb.txt",index = False,
#                 sep=' ',header=None,encoding = "utf-8")


#%% 将一列时间格式数据time1转换为字符串time2 time1必须是dataframe

# time2=time1.dt.strftime('%Y%m%d') #时间变字符串

#%% 获取带小数点的时间 字符串变时间

# path_file1 = 'F:\\CZ\\data\\钢梁平台风速风向.txt'
# a1 = pd.read_table(path_file1,sep=',',nrows=500)
# print(a1.dtypes)
# # 转换时间，法一
# # Measure_ID,col0,col1,col2
# # 6693290,2022-01-01-00-00-00.734,103,5
# a1.loc[:,'time'] = pd.to_datetime(a1['col0'],format = '%Y-%m-%d-%H-%M-%S.%f') 

# # 转换时间，法二
# # def convert(x):
# #     time = dt.datetime.strptime(x['col0'], '%Y-%m-%d-%H-%M-%S.%f') #字符串变时间
# #     return time                   
# # https://blog.csdn.net/T_110140/article/details/123658046
# # a1.loc[:,'time']= a1.apply(convert, axis=1)
        