# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 20:17:35 2023

@author: yewei
"""

import re
import pandas as pd


data_dir = "D:\\YEWEI\\project\\traffic\\2024\\data\\"
pic_dir = "D:\\YEWEI\\project\\traffic\\2024\\pic\\"


#%% branch1 step1 规范桩号数据

# df = pd.read_excel(data_dir +"高影响路段桩号处理2023.xlsx",sheet_name = 0,
#                     index_col = None,usecols= [0,1,2,3,4,5,6,7,8,9,10])

# S107 = df.loc[df["督办路段点位编码"]=="S107",:]
# S107a = S107["经度（度）"].str.split(".", expand=True).values[:, :3].astype(int)
# S107["经度（度）"] = S107a[:, 0] + S107a[:, 1]/60 + S107a[:, 2]/3600
# S107a = S107["纬度（度）"].str.split(".", expand=True).values[:, :3].astype(int)
# S107["纬度（度）"] = S107a[:, 0] + S107a[:, 1]/60 + S107a[:, 2]/3600


# G545 = df.loc[df["督办路段点位编码"]=="G545",:]
# G545a = G545["经度（度）"].str.split("°|′|″", expand=True).values[:, :3].astype(int)
# G545["经度（度）"] = G545a[:, 0] + G545a[:, 1]/60 + G545a[:, 2]/3600
# G545a = G545["纬度（度）"].str.split("°|′|″", expand=True).values[:, :3].astype(int)
# G545["纬度（度）"] = G545a[:, 0] + G545a[:, 1]/60 + G545a[:, 2]/3600

# # 使用布尔索引过滤某些行数据
# # 过滤S107和G545
# df1 = df[(df['督办路段点位编码'] != "S107") & (df['督办路段点位编码'] != "G545")]

# # 重新拼接处理过经纬度的S107 G545
# dff= pd.concat([df1, S107,G545],axis = 0, ignore_index = True) 
# dff.columns = ['road_id','lon','lat','alti','pile_id','province','city','county',
#               'road','road_type','weather']
# #写入文件
# dff.to_csv(data_dir+"桩号2023.txt",
#               index = False,sep=' ',na_rep=32700)


#%% #%% branch1 step2  计算距离 得到离每段路最近距离站点

# from math import sin,radians,cos,asin,sqrt
# import numpy as np

# def SphereDistance(lon1, lat1, lon2, lat2):
#     radius = 6371.0 # radius of Earth, unit:KM
#     # degree to radians
#     lon1, lat1,lon2, lat2 = map(radians,[lon1, lat1,lon2, lat2])
#     dlon = lon2 -lon1
#     dlat = lat2 -lat1
#     arg  = sin(dlat*0.5)**2 +  \
#             cos(lat1)*cos(lat2)*sin(dlon*0.5)**2
#     dist = 2.0 * radius * asin(sqrt(arg))
#     return dist

# # 函数：根据桩号和每个站点之间的距离，返回最小距离的站点
# def min_dist(road_id,pile_id,pile_lat,pile_lon):
#     #站点数据
#     sta_info = pd.read_table(data_dir+"sta_info.txt",sep = ",",
#                         usecols=['sta','name','lon','lat','alti'])
#     sta_save = [] #保存计算过的所有站点信息
#     dist_save=[] #保存最近站点距离
#     station=sta_info['sta'].tolist()
#     sta_lat=sta_info['lat'].tolist()
#     sta_lon=sta_info['lon'].tolist()
#     N=len(sta_lon)
#     for i in range(0,N):
#         newLine = ['road_id','pile_id','pile_lat','pile_lon','sta',
#                     'sta_lat', 'sta_lon']
#         dist_pile2sta = SphereDistance(sta_lon[i],sta_lat[i], pile_lon,pile_lat)   
#         newLine[0] = road_id                 
#         newLine[1] = pile_id
#         newLine[2] = pile_lat
#         newLine[3] = pile_lon
#         newLine[4] = station[i]
#         newLine[5] = sta_lat[i]
#         newLine[6] = sta_lon[i]
#         # print(newLine)
#         if newLine not in sta_save:
#             sta_save.append(newLine)
#             dist_save.append(dist_pile2sta)
#     sta_df = pd.DataFrame(sta_save,columns = ['road_id','pile_id','pile_lat',
#                                               'pile_lon','sta','sta_lat', 'sta_lon'])
#     dist_df = pd.DataFrame(dist_save,columns = ['dist'])
#     id_b = dist_df.idxmin(axis=0)  # 打印距离最小值的索引
#     b = dist_df.min(axis=0)  # 打印距离最小值的索引
#     print(id_b)
#     print(b)
#     print(sta_df.loc[int(id_b),:])
#     dfa = pd.concat([sta_df.loc[int(id_b),:],b])
#     return dfa


# # 读取站点数据
# road_id =dff['road_id'].tolist()
# pile_id =dff['pile_id'].tolist()
# pile_lat=dff['lat'].tolist()
# pile_lon=dff['lon'].tolist()

# #测试
# # pile1 =pile_id[0]
# # lat1 = pile_lat[0]
# # lon1 = pile_lon[0]

# npts=len(pile_id)
# dist_list=[]
# for i in range(0,npts):
#     dist_list.append(min_dist(road_id[i],pile_id[i],pile_lat[i],pile_lon[i]))
    
# #% 筛选不重复的站点

# df_pile = pd.concat(dist_list,axis = 1)
# df_pile1 = df_pile.T
# sta_pick = df_pile1.drop_duplicates(["sta"], keep='first').reset_index(drop=True)

# #写入文件
# sta_pick.to_csv(data_dir+"road_sta_pick2023.txt",
#               index = False,sep=' ',na_rep=32700)

#%% branch2 根据站点筛选浓雾年均日数

# sta_pick = pd.read_table(data_dir+"road_sta_pick2023.txt",sep = "\s+")
# sta1 = sta_pick.set_index('sta',inplace=False)
# fog = pd.read_table(data_dir+"fog_year_avg_days.txt",sep = "\s+")
# fog1 = fog.set_index('sta', inplace=False)
# road_fog = pd.concat([sta1,fog1],axis =1,join = "inner")
# road_fog1 = road_fog.drop(['lon','lat'],axis=1)
# road_fog2 = road_fog1.reset_index(drop = False)
# road_fog2.to_csv(data_dir+"road_sta_fogdays2023.txt",
#                   index = False,columns = ['road_id','pile_id',
#                 'pile_lat','pile_lon','sta','sta_lat', 'sta_lon',
#                 'alti','dist','days'],sep=' ',na_rep=32700)


#%% branch3 根据站点筛选有降水且最低温小于0度日数

# sta_pick = pd.read_table(data_dir+"road_sta_pick2023.txt",sep = "\s+")
# sta1 = sta_pick.set_index('sta',inplace=False)
# fog = pd.read_table(data_dir+"tmp0_year_avg_days.txt",sep = "\s+")
# fog1 = fog.set_index('sta', inplace=False)
# road_fog = pd.concat([sta1,fog1],axis =1,join = "inner")
# road_fog1 = road_fog.drop(['lon','lat'],axis=1)
# road_fog2 = road_fog1.reset_index(drop = False)
# road_fog2.to_csv(data_dir+"road_sta_tmp0days2023.txt",
#                   index = False,columns = ['road_id','pile_id',
#                 'pile_lat','pile_lon','sta','sta_lat', 'sta_lon',
#                 'alti','dist','days'],sep=' ',na_rep=32700)

