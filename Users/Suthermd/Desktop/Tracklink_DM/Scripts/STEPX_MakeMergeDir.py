# -*- coding: utf-8 -*-
"""
Created on Fri May 15 12:03:25 2020

@author: Suthermd
"""


import os
import numpy as np
import pandas as pd

os.chdir('D:\\OEH\\NESP\\SQIDL\\NSW_DPIE\\TDS')
cur_dir = os.getcwd()

images = 'images'

for root, subdirs, files in os.walk(cur_dir):
    if images in root:
        print(root)
        new_dir = root.replace('images', 'merge')
        print(new_dir)
        os.makedirs(new_dir)