# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 14:39:53 2023
分析气象数据计算浓雾日数 道路结冰日数 百分位数
@author: yewei
"""

import pandas as pd

path_fog = r'D:\YEWEI\project\traffic\2024\data\fog_year_avg_days.txt'
fog = pd.read_table(path_fog,sep = "\s+",na_values= 32700)
fog1 = fog[fog['days']>0]
fog_quantile = fog1['days'].quantile([0.25,0.5,0.65,0.7,0.75,0.8,0.85,0.9,0.95])
print(fog_quantile)

path_fog = r'D:\YEWEI\project\traffic\2024\data\tmp0_year_avg_days.txt'
ice = pd.read_table(path_fog,sep = "\s+",na_values= 32700)
ice1 = ice[ice['days']>0]
ice_quantile = ice1['days'].quantile([0.25,0.5,0.65,0.7,0.75,0.8,0.85,0.9,0.95])
print(ice_quantile)
