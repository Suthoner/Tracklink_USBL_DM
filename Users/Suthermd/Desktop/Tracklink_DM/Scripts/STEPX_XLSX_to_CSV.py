# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:19:34 2020

@author: suthermd
"""


import os
import pandas as pd

os.chdir('D:\\OEH\\NESP\\MB\\Bathy_Extract\\Broughton\\') #INPUT DIRECTORY
cur_dir = os.getcwd()

a = os.listdir(cur_dir)

#print(a)

for root, subdir, files in os.walk(cur_dir):
    for file in files:
        if file.endswith('.xlsx'):
            fpath = os.path.join(root,file)
            #print(fpath)
            fn = file
            #print(fn)
            xlsx = pd.read_excel(fpath)
            #print(xlsx) 
            new_fn = fn.replace('xlsx','csv')
            #print(new_fn)
            new_fpath = os.path.join(root, new_fn)
            #print(new_fpath)
            xlsx.to_csv(new_fpath, index=False)
            #print('NEXT FILE:')
            #print("")

#print(a)            
            
