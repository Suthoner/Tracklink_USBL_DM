# -*- coding: utf-8 -*-
"""
Created on Mon May 18 09:22:00 2020

@author: Suthermd
"""


#This program reads the number of image files in a folder and compares that value to the number of rows in the associated metadata file
#to confirm that all images have been included

import os
import pandas as pd

#def append(x):
#    images = []
#    images.append(x)
#    df = pd.DataFrame(images, index='filename')
#    df.to_excel
#    open()

os.chdir('D:\\OEH\\NESP\\SQIDL\\NSW_DPIE\\TDS\\NESP_HUNTER_BROUGHTON')
cur_dir = os.getcwd()

Target = 'metadata.csv'

for root, subdirs, files in os.walk(cur_dir):
    for file in files:
        if file == Target:
            fn = os.path.join(root, file)
            df = pd.read_csv(fn, header=0)
            length = len(df.index)
            print(f'{root} length = {length}')
        if file.endswith('.JPG'):
#            print(len(file))
