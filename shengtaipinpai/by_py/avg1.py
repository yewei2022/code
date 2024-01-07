# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 09:56:30 2023
计算第一步

# 把汉源字符删去 第二行开始
# 隔两行删一个站名
@author: 14779
"""

import pandas as pd


#%% branch1  读取所有sheet name

# df_all = pd.read_excel(r'D:\job\data\hy20230721.xlsx', sheet_name=None)
# sheet_names = list(df_all)
# print(sheet_names)


#%% branch2 提取每个县城的站名站号经纬度信息 并保存

# sheet_names = ['石棉县', '汉源县', '雨城区', '什邡市', '万源市', '越西县', 
#                 '峨边彝族自治县', '梓潼县', '大邑县', '叙永县', '市中区', 
#                 '邛崃市', '普格县']
# sheet_en = ["shimian", "hanyuan", "yuchengqu", "shenfang", "wanyuan", "yuexi",
#             "ebian", "zitong", "dayi", "xuyong", "leshanshizhongqu", 
#             "qionglai", "puge"]

# #(0, 11) 为0-10 前11个 
# for i in list(range(0,13,1)):
#     # i = 10
    
#     df0 = pd.read_excel(r"D:\job\data\hy20230721.xlsx",sheet_name = i,
#                         index_col = None)      
#     # 选取目标县 
#     if i == 10:    
#         df1 = df0[(df0['县级']==sheet_names[i]) & (df0['市级']=="乐山市")]
#     else:
#         df1 = df0[df0['县级']==sheet_names[i]]   
    
#     # 运行一次即可 提取所有站号 站名 经度 和 纬度 
#     sta = df1[["站号","站名","经度","纬度","海拔"]]
#     sta = sta.drop_duplicates(["站号"], keep='first').reset_index(drop=True)
#     sta.to_csv(r"D:\job\data\sta\sta_"+sheet_en[i]+".txt",index = False,sep=',')
#     del df0



#%%  branch3 简化每个县城的站名 并保存


# 用于简化站点名称 和sheet_names 不同
str_name = ['石棉', '汉源', '雨城', '什邡', '万源', '越西', 
                '峨边彝族自治县', '梓潼', '大邑', '叙永', '乐山', 
                '邛崃', '普格']
sheet_en = ["shimian", "hanyuan", "yuchengqu", "shifang", "wanyuan", "yuexi",
            "ebian", "zitong", "dayi", "xuyong", "leshanshizhongqu", 
            "qionglai", "puge"]

i = 10 #!!!
sta_name = str_name[i]
path_sta= "D:\\job\\data\\sta\\sta_"+sheet_en[i]+".txt" 
df = pd.read_table(path_sta,sep = ",")

# 当乐山时
a_sta = df.loc[df['站名']== sta_name, :]
# 县把所有站名字符串内的汉源县 汉源 字符删去  regex = True 必须
df['站名'].replace([sta_name+'县'], '',regex = True, 
                      inplace=True)
df['站名'].replace([sta_name], '',regex = True, 
                      inplace=True)


# #==================当站点太密集导致图不好看时---------------------
# # 隔两行删一个站名 按照站名排序在一块的地方就可以删掉一两个地名
# df_sort = df.sort_values(by='经度')
# list_index = list(np.arange(2, len(df_sort), 2))
# df_sort["站名"].iloc[list_index] = " "

# 拼接县名站
#================================================================
# [a_sta, df]  or  [a_sta, df_sort]
dff = pd.concat([a_sta, df],axis = 0, ignore_index = True) #!!!记得改这里
dff1 = dff.drop_duplicates(['站号','经度','纬度'], keep='first')

dff1.to_csv(r"D:\job\data\sta_simplify\sta_"+sheet_en[i]+".txt",index = False,
          sep=',')

