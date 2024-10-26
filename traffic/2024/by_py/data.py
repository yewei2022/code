# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:39:53 2023
处理气象数据计算浓雾日数 道路结冰日数
@author: yewei
"""

import pandas as pd

# 交通事故调查
# f_dir = r'D:\YEWEI\project\交通\202310-公路交通一张图\3.相关参考文档\全省恶劣天气频发路段明细表.xlsx'
# df = pd.read_excel(f_dir, sheet_name=0, skiprows = 1,index_col= None,nrows=150)

#气象数据2016-2023
f_dir = r'D:\YEWEI\project\traffic\2023\202310-公路交通一张图\2.气象数据\2016-2023.csv'
df1 = pd.read_csv(f_dir,sep = ",",header = 0,usecols =['sid',
                'sdate','statTime','vsmin08','tmin08','pr08'],na_values=['NULL'])

# df1.loc[:,'time'] = pd.to_datetime(df1['statTime'],format = '%Y-%m-%d %H:%M:%S.%f')
df1.loc[:,'time'] = pd.to_datetime(df1['sdate'],format = '%Y-%m-%d')


#%% 一次就够 有效站点数 

# sta_list = df1.drop_duplicates(["sid"], 
#                                           keep='first').reset_index(drop=True)
# # 基本站信息
# f_dir1 = r'D:\YEWEI\project\traffic\202310-公路交通一张图\2.气象数据\四川基本站信息.rpt'
# df2 = pd.read_csv(f_dir1, skiprows = 2,sep = "\s+",header = None,
#                   names=['sta','name','class','lat','lon','alti','unknow',
#                         'province','city','county'])
# sta_pick = df2[:-2]

# # sta_list sta_pick 都是156
# sta_pick.to_csv(r"D:\YEWEI\project\traffic\data\sta_info.txt",index = False,
#             sep=',',encoding = "utf-8")


#%% 一次就够 截取时间到2022年底，筛选数据缺测率在10%以内站点，结果是156站全部满足

# df11 = df1.set_index(['time']) #设置时间列为索引
# # 必须先按时间排序再切片
# count = df11.sort_index().loc['2016-01-01 00:00:00':'2022-12-31 00:00:00',:]
# #计数
# count.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 便于后面缺测值计数 
# count.loc[:,'count']=1
# count1=count.groupby(by=['sid'])['count'].sum()

# # 获取总日数
# time1 = pd.to_datetime('2016-01-01')
# time2 = pd.to_datetime('2022-12-31')
# # Timedelta类型
# delta_time = time2 - time1
# # 转换为int
# delta_time = delta_time.days

# count1=count1/delta_time
# count1.where(count1 > 0.9, inplace=True)#condition为True，则保留原值，否则默认替换为nan
# #``df1.where(m, df2)``等于``np.where(m, df1, df2)``等于''df1.mask(~m, df2)''
# count1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
# # count无异常值 可不做异常值剔除

# count2=count1.reset_index(drop=False)
# count_sta=count2.sid.tolist()


#%% branch1 计算 年均浓雾日数  浓雾：能见度小于200米

# df11 = df1.set_index(['time']) #设置时间列为索引
# # 必须先按时间排序再切片
# df111 = df11.sort_index().loc['2016-01-01 00:00:00':'2022-12-31 00:00:00',:]
# df111.reset_index(inplace=True,drop=False)

# fog = df111[df111['vsmin08']<200]

# fog.loc[:,'year'] = fog['time'].dt.year
# fog.loc[:,'count'] = 1
# fog_sum = fog.groupby(by=['sid'])['count'].sum()
# fog_avg = fog_sum/7
# fog_avg1 = fog_avg.round(decimals=0)

# #添加位置信息，法二
# path_sta = r'D:\YEWEI\project\traffic\2023\data\sta_info.txt'
# sta = pd.read_table(path_sta,sep = ",",usecols=['sta','lon','lat','alti'])
# #拼接
# sta.set_index('sta', inplace=True) # column 改为 index
# fog_avg2 = fog_avg1.reset_index(drop=False)
# fog_avg2.columns=['sta','days']
# fog_avg2.set_index('sta', inplace=True) # column 改为 index
# info = pd.concat([sta,fog_avg2],axis=1,join="inner") #和80个站点信息取交集
# #写入文件
# info.to_csv(r'D:\YEWEI\project\traffic\2024\data\fog_year_avg_days.txt',
#                     index = True,sep=' ',na_rep=32700)


#%% branch2 计算 有降水且日最低气温＜1的年均日数

# df11 = df1.set_index(['time']) #设置时间列为索引
# # 必须先按时间排序再切片
# df111 = df11.sort_index().loc['2016-01-01 00:00:00':'2022-12-31 00:00:00',:]
# df111.reset_index(inplace=True,drop=False)

# fog = df111[(df111['tmin08']<0) & (df111['pr08']>=0.1)]

# fog.loc[:,'year'] = fog['time'].dt.year
# fog.loc[:,'count'] = 1
# fog_sum = fog.groupby(by=['sid'])['count'].sum()
# fog_avg = fog_sum/7
# fog_avg1 = fog_avg.round(decimals=0)

# #添加位置信息，法二
# path_sta = r'D:\YEWEI\project\traffic\2023\data\sta_info.txt'
# sta = pd.read_table(path_sta,sep = ",",usecols=['sta','lon','lat','alti'])
# #拼接
# sta.set_index('sta', inplace=True) # column 改为 index
# fog_avg2 = fog_avg1.reset_index(drop=False)
# fog_avg2.columns=['sta','days']
# fog_avg2.set_index('sta', inplace=True) # column 改为 index
# info = pd.concat([sta,fog_avg2],axis=1,join="inner") #和80个站点信息取交集
# #写入文件
# info.to_csv(r'D:\YEWEI\project\traffic\2024\data\tmp0_year_avg_days.txt',
#                     index = True,sep=' ',na_rep=32700)



 



   
