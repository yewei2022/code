# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:20:47 2023
使用历史回算数据,计算邛崃普格
@author: 14779
"""

import pandas as pd


# excel表格中“县级”那栏下的名称 用于读取每个表中需要的县（有些表可能混杂其他县
sheet_names = ['石棉县', '汉源县', '雨城区', '什邡市', '万源市', '越西县', 
               '峨边彝族自治县', '梓潼县', '大邑县', '叙永县', '市中区', 
               '邛崃市', '普格县']
sheet_en = ["shimian", "hanyuan", "yuchengqu", "shifang", "wanyuan", "yuexi",
            "ebian", "zitong", "dayi", "xuyong", "leshanshizhongqu", 
            "qionglai", "puge"]

file_dir = "E:\\"

#%% branch1 


# #(11, 13) 为11-12 两个 
# for i in list(range(11,13,1)):
#     # i = 10
    
#     df0 = pd.read_excel(file_dir + "历史回算数据\\"+sheet_en[i]+".xlsx",sheet_name = 0,
#                         index_col = None)      

#     df1 = df0[df0['县级']==sheet_names[i]]   
    
#     # 运行一次即可 提取所有站号 站名 经度 和 纬度 
#     sta = df1[["站号","站名","经度","纬度"]]
#     sta = sta.drop_duplicates(["站号"], keep='first').reset_index(drop=True)
#     sta.to_csv(file_dir + "job\\data\\sta\\sta_"+sheet_en[i]+".txt",index = False,sep=',')
#     del df0


#%% branch2 处理站点名称


# # 用于简化站点名称 和sheet_names 不同
# str_name = ['石棉', '汉源', '雨城', '什邡', '万源', '越西', 
#                 '峨边彝族自治县', '梓潼', '大邑', '叙永', '乐山', 
#                 '邛崃', '普格']

# i = 12 #!!!
# sta_name = str_name[i]
# path_sta= file_dir + "job\\data\\sta\\sta_"+sheet_en[i]+".txt" 
# df = pd.read_table(path_sta,sep = ",")

# # 当乐山时
# a_sta = df.loc[df['站名']== sta_name, :]
# # 县把所有站名字符串内的汉源县 汉源 字符删去  regex = True 必须
# df['站名'].replace([sta_name+'县'], '',regex = True, 
#                       inplace=True)
# df['站名'].replace([sta_name], '',regex = True, 
#                       inplace=True)
# #邛崃
# df['站名'].replace(["应用气象观测站（交通）"], '',regex = True, 
#                       inplace=True)


# # #==================当站点太密集导致图不好看时但要记得改下方叹号--------------
# # # 隔两行删一个站名 按照站名排序在一块的地方就可以删掉一两个地名
# # df_sort = df.sort_values(by='经度')
# # list_index = list(np.arange(2, len(df_sort), 2))
# # df_sort["站名"].iloc[list_index] = " "

# # 拼接县名站
# #================================================================
# # [a_sta, df]  or  [a_sta, df_sort]
# dff = pd.concat([a_sta, df],axis = 0, ignore_index = True) #!!!记得改这里
# dff1 = dff.drop_duplicates(['站号','经度','纬度'], keep='first')

# dff1.to_csv(file_dir + "job\\data\\sta_simplify\\sta_"+sheet_en[i]+".txt",index = False,
#           sep=',')


#%% branch3  处理数据

   
i= 12 #一个一个来

df0 = pd.read_excel(file_dir + "历史回算数据\\"+sheet_en[i]+".xlsx",sheet_name = 0,
                    index_col = None)      
# 选取目标县

df1 = df0[df0['县级']==sheet_names[i]]

df1.loc[:,'time'] = pd.to_datetime(df1['资料日期'],format = '%Y-%m-%d %H:%M:%S')
df1.loc[:,'年'] =df1.time.dt.year
df1.loc[:,'月'] =df1.time.dt.month
df1.loc[:,'日'] =df1.time.dt.day

var =['最低气温','最高气温','平均气温','降水','平均湿度','平均风速']
for j in list(range(0,6,1)):
    
    # j=3
    # 筛选出缺测值
    def fill_nan(x):
        if x[var[j]] >999900:
            return None
        else:
            return x[var[j]]
    df1.loc[:,var[j]]= df1.apply(fill_nan,axis=1)
    # # 邛崃 普格的降水做多年夏季总量平均 
    if (10<i<13) and (j==3):     
        df2 = df1[(df1['月']>5) & (df1['月']<9)].loc[:,['站号','资料日期','年',
                                                  var[j]]] 
        # df2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
        #删不删结果是一样的 df求均值没管某个nan
        a00 = df2.groupby(by=['站号','年'])[var[j]].sum()
        a000 = a00.reset_index(drop=False)
    # # 其他县的降水做多年年总量平均 
    elif (i<11) and (j==3):
        df2 = df1.loc[:,['站号','资料日期','年',var[j]]] 
        # df2.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
        a00 = df2.groupby(by=['站号','年'])[var[j]].sum()
        a000 = a00.reset_index(drop=False)
    # 邛崃 普格的三个温度做多年夏季日平均  不需要的话就注释掉 #!!!
    elif (10<i<13) and (j>=0 and j<3):    
        df2 = df1[(df1['月']>5) & (df1['月']<9)].loc[:,['站号','资料日期','年',
                                                      var[j]]] 
        a000 = df2.reset_index(drop=False)
    # 其他县 其他要素 做多年日平均  
    else:
        a000 = df1
    

    a1 = a000.groupby(by=['站号'])[var[j]].mean()
    a1.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行 
    a2 = a1.reset_index(drop=False)
    a2.loc[:,'站号']= a2['站号'].astype(str) #不改的话56378会丢失

    path_sta= file_dir + "job\\data\\sta_simplify\\sta_"+sheet_en[i]+".txt" #!!!文件夹
    sta=pd.read_table(path_sta,sep = ",")
    #拼接
    sta.set_index('站号', inplace=True) # column 改为 index
    a2.set_index('站号', inplace=True) # column 改为 index
    info = pd.concat([sta,a2],join='inner',axis=1) #'outer' 'inner'
    info1 = info.reset_index()

    #写入文件
    putfile = ["tem_min","tem_max","tem_avg","prcp","RH","wind"]
    info1.to_csv(file_dir + "job\\data\\deal\\"+sheet_en[i]+"_"+putfile[j]+".txt",
                  index = False,sep=' ',na_rep=32700)




