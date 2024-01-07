# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:20:47 2023
计算第二步
一个县一个县算（因为要等前面每个县站名处理
@author: 14779
"""

import pandas as pd

data_dir = "D:\\project\\shengtaipinpai\\data\\"

#%% branch1  处理数据

# excel表格中“县级”那栏下的名称 用于读取每个表中需要的县（有些表可能混杂其他县
sheet_names = ['石棉县', '汉源县', '雨城区', '什邡市', '万源市', '越西县', 
               '峨边彝族自治县', '梓潼县', '大邑县', '叙永县', '市中区', 
               '邛崃市', '普格县']
sheet_en = ["shimian", "hanyuan", "yuchengqu", "shifang", "wanyuan", "yuexi",
            "ebian", "zitong", "dayi", "xuyong", "leshanshizhongqu", 
            "qionglai", "puge"]
#(0, 11) 为0-10 前11个 
# for i in list(range(0,13,1)):

# 还是单个来吧，等第二步del_str 每个县的站名改后再做    
i= 11

df0 = pd.read_excel(r"D:\job\data\hy20230721.xlsx",sheet_name = i,
                    index_col = None)      
# 选取目标县
#=========== 市中区 # 因为这里既有内江的又有乐山的市中区 加个判断============
if i == 10:    
    df1 = df0[(df0['县级']==sheet_names[i]) & (df0['市级']=="乐山市")]
else:
    df1 = df0[df0['县级']==sheet_names[i]]
    # 因为这里既有内江的又有乐山的市中区

var =['最低气温','最高气温','平均气温','20降水','平均气压','平均湿度','平均风速']
for j in list(range(0,7,1)):
    
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

    path_sta= "D:\\job\\data\\sta_simplify\\sta_"+sheet_en[i]+".txt" #!!!文件夹
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




