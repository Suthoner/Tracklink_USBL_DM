# -*- coding: utf-8 -*-
"""
Created on Fri May 15 11:58:23 2020

@author: Suthermd
"""


import os
import numpy as np
import pandas as pd

os.chdir('D:\\OEH\\NESP\\SQIDL\\NSW_DPIE\\TDS')
cur_dir = os.getcwd()

merge_AV = 'metadata_AV.xlsx'
merge_final = 'metadata.csv'

for root, subdirs, files in os.walk(cur_dir):
    for file in files:
        if file == merge_AV:
            n_root = root.replace('merge','')
            fn = os.path.join(root,file)
            print(fn)            
            fn_path = os.path.join(n_root,merge_final)
            print(fn_path)
            #dfd1 = pd.ExcelFile(fn)
            df1 = pd.read_excel(fn)

            df1.latitude_TDS.fillna(df1.AV_latitude_TDS, inplace=True)
            df1.longitude_TDS.fillna(df1.AV_longitude_TDS, inplace=True)
            df1.depth_USBL.fillna(df1.AV_depth_USBL, inplace=True)
            df1.SlantRange.fillna(df1.AV_SlantRange, inplace=True)
            df1.z.fillna(df1.AV_z, inplace=True)
            df1.Z.fillna(df1.AV_Z, inplace=True)
            df1.X.fillna(df1.AV_X, inplace=True)
            df1.BRG.fillna(df1.AV_BRG, inplace=True)
            
            df1['Av_True=1'] = np.where((df1['latitude_TDS'] == df1['AV_latitude_TDS']) & (df1['longitude_TDS'] == df1['AV_longitude_TDS']) & (df1['depth_USBL'] == df1['AV_depth_USBL']), 1, np.nan)
            df1 = df1[df1['filename'].notna()]
            
            df1 = df1[['filename','timestamp','latitude_TDS','longitude_TDS','depth_TDS','latitude_SHIP','longitude_SHIP','sounder_SHIP','COG_SHIP','SOG_SHIP','Roll_TDV','Pitch_TDV','Yaw_TDV', 'depth_USBL','SlantRange','z','Z','X','BRG','Av_True=1']]
            df1 = df1.rename(columns={'depth_TDS':'depth_TDS(m)', 'sounder_SHIP':'sounder_SHIP(m)','SOG_SHIP':'SOG_SHIP(kn)','depth_USBL':'depth_USBL(m)','SlantRange':'SlantRange_USBL','z':'z_USBL','Z':'Z_USBL','X':'X_USBL','BRG':'BRG_USBL'})

#ROUNDS GPS POSITIONS TO THEIR ORIGINAL ACCURACY            
            df1['latitude_TDS'] = df1['latitude_TDS'].apply(lambda x: round(x, 7))
            df1['longitude_TDS'] = df1['longitude_TDS'].apply(lambda x: round(x, 7))
            df1['latitude_SHIP'] = df1['latitude_SHIP'].apply(lambda x: round(x, 7))
            df1['longitude_SHIP'] = df1['longitude_SHIP'].apply(lambda x: round(x, 7))



            #print(df1["latitude_SHIP"])
            df1.to_csv(fn_path, index=False) 

