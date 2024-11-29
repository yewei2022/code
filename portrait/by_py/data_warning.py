# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 15:07:14 2024
按指定索引重置行
@author: yewei
"""

import pandas as pd
import numpy as np

data_dir = r'D:\YEWEI\project\袁-软课题\预警特征分析\data'
pic_dir = r'D:\YEWEI\project\袁-软课题\预警特征分析\pic'

#%% 读取数据

data = pd.read_excel(data_dir + '\四川预警2023.xlsx', sheet_name=0,
                     usecols= [0,1,2,3,4,5,6])
data.loc[:,'count'] = 1

#%% 统计

disaster = data.groupby(by=['预警事件'])['count'].sum()
color = data.groupby(by=['预警等级'])['count'].sum()
data.loc[:,'time'] =pd.to_datetime(data['发布时间']) #转换为时间戳time
data['month'] = data['time'].dt.month #取出时间中的月份
month = data.groupby(by=['month'])['count'].sum()
month.to_csv(data_dir +"\month2023.csv",index = True)#写入文件

 # #统计不同预警类型各月总量
dis_mon = data.groupby(by=['预警事件','month'])['count'].sum()
dis_mon1 = dis_mon.reset_index(drop=False)
# 变成行索引为类别 列索引为月
dis_mon2 = dis_mon1.pivot(index = '预警事件', columns = 'month',values = 'count')
dis_mon3 = dis_mon2.fillna(0)
#在原数据结构上新建行（index是新索引，若新建数据索引在原数据中存在，则引用原有数据），
#默认用NaN填充(使用fill_value=0 来修改填充值自定义，此处我设置的是0)。
dis_mon4 = dis_mon3.reindex(index=['暴雪','暴雨','冰雹','大风','大雾','霜冻',
                                   '干旱','高温', '寒潮','雷电','道路结冰',
                                   '强降温','地质灾害气象风险','森林（草原）火险'],
                            fill_value=0)
dis_mon4.to_csv(data_dir +"\disaster_month2023.csv",index = True)

# 读取2018-2022的
data2022 = pd.read_excel(data_dir +"\disaster_month2022before.xlsx")
data2022.set_index('预警类别',inplace =True) 
df = data2022 + dis_mon4
# 写入文件
# df.to_csv(data_dir +"\disaster_month_all.csv",index = True)
df1 = df/6
# 写入文件
# df1.to_csv(data_dir +"\disaster_month_ave.csv",index = True)

pick1 = data[(data['预警事件']=='高温')&(data['预警等级']=='橙色预警')]
pick2 = data[(data['市名称']=='甘孜藏族自治州')&(data['预警等级']=='红色预警')]
pick3 = data[(data['市名称']=='攀枝花')&(data['预警等级']=='红色预警')]
pick4 = data[data['预警等级']=='红色预警']
pick5 = pick4.drop_duplicates(["预警事件"], keep='first').reset_index(drop=True)







