# -*- coding: utf-8 -*-
"""
站点聚类
"""

import pandas as pd
import math
from sklearn.cluster import KMeans
from matplotlib.path import Path



#%% 读取数据


df = pd.read_excel('D:\\Data\\portrait\\信息登记表.xlsx',sheet_name = 0,
                  usecols = ["省",'市',"县（区、市、旗）", "预警接收单位",
                             "预警接收单位级别"])
df0 = df.dropna(how='all', axis=0)
hangye = pd.read_table('D:\\Data\\portrait\\行业.txt', header = None,
                       names = ['hangye'])

#%% 处理数据

search_characters = hangye['hangye'].tolist()

# 创建正则表达式模式
pattern = '|'.join(search_characters)  # 'world|pandas'

# 使用str.extract()方法提取匹配的字符
df0['hangye'] = df['预警接收单位'].str.extract(f'({pattern})', expand=False)

 
# pre_f=pre.groupby(by=['station'])['pre_extrm_label'].sum() # 极端pre频数
# gss_f=gss.groupby(by=['station'])['gss_extrm_label'].sum() # 极端gss频数


#%% 计算各参数  用距平 不太中啊

# pic_save_name="dev_station_label"
# pre_f=pd.read_table("F:\\f\\snow_sts_data\\1981-2020\\sta_avg_pre.txt",
#                           sep='\s+',usecols=['station','dev'],na_values=32700)
# gss_f=pd.read_table("F:\\f\\snow_sts_data\\1981-2020\\sta_avg_gss.txt",
#                           sep='\s+',usecols=['station','dev'],na_values=32700)
 
# pre_f.set_index('station', inplace=True) # column 改为 index 
# gss_f.set_index('station', inplace=True)


#%% 计算各参数 pre>=2mm gss>=1cm 频数 

# pic_save_name="thres_station_label"
# need=pd.read_table("F:\\f\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)
# pre1=need[need['dailypre']>=2]
# gss1=need[need['gss']>=1]

# snow_f=need.groupby(by=['station'])['snow'].sum() 
# pre_f0=pre1.groupby(by=['station'])['snow'].sum() 
# gss_f0=gss1.groupby(by=['station'])['snow'].sum()
# pre_f=pd.concat([snow_f,pre_f0],axis=1)
# gss_f=pd.concat([snow_f,gss_f0],axis=1)
# pre_f.columns=['snow_f','pre_f']
# pre_f.drop(['snow_f'],axis=1,inplace=True)
# gss_f.columns=['snow_f','gss_f']
# gss_f.drop(['snow_f'],axis=1,inplace=True)


#%% 计算各参数  用降雪频数 降水量均值 积雪深度均值 

# pic_save_name="f_mean_station_label"
# need=pd.read_table("F:\\f\\snow_sts_data\\1981-2020\\snow_pre_gss.txt",
#                           sep='\s+',na_values=32700)

# snow_f= need.groupby(by=['station'])['snow'].sum()
# pre_f=need.groupby(by=['station'])['dailypre'].mean() 
# gss_f=need.groupby(by=['station'])['gss'].mean()


#%% 站点

# # # #添加位置信息，法二
# path_sta='F:\\f\\snow_sts_data\\after_quality_control\\tp_sta_info_by2014.txt'
# sta=pd.read_table(path_sta,sep = ",",usecols=['station','lon','lat'])
# sta.set_index('station', inplace=True) # column 改为 index
# sta0=pd.read_table(path_sta,sep = ",",usecols=['station','alti'])
# sta0.set_index('station', inplace=True) # column 改为 index

# snow_sta=pre_f.index
# snow_sta_df=pd.DataFrame(snow_sta)
# snow_sta_df.loc[:,'useless']=0
# snow_sta_df.set_index('station', inplace=True)
# snow_sta_alti=pd.concat([sta0,snow_sta_df],axis=1)
# snow_sta_alti.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行
# snow_sta_alti.drop(['useless'],axis=1,inplace=True)

# # # 分别标准化 因为单位不一样 量纲不一致
# # df_zs=df.apply(lambda x : (x-np.min(x))/(np.max(x)-np.min(x)))#归一化
# #标准化，适用于有极端值的情况
# df_snow_zs = 1.0*(snow_f - snow_f.mean())/snow_f.std() 
# df_pre_zs = 1.0*(pre_f - pre_f.mean())/pre_f.std() 
# df_gss_zs = 1.0*(gss_f - gss_f.mean())/gss_f.std() 
# df_alti_zs = 1.0*(snow_sta_alti - snow_sta_alti.mean())/snow_sta_alti.std() 

# # df_pre_gss=pd.concat([pre_f,gss_f],axis=1) #同类型变量 可合并
# # df_pre_gss.columns=['pre_f','gss_f']
# # df_pre_gss.fillna(0,inplace=True)

# df_zs = pd.concat([df_snow_zs,df_pre_zs,df_gss_zs,df_alti_zs],axis=1)


#%%  # 先测试 聚类为？类最优 S局部最大，SSE拐点 绘图

# 参考https://blog.csdn.net/weixin_43718084/article/details/90273463

# import matplotlib.pyplot as plt
# from matplotlib.pyplot import MultipleLocator
# # 轮廓系数
# from sklearn.metrics import silhouette_score  

# plt.figure(figsize=(4,4))#绘制画布
  
