# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:33:17 2020

@author: Suthermd
"""


import os
import pandas as pd
output = 'metadata_bathy.xlsx'
bathy = 'metadata_bathy.csv'
meta = 'metadata.csv'

os.chdir('D:\\OEH\\NESP\\MB\\Bathy_Extract\\Broughton\\T002')
cur_dir = os.getcwd()

df1 = pd.read_csv(bathy, header=0)
df_metadata = pd.read_csv(meta, header=0)

df2 = df1[["timestamp","Bathymetry_Gridded(m)","Altitude_Inferred(m)"]]

df3 = pd.merge(left=df_metadata, right = df2, how='left', on=["timestamp"])

df3['Bathymetry_Gridded(m)'] = df3['Bathymetry_Gridded(m)'].apply(lambda x: round(x, 3))
df3['Altitude_Inferred(m)'] = df3['Altitude_Inferred(m)'].apply(lambda x: round(x, 3))




df3.to_csv('metadata_new.csv', index=False)


print(df3)
