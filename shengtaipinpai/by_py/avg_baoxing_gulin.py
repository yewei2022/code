# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:54:17 2023
宝兴
@author: 14779
"""

import pandas as pd

# excel表格中“县级”那栏下的名称 用于读取每个表中需要的县（有些表可能混杂其他县
sheet_names = ['宝兴县', '古蔺县']
sheet_en = ["baoxing", "gulin"]
data_dir = "D:\\project\\shengtaipinpai\\data\\"
pic_dir = "D:\\project\\shengtaipinpai\\pic\\"

#%% branch1 提取站点 step1提取每个县城的站名站号经纬度信息 并保存
    
# df0 = pd.read_excel(r"D:\project\shengtaipinpai\data\hy20231101.xlsx",sheet_name = 0,
#                     index_col = None)
# #(0, 2) 为0-1 前2个

# for i in list(range(0,2,1)):      
#     df1 = df0[df0['县级']==sheet_names[i]]   
    
#     # 运行一次即可 提取所有站号 站名 经度 和 纬度 
#     sta = df1[["站号","站名","经度","纬度","海拔"]]
#     sta = sta.drop_duplicates(["站号"], keep='first').reset_index(drop=True)
#     sta.to_csv(r"D:\project\shengtaipinpai\data\sta\sta_"+sheet_en[i]+".txt",
#                index = False,sep=',')
#     del df1



#%% branch1 提取站点 step2 简化每个县城的站名 并保存

# # 用于简化站点名称 和sheet_names 不同
# str_name = ['宝兴', '古蔺']
# sheet_en = ["baoxing", "gulin"]

# i = 1 #!!! 一个一个做
# sta_name = str_name[i]
# path_sta= "D:\\project\\shengtaipinpai\\data\\sta\\sta_"+sheet_en[i]+".txt" 
# df = pd.read_table(path_sta,sep = ",")

# # 当乐山时
# a_sta = df.loc[df['站名']== sta_name, :]#先保存县名站那行
# # 把所有字符串内部的特定字符去掉 eg. 去掉汉源县 "汉源"  regex = True 必须
# df['站名'].replace([sta_name+'县'], '',regex = True, 
#                       inplace=True)
# df['站名'].replace([sta_name], '',regex = True, 
#                       inplace=True)


# # #================当站点太密集导致图不好看时 这里不要！后续绘图再操作也行---------
# # # 隔两行将一个站名设置为空 按照站名排序在一块的地方就可以删掉一两个地名
# # df_sort = df.sort_values(by='经度')
# # list_index = list(np.arange(2, len(df_sort), 2))
# # df_sort["站名"].iloc[list_index] = " "

# # 拼接县名站
# #================================================================
# # [a_sta, df]  or  [a_sta, df_sort]
# dff = pd.concat([a_sta, df],axis = 0, ignore_index = True) #!!!记得改这里
# dff1 = dff.drop_duplicates(['站号','经度','纬度'], keep='first')

# dff1.to_csv(r"D:\project\shengtaipinpai\data\sta_simplify\sta_"+sheet_en[i]+".txt",index = False,
#           sep=',')

#%% branch2 计算站点平均 

# 还是单个来吧，等branch1 step2 del_str 每个县的站名改后再做    
i= 1 #古蔺

df0 = pd.read_excel(data_dir+"hy20231101.xlsx",sheet_name = 0,
                    index_col = None)      
# 选取目标县
df1 = df0[df0['县级']==sheet_names[i]]

var =['最低气温','最高气温','平均气温','20降水','平均气压','平均湿度','平均风速']
for j in list(range(0,7,1)):
    
    # j=2 #一个一个来#======================================================
    # 筛选出缺测值
    def fill_nan(x):
        if x[var[j]] >999900:
            return None
        else:
            return x[var[j]]
    df1.loc[:,var[j]]= df1.apply(fill_nan,axis=1)
    # # 古蔺的降水做多年夏季总量平均 
    if (i==1) and (j==3):     
        df2 = df1[(df1['月']>5) & (df1['月']<9)].loc[:,['站号','资料日期','年',
                                                  var[j]]] 
        # df2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
        #删不删结果是一样的 df求均值没管某个nan
        a00 = df2.groupby(by=['站号','年'])[var[j]].sum()
        a000 = a00.reset_index(drop=False)
    # # 宝兴的降水做多年年总量平均 
    elif (i==0) and (j==3):
        df2 = df1.loc[:,['站号','资料日期','年',var[j]]] 
        # df2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
        a00 = df2.groupby(by=['站号','年'])[var[j]].sum()
        a000 = a00.reset_index(drop=False)
    # 古蔺的三个温度做多年夏季日平均  不需要的话就注释掉 #!!!
    elif (i==1) and (j>=0 and j<3):    
        df2 = df1[(df1['月']>5) & (df1['月']<9)].loc[:,['站号','站名','资料日期','年',
                                                      '月',var[j]]] 
        a000 = df2.reset_index(drop=False)
    # 其他县 其他要素 做多年日平均  
    else:
        a000 = df1
    
    
    a1 = a000.groupby(by=['站号'])[var[j]].mean()
    a1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
    a2 = a1.reset_index(drop=False)
    a2.loc[:,'站号']= a2['站号'].astype(str) #不改的话56378会丢失
    
    path_sta = data_dir+"sta_simplify\\sta_"+sheet_en[i]+".txt" #!!!文件夹
    sta=pd.read_table(path_sta,sep = ",")
    #拼接
    sta.set_index('站号', inplace=True) # column 改为 index
    a2.set_index('站号', inplace=True) # column 改为 index
    info = pd.concat([sta,a2],join='inner',axis=1) #'outer' 'inner'
    info1 = info.reset_index()
    
    #写入文件
    putfile = ["tem_min","tem_max","tem_avg","prcp","pres","RH","wind"]
    info1.to_csv(data_dir+"deal\\"+sheet_en[i]+"_"+putfile[j]+".txt",
                  index = False,sep=' ',na_rep=32700)