# S = []  # 存放轮廓系数
# num = range(2,10)#分别模拟k为2~9的情况
# for i in num:
#     kmeans = KMeans(n_clusters=i,random_state=150)  # 构造聚类器
#     kmeans.fit(df_zs)
#     S.append(silhouette_score(df_zs,kmeans.labels_,metric='euclidean'))
#     # silhouette_score()计算每类所有点的平均轮廓系数，而silhouette_samples()返回每个点的轮廓系数
    
    
# plt.plot(num,S,'r*:')#'b*:'为线的格式设置，b表示蓝色，*为点的标记，:表示线型为点状线条。
# plt.xlabel('k',fontsize=12,fontproperties='Helvetica')
# plt.ylabel('S',fontsize=12,fontproperties='Helvetica')
# # plt.title('find the best K value')
# plt.tick_params(labelsize=12) #坐标轴标签字号

# x_minor_locator=MultipleLocator(1)
# ax = plt.gca()#获取大图边框
# ax.xaxis.set_minor_locator(x_minor_locator)

# # plt.text(1.56,0.319,'(a)', fontsize=13,color = 'black')

# plt.savefig(pic_dir+pic_save_name+'路径分类轮廓系数.jpg', dpi=1000, bbox_inches = 'tight')
# plt.show()

# # SSE误差平方和绘图
# num = range(1,10)#分别模拟k为1~9的情况

# plt.figure(figsize=(4,4))#绘制画布

# sse_result=[]#用于存放每种k聚类后的SSE
# for k in num:
#     kmeans=KMeans(n_clusters=k)
#     kmeans.fit(df_zs)
#     sse_result.append(kmeans.inertia_)#inertia_表示样本到最近的聚类中心的距离总和。
    
    
# plt.plot(num,sse_result,'b*:')#'b*:'为线的格式设置，b表示蓝色，*为点的标记，:表示线型为点状线条。
# plt.xlabel('k',fontsize=12,fontproperties='Helvetica')
# plt.ylabel('SSE',fontsize=12,fontproperties='Helvetica')
# plt.tick_params(labelsize=12) #坐标轴标签

# x_minor_locator=MultipleLocator(1)
# ax = plt.gca()#获取大图边框
# ax.xaxis.set_minor_locator(x_minor_locator)

# # plt.text(0.6,1036,'(b)', fontsize=13,color = 'black')

# plt.savefig(pic_dir+pic_save_name+'路径分类误差平方和.jpg', dpi=1000, bbox_inches = 'tight')
# plt.show()


#%% 聚类 结果保存 

# km = KMeans(n_clusters=2,random_state=150)#构造聚类器,random_state=150

# # km = KMeans(n_clusters=3,init=init,n_init=1,random_state=150)#构造聚类器,
# # random_state=150
# km.fit(df_zs)#聚类,init=init,n_init=1
# # label0 = km.labels_ #获取聚类标签 和下面是一样的
# label=km.predict(df_zs)#分组结果

# df_zs['label']=label

# num_label_all=df_zs['label'].value_counts()
# print('所有分类',num_label_all)

# df1=df_zs[['label']]

# df2=pd.concat([sta,df1],axis=1)
# df3=df2.reset_index()
# df3.dropna(axis=0, how='any',inplace=True) #删除任何有nan的行

# df3.to_csv("F:\\f\\snow_sts_data\\RTC\\"+pic_save_name+".txt",index = False,
#                 sep=' ')
# # a=df3[(df3['lon']>=95.5)&(df3['lon']<=97.2)&\
# #       (df3['lat']>=32.8)&(df3['lat']<=35)]


#%% 人工修正

# pic_save_name="f_mean_station_label"
# a_info=pd.read_table("F:\\f\\snow_sts_data\\RTC\\"+pic_save_name+".txt",
#                     sep='\s+',na_values=32700)

# # E
# p1= Path([(86.2,37.8),(99.3,35.1),(100.8,32.1),( 100.8,27.8),(105,27.8),
#           (105,40),(86.2,40),(86.2,37.8)])
# # C
# p2= Path([(82,36.4),(88,30),(95,30.4),(97.5,32.1),(100.8,32.1),(99.3,35.1),
#           (86.2,37.8),(82,36.4)])
# # # 原来的S  
# # p3= Path([(79.1,32.5),(87,28.2),(89.5,28.5),(92.5,28.8),(95,29.3),
# #           (98,30.5),(100.8,30.5),(100.8,32.1),(97.5,32.1),(95,30.4),(88,30),
# #           (82,36.4),(79.1,32.5)])
# # # SW  
# # p4= Path([(79.1,27),(100.8,27),(108,30.5),(98,30.5),(95,29.3),(92.5,28.8),
# #           (89.5,28.5),(87,28.2),(79.1,32.5),(79.1,27)])

# # 现在的S 原S与SW合并 
# p3= Path([(79.1,27),(100.8,27),(100.8,32.1),(97.5,32.1),(95,30.4),(88,30),
#           (82,36.4),(79.1,32.5),(79.1,27)])
# sta_label=[]
# for j in range(len(a_info)):
#     if p1.contains_point((a_info['lon'][j],a_info['lat'][j])):
#         w=1
#     elif p2.contains_point((a_info['lon'][j],a_info['lat'][j])):
#         w=2
#     elif p3.contains_point((a_info['lon'][j],a_info['lat'][j])):
#         w=3  
#     sta_label.append(w)
# a_info.loc[:,"sta_label"]=sta_label        

# a_info.to_csv("F:\\f\\snow_sts_data\\RTC\\"+pic_save_name+"_modify.txt",
#               index = False, sep=' ',na_rep=32700)

