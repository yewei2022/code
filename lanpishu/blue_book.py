# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 09:15:31 2024
数据清洗,切割字符串
找到区县对应的市
用缺失值补全12个月
将某两列名称分别变为行和列索引重组数据
时间和字符串转换
@author: yewei
"""

import pandas as pd
import numpy as np

f_dir = r'C:\Users\yewei\Desktop\蓝皮书'
data_dir = r'C:\Users\yewei\Desktop\蓝皮书\data'
pic_dir = r'C:\Users\yewei\Desktop\蓝皮书\picture'


#%% branch1 step1 分割字符串

# data = pd.read_excel(f_dir + '\原始统计信息.xls', sheet_name=0)
# data.columns =['date','title','content']

# #将title字符串中包含“测试”字符的行设为None
# data["title"].mask(data.title.str.contains("测试"), None, inplace=True)
# #删除预警信号的预警信息
# data["content"].mask(data.content.str.contains("解除"), None, inplace=True)
# #删除空行
# data1 = data.dropna(axis=0,how='any')
# #筛选出'content'字符串中包含“气象台”字符的行
# df_all = data1[data1['content'].str.contains('气象台')]

# # 删除'content'字符串中的标点符号
# df_all['content'].replace(['【','】','，'], '',regex = True, inplace=True)

# df_all['split'] = df_all["title"].str.split("色", expand=True)[0]
# df_all['color'] = df_all["split"].str[-1]
# df_all['disaster'] = df_all["split"].str[:-1]
# df_all['district'] = df_all["content"].str.split("气象台", expand=True)[0]
# df_all['month'] = df_all['date'].dt.month #取出时间中的月份

# df_split = df_all.drop(["title","content","split"],axis=1)

#%% branch1 step2 找到区县对应的市

# dic1 = pd.read_excel(f_dir + "\市-区县.xlsx",sheet_name = 2,
#                     index_col = None)
# dic1 = dic1.rename(columns = {'市':'id','区县':'values'})
# #============================================================

# def find_ids(value):
#     #join相当于把所有字符都练成一串，例如巴中的'巴中市','巴州区','平昌县',连成一个字符串
#     id2= dic1.loc[dic1['values'].str.join(sep = "").str.contains(value), "id"]
#     id3 = id2.values
#     return id3

# # id2 =find_ids('安岳县')
# # print(id2) #测试

# df_split.loc[:,'city']= df_split['district'].apply(find_ids)

#%% branch1 step3 发现理县包含在两个市，手动调整

# city_str = df_split['city'].astype(str)
# df_split.loc[:,'city'] = city_str.replace(r'[^\w\s]+', '',regex = True, inplace=False)
# #手动替换特定值所在行的另一列值
# df_split.loc[df_split["district"] == "眉山市", "city" ] = "眉山市"
# df_split.loc[df_split["district"] == "乐山市", "city" ] = "乐山市"
# df_split.loc[df_split["district"] == "理县", "city" ] = "阿坝州"
# df_split.loc[df_split["district"] == "渠县", "city" ] = "达州市"
# df_split.loc[df_split["district"] == "荣县", "city" ] = "自贡市"
# df_split.to_csv(data_dir+"\清洗后数据.csv",index = False)


#%% branch2 step1 统计

# # 读取csv文件
# data = pd.read_csv(data_dir +"\清洗后数据.csv")
# data.loc[:,'count'] = 1
# # print(data.loc[data["disaster"] == "通川区暴雨"])
# # # 删除'disaster'字符串"通川区暴雨"的"通川区"
# data['disaster'].replace(['通川区'], '',regex = True, inplace=True)

# #开始统计
# #统计级别
# color = data.groupby(by=['color'])['count'].sum()
# disaster = data.groupby(by=['disaster'])['count'].sum()
# color = data.groupby(by=['color'])['count'].sum()
# month = data.groupby(by=['month'])['count'].sum()
# month_disaster = data.groupby(by=['month','disaster'])['count'].sum()
# mon_dis1 = month_disaster.reset_index(drop=False)
# # 计算各月，每一种灾害类型占当月百分比
# month1 = month.reset_index(drop=False)
# month1.loc[:,'per']  = month1['count']/month1['count'].sum()
# for j in range(0,len(mon_dis1)):
#     a1 =mon_dis1['month'][j]
#     mon =  month1.loc[month1['month']==a1,'count']
#     mon_dis1.loc[[j],'sum'] =  int(mon)
    
# mon_dis1.loc[:,'per']  = mon_dis1['count']/mon_dis1['sum']

# # 统计各市州预警总量
# data_sichuan = data[~(data['city']=="四川省")] #不要四川省台
# city = data_sichuan.groupby(by=['city'])['count'].sum()

# # #统计各市州不同预警类型总量
# city_dis = data_sichuan.groupby(by=['city','disaster'])['count'].sum()
# city_dis1 = city_dis.reset_index(drop=False)
# # 变成行索引为市 列索引为灾害
# city_dis2 = city_dis1.pivot(index = 'city', columns = 'disaster',values = 'count')
# city_dis3 = city_dis2.fillna(0)
# #取出最大值
# city_max= city_dis3.max(axis=1)
# #取出每行最大值所在索引
# city_dis3['1st'] = city_dis3.columns.to_numpy()[np.argsort(city_dis3.to_numpy())[:, -1]]
# city_dis3['1st'] = city_dis3['1st']+" N0.1"
# #最大值连接到原列表
# city_dis3['value'] = city_max

# # 统计每日总量
# data.loc[:,'time'] =pd.to_datetime(data['date']) #转换为时间戳time
# data.loc[:,'day'] = data['time'].dt.strftime('%Y-%m-%d') #转换成年月日字符串
# calendar = data.groupby(by=['day'])['count'].sum()
# calendar1 = calendar.reset_index(drop=False)
# calendar1.loc[:,'date'] =pd.to_datetime(calendar1['day'])
# calendar2 = calendar1.drop('day', axis=1)
# calendar2 = calendar2.reindex(columns=['date','count'])
# calendar3 = calendar2.values
# rows =[list(row) for row in calendar3] #必须列表嵌套列表之后才能绘图

# # 分析数据
# # a1 = data[data['day']=="2023-07-03"]
# a1 = data
# a2 = a1.groupby(by=['disaster'])['count'].sum()
# a3 = a1.groupby(by=["color",'city'])['count'].sum()
# a4 = a3.reset_index(drop=False)
# a5 = a4[a4['color']=="红"]
# # data_sorted = data.sort_values(['time'], ascending=True)
# # a4 = data_sorted.drop_duplicates(["color","disaster"], keep='first').reset_index(drop=True)



# # #保存文件
# color.to_csv(data_dir +"\color.csv",index = True)
# disaster.to_csv(data_dir +"\disaster.csv",index = True)
# month1.to_csv(data_dir +"\month.csv",index = False)
# mon_dis1.to_csv(data_dir +"\各类灾害月发布量及其占当月总量百分比.csv",index = False)
# city.to_csv(data_dir +"\地市州发布数.csv",index = True)
# city_dis3.to_csv(data_dir +"\地市州各类型发布数.csv",index = True)
# city_dis3.to_csv(data_dir +"\地市州发布数NO1.csv",index = True,columns =['1st','value'])
# calendar2.to_csv(data_dir +"\日历.csv",index = False)



#%% branch2 step2 所有灾害类型饼图

# disaster1 = disaster.reset_index(drop=False)
# # disaster1.loc[:,'per']  = disaster1['count']/disaster1['count'].sum()

# from pyecharts import options as opts
# from pyecharts.charts import Pie
# from pyecharts.globals import ThemeType
# c = (
#       #设置主题
#     Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
#     .add(
#         # 系列名称
#         "",   
        
#         # 系列数据项  格式为 [(key1, value1), (key2, value2)]
#         [list(z) for z in zip(disaster1['disaster'], disaster1['count'])],  
        
#         # 系列 label 颜色  Optional[str]
#         color = None,
         
#         # 饼图的半径，数组的第一项是内半径，第二项是外半径
#         # 默认设置成百分比，相对于容器高宽中较小的一项的一半
#         # Optional[Sequence]
#         radius = None,
        
#         # 饼图的中心（圆心）坐标，数组的第一项是横坐标，第二项是纵坐标
#         # 默认设置成百分比，设置成百分比时第一项是相对于容器宽度，第二项是相对于容器高度
#         # Optional[Sequence]
#         center =None,

#         # 是否展示成南丁格尔图，通过半径区分数据大小，有'radius'和'area'两种模式。
#         # radius：扇区圆心角展现数据的百分比，半径展现数据的大小
#         # area：所有扇区圆心角相同，仅通过半径展现数据大小
#         # Optional[str]
#         rosetype = None, # "radius"
    
#         # 饼图的扇区是否是顺时针排布。
#         is_clockwise = True,
    
#         # 标签配置项，参考 `series_options.LabelOpts`
#         # label_opts = opts.LabelOpts(),
#         # label_opts = False,
    
#         # 提示框组件配置项，参考 `series_options.TooltipOpts`
#         tooltip_opts = None,
    
#         # 图元样式配置项，参考 `series_options.ItemStyleOpts`
#         itemstyle_opts = None,
    
#         # 可以定义 data 的哪个维度被编码成什么。
#         # types.Union[types.JSFunc, dict, None]
#         encode = None,
#         )
#     # 全局配置项
#     # 标题和图例
#     .set_global_opts(title_opts=opts.TitleOpts(title=""),
#                       legend_opts=opts.LegendOpts(orient="vertical",
#                                                   pos_top="15%", pos_left="-2%",
#                                                   border_width=0)
#                       )
    
#     # 系统配置项
#     # 设置标签
#     .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}   {d}%",
#                                                 font_size =15,
#                                                 font_weight = "bold"))
#     .render(pic_dir+ "\pie_color.html")
# )



#%% branch2 step3 统计和绘制月分布

# dis_name = list(set(mon_dis1['disaster'].tolist()))

# # #测试单个
# # list0 = mon_dis1[mon_dis1['disaster']==dis_name[0]]
# # # 把原数据的月份设为索引，因为要判断月份是不是缺
# # list0.set_index('month', inplace=True) # column 改为 index
# # new_df0 = pd.DataFrame({'month': list(range(1,13))})#月份单独生成数据帧
# # new_df0['count'] = new_df0['month'].map(lambda x: list0.loc[x]['count'] if x in list0.index else None)
# # new_df0['per'] = new_df0['month'].map(lambda x: list0.loc[x]['per'] if x in list0.index else None)
# # new_df1 = new_df0.drop('month', axis=1)
# # # https://blog.csdn.net/weixin_42081390/article/details/121486034 转字典
# # dic  = new_df1.to_dict('records')
# # print(dic)

# # 批量
# plot_df = []
# for i in range(0,len(dis_name)):
#     list0 = mon_dis1[mon_dis1['disaster']==dis_name[i]]
#     # 把原数据的月份设为索引，因为要判断月份是不是缺
#     list0.set_index('month', inplace=True) # column 改为 index
#     new_df0 = pd.DataFrame({'month': list(range(1,13))})#月份单独生成数据帧
#     new_df0['count'] = new_df0['month'].map(lambda x: list0.loc[x]['count'] if x in list0.index else None)
#     new_df0['per'] = new_df0['month'].map(lambda x: list0.loc[x]['per'] if x in list0.index else None)
#     new_df1 = new_df0.fillna(0)
#     #保存每类灾害月分布数据
#     new_df1.to_csv(data_dir +"\\" + dis_name[i]+"各月分布.csv",index = False)
#     new_df2 = new_df1.drop(['month'], axis=1)
#     # dic  = new_df2.to_dict('records')
#     plot_df.append(new_df2)

# print(plot_df[0]['count'])
 

# # 绘图   
# # https://gallery.pyecharts.org/#/Bar/stack_bar_percent 柱状图
# from pyecharts import options as opts
# from pyecharts.charts import Bar
# from pyecharts.commons.utils import JsCode
# from pyecharts.globals import ThemeType

# c = (
#     Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT,
#                                       width='1000px',height='600px'))
#     .add_xaxis(list(range(1,13)))
#     # 数据堆叠,同个类目轴上stack值相同可堆叠
#     .add_yaxis(dis_name[0], plot_df[0]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[1], plot_df[1]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[2], plot_df[2]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[3], plot_df[3]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[4], plot_df[4]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[5], plot_df[5]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[6], plot_df[6]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[7], plot_df[7]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[8], plot_df[8]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[9], plot_df[9]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[10], plot_df[10]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[11], plot_df[11]['count'].tolist(), stack="stack1", category_gap="50%")
#     .add_yaxis(dis_name[12], plot_df[12]['count'].tolist(), stack="stack1", category_gap="50%")
#    # .set_global_opts(xaxis_opts=opts.AxisOpts(name='X轴名称',name_location='middle' 
#    #                                           #坐标轴名字所在的位置,name_gap=25#坐标轴名字与坐标轴之间的距离,
#    #                                           name_rotate=15 #坐标轴名字旋转角度,offset=5 #坐标轴X的值距离X轴的距离,
#    #                                           name_textstyle_opts=opts.TextStyleOpts(color='black',font_style='italic'
# #                                                                                  ## 可选：'normal'，'italic'，'oblique',
# #                                                                                  font_weight='bolder'    
# #                                                                                  #粗细 'normal'，'bold'，'bolder'，'lighter' 
# #                                                                                  ,font_family= 'monospace'# 还可以是 'serif' , 
# #                                                                                  'monospace', 'Arial', 'Courier New', 'Microsoft YaHei', ...,
#                                          # font_size=14,background_color='grey'#文字背景颜色,
#                               #            border_color='black' #文字块边框颜色)##X轴名称的格式配置,
#                               #       axistick_opts=opts.AxisTickOpts(is_inside=True #刻度线是否在内侧) #坐标轴刻度配置项,
#                               #       axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(width=3 ##设置宽度,
#                               #       opacity=0 #设置透明度,
#                               #       type_='dashed'  # 'solid', 'dashed', 'dotted',color='black') )#坐标轴线的配置项,
#                               #   axislabel_opts=opts.LabelOpts(font_size=13#字的大小,rotate=15 #字旋转的角度)##坐标轴标签的格式配置)))
#                               # bar1.render('bar1.html') ###输出html文件
#     #设置数值标签
#     # .set_series_opts(
#     #     label_opts=opts.LabelOpts(
#     #         position="right",
#     #         formatter=JsCode(
#     #             "function(x){return Number(x.data)}"
#     #         ),
#     #     )
#     # )
#     # 不要数值标签
#     .set_series_opts(
#         label_opts=opts.LabelOpts(False)
#     )
#     .set_global_opts(title_opts=opts.TitleOpts(title=""),
#                       legend_opts=opts.LegendOpts(orient="horizontal",
#                                                   pos_top="0%", pos_left="0%",
#                                                   border_width=0, 
#                                                   textstyle_opts=opts.
#                                                   TextStyleOpts(color='black',font_size=16,
#                                                                 font_weight="bold")),
#                       xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='black',font_size=16,font_weight="bold")),
#                       yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='black',font_size=16,font_weight="bold"))
#                       )
#     .render(pic_dir+"\stack_bar_percent.html")
# )



# # 法二
# from pyecharts.charts import *
# from pyecharts import options as opts
# from pyecharts.faker import Faker

# def bar_stack():
#     # 创建 Bar 实例对象
#     bar = Bar(init_opts=opts.InitOpts(theme='light',
#                                       width='1000px',
#                                       height='600px'))
#     # 添加 x 轴数据
#     bar.add_xaxis(list(range(1,13)))
#     # 添加 y 轴数据，stack 值一样的系列会堆叠在一起
#     #都是stack1代表在同一个柱子上stack2是第二个柱子了
#     # 数据堆叠,同个类目轴上stack值相同可堆叠
#     bar.add_yaxis(dis_name[0], plot_df[0]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[1], plot_df[1]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[2], plot_df[2]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[3], plot_df[3]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[4], plot_df[4]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[5], plot_df[5]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[6], plot_df[6]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[7], plot_df[7]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[8], plot_df[8]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[9], plot_df[9]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[10], plot_df[10]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[11], plot_df[11]['count'].tolist(), stack="stack1", category_gap="50%")
#     bar.add_yaxis(dis_name[12], plot_df[12]['count'].tolist(), stack="stack1", category_gap="50%")
#     # bar.set_global_opts(
#     #     yaxis_opts = opts.AxisOpts(name = "",max_=5000))
#     return bar

# # 生成堆叠柱状图
# chart = bar_stack()
# # 保存堆叠柱状图
# chart.render(pic_dir+"\stack_bar_percent.html")


#%%  各市州不同类型的散点图 画不出来

# city_dis_plot = city_dis3.drop(["1st","value"],axis=1)
# city_name = city_dis_plot.index.tolist()
# dis_name = city_dis_plot.columns.tolist()
# print(list(city_dis_plot.iloc[0,:]))



# from pyecharts import options as opts
# from pyecharts.charts import Scatter

# c = (
#     Scatter()
#     .add_xaxis(city_name)
#     .add_yaxis(dis_name[0], list(city_dis_plot.iloc[:,0]))
#     .set_global_opts(
#         title_opts=opts.TitleOpts(title="Scatter-VisualMap(Size)"),
#         visualmap_opts=opts.VisualMapOpts(type_="size", max_=150, min_=20),
#     )
#     .render(pic_dir + "\scatter_visualmap_size.html")
# )

#%% 日历图

# import random
# import datetime

# import pyecharts.options as opts
# from pyecharts.charts import Calendar


# (
#     Calendar()
#     .add(
#         series_name="",
#         yaxis_data=rows,
#         calendar_opts=opts.CalendarOpts(
#             pos_top="120",
#             pos_left="30",
#             pos_right="30",
#             range_="2023",
#             yearlabel_opts=opts.CalendarYearLabelOpts(is_show=False),
#         ),
#     )
    
#     .set_global_opts(
#         title_opts=opts.TitleOpts(pos_top="30", pos_left="center", title=""),
#         # 设置图例配置项
#         legend_opts=opts.LegendOpts(
#             pos_right="right",  # 设置为水平居左
#             pos_bottom="top"  # 设置为垂直居下
#         ),
#         visualmap_opts=opts.VisualMapOpts(
#             max_=400, min_=0, orient="horizontal", is_piecewise=False,
#         pos_right="right",  # 设置为水平居左
#         pos_bottom="180"  # 设置为垂直居下 越大越上
#         ),
#         # xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='black',font_size=16,font_weight="bold")),
#         #                       yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(color='black',font_size=16,font_weight="bold")),
#     )
#     .render(pic_dir + "\calendar_heatmap.html")
# )
