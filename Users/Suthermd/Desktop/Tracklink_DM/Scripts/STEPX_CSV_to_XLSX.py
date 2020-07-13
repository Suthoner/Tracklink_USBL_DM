# -*- coding: utf-8 -*-
"""
Created on Sun May 17 13:56:41 2020

@author: Suthermd
"""

import os
import pandas as pd
output = 'metadata_bathy.xlsx'
file = 'metadata_bathy.csv'

os.chdir('D:\\OEH\\NESP\\MB\\Bathy_Extract\\Broughton\\')
cur_dir = os.getcwd()

for root, subdirs, files in os.walk(cur_dir):
    for i in files:
        if i == file:
            fn = os.path.join(root, i)
            fn_path = os.path.join(root,output)
            print(fn)
            df1 = pd.read_csv(fn, header=0)
            df1.to_excel(fn_path,index=0)