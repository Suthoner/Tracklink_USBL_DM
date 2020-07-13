# -*- coding: utf-8 -*-
"""
Created on Tue May 12 18:53:04 2020

@author: suthermd
"""

#MUST HAVE IMAGES SEPARATED BY TRANSECTS AND SITTING IN 'image'
#MUST SPECIFY DATA DIRECTORY
#MUST MODIFY 'NAME' BASED ON PROJECT (I.E. 'NESP')
#MUST MODIFY 'NEW_NAME' BASED ON 'TARGET' LIST INDEX VALUES (I.E. 'TARGET[7]')


import os
from PIL import Image
from PIL.ExifTags import TAGS
import time
import pandas as pd

def get_exif(fn):
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    return ret

os.chdir('D:\\OEH\\NESP\\SQIDL\\NSW_DPIE\\TDS') #INPUT DIRECTORY
cur_dir = os.getcwd()

for root, subroot, files in os.walk(cur_dir):
    if root.endswith('images'):
        root_new = root.replace("images","merge")
        imagemetadata = os.path.join(root_new,'imagesmetadata.csv')
        met = []
        name = 'NSW_DPIE_TDS_' #CUSTOMISE PER PROJECT (I.E. 'NESP')
        for file in files:
            if file.endswith(".JPG"):
                #print(root)
                fn = file
                picture = os.path.join(root, file)          #creates object for function: 'get_exif()' to interogate
                time = get_exif(picture)["DateTimeOriginal"]            
                datetime = time.replace(':','').replace(' ', '_')                                        #STRUCTURE IMG DATETIME STRING                 
                #print(datetime)
                Target = root.split('\\')
                #print(Target)
                new_name = (name + Target[6] + '_' + Target[7] + '_' + datetime + 'UTC.JPG').replace(" " ,"_")   #CUSTOMISE PER DIRECTORY (I.E. 'TARGET[7]')
                #print(new_name)
                #os.rename(os.path.join(root, file), os.path.join(root, new_name))
                metadata = new_name + ',' + time.replace(':','-',2)             
                met.append(metadata)
        df = pd.DataFrame(met,index=None,columns=['filename,timestamp'])
        df.to_csv(imagemetadata, sep=',',index=False)
        
        