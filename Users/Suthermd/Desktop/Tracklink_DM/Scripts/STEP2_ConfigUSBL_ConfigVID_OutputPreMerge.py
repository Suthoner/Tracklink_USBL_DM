# -*- coding: utf-8 -*-
"""
Created on Wed May 13 10:51:05 2020

@author: suthermd
"""

import os
import pandas as pd

os.chdir("D:\\OEH\\NESP\\SQIDL\\NSW_DPIE\\TDS") #INPUT DIRECTORY
cur_dir = os.getcwd()
usbl = "usbl.csv"
vid = "vid.csv"
img = "imagesmetadata.csv"
usbl_out = "usbl_merge.csv"
vid_out = "vid_merge.csv"
merge = "merge"
merge_out = "metadata_AV.xlsx"

#CONVERTS USBL FILE INTO REQUIRED FORMAT FOR MERGE ('USBL_MERGE.CSV')

for root, subdir, files in os.walk(cur_dir):
   for file in files:
        if file == usbl:
            fn = os.path.join(root, file)
            #print(fn)
            fn_path = os.path.join(root + "\\" + "merge"+ "\\")         #CREATES OUTPUT XLSX FILE ROOT
            #print(fn_path)
            df1 = pd.read_csv(fn, header=0)
            #print(df1)
            df1 = df1.rename(columns={'D' : 'day', 'M' : 'month', 'Y' : 'year', 'H' : 'hour', 'MM' : 'minute', 'S' : 'second'})
            df1["date"] = pd.to_datetime(df1[['day','month','year']])
            #print(df1["date"])
            df1["time"] = pd.to_datetime(df1["hour"].astype(int).astype(str)+":"+ df1["minute"].astype(int).astype(str)+":"+ df1["second"].astype(int).astype(str), format = '%H:%M:%S').dt.time #combines hour, minute, second columns into one
            #print(df1["time"])
            df1["timestamp"] = df1.apply(lambda r : pd.datetime.combine(r["date"],r["time"]),1).astype(str) #combines date and time columns into one
            df1["timestamp"] = df1["timestamp"].replace("-","/")
            print(df1["timestamp"])
            df1["latitude_TDS"] = ((df1["FISHLAT"]+3200)/60)+(-32) #This converts deciaml minutes for decimal degrees
            #print(df1["latitude_TDS"])
            df1["longitude_TDS"] = ((df1["FISHLONG"]-15200)/60)+(152)
            #print(df1["longitude_TDS"])
            df1 = df1.rename(columns={"FISHDEPTH" : "depth_USBL"})
            df1 = df1[df1.Check == 0]   #Removes all rows where check was not zero (i.e. good)
            df1 = df1[["timestamp", "latitude_TDS", "longitude_TDS", "depth_USBL", "Target", "Check", "SlantRange","z", "Z", "X","BRG","D1","D2","D3","D4","D5","D6", "D7", "D8", "D9", "D10", "D11", "D12", "D13"]] #this rearranges all columns
            #print(df2)
            df1.to_csv(fn_path + usbl_out, index=False)
            
            
#CONVERTS VID FILE INTO REQUIRED FORMAT FOR MERGE ('VID_MERGE.CSV')
        if file == vid:
            fn = os.path.join(root, file)
            #print(fn)
            fn_path = os.path.join(root + "\\" + "merge"+ "\\")        #CREATES OUTPUT XLSX FILE ROOT
            #print(fn_path)
            df3 = pd.read_csv(fn, header=0)
            df3["Time"] = df3["PC_Time"].astype(str) # converts PC_Time into string
            df3["Time"] = df3["Time"].str.replace('\..*','') # removes decimal seconds from time values
            #print(df3["Time"])
            df3["Date"] = df3["PC_Date"].astype(str) #converts PC_Date into string
            #print(df3["Date"])
            df3["timestamp"] = df3["Date"] + ' ' + df3["Time"] #combines date and time object strings
            df3["timestamp"] = df3["timestamp"].astype(str)
            df3["timestamp"] = df3["timestamp"].replace("-","/")
            #print(df3["timestamp"])
            df3["latitude_SHIP"] = (((df3["Ship_Lat"]-3200)/60)*(-1)-32)
            df3["longitude_SHIP"] = (((df3["Ship_Long"]-15200)/60)+152)
            df3["depth_TDS"] = (df3["Press(dBars)"]+0.54)   #adds depth offset from pressure guage to camera
            #print(df3["depth_TDS"])               
            df4 = df3[["timestamp", "latitude_SHIP", "longitude_SHIP", "Sounder Depth", "SOG", "COG", "Press(dBars)", "Roll", "Pitch", "Yaw"]]
            df4 = df4.rename(columns={"Sounder Depth" : "sounder_SHIP", "SOG" : "COG_SHIP", "COG" : "SOG_SHIP", "Roll" : "Roll_TDV", "Pitch" : "Pitch_TDV", "Yaw" : "Yaw_TDV", "Press(dBars)" : "depth_TDS"})
            df4.to_csv(fn_path + vid_out, index=False)

#MERGES USBL, VID, IMAGE FILES INTO SINGLE OUTPUT 'METADATA_AV.XLSX'

for root, subdirs, files in os.walk(cur_dir):
    if root.endswith(merge):
        fn_path = os.path.join(root + "\\" + merge_out)
        #print(fn_path)
        
        dfdi = os.path.join(root + "\\" + img)
        dfdu = os.path.join(root + "\\" + usbl_out)
        dfdv = os.path.join(root + "\\" + vid_out)  

       
        dfi = pd.read_csv(dfdi, header=0, sep=",", quoting=3)
        dfi.columns = dfi.columns.str.strip('" ')
        dfi.iloc[:, [0, -1]] = dfi.iloc[:, [0, -1]].apply(lambda x: x.str.strip('"'))
        dfu = pd.read_csv(dfdu, header=0)
        dfv = pd.read_csv(dfdv, header=0)
        
        dfi["timestamp"] = dfi["timestamp"].astype(str) 
        dfu["timestamp"] = dfu["timestamp"].astype(str)
        dfv["timestamp"] = dfv["timestamp"].astype(str)
        
#        print(dfi["timestamp"][0])
#        print(dfu["timestamp"][0]) 
#        print(dfv["timestamp"][0])
        
        df5 = pd.merge(left=dfv, right = dfu, how='left', on=["timestamp"])
        df5 = pd.merge(left=df5, right=dfi, how='left', on=["timestamp"])
        #print(df5)

        df5["AV_latitude_TDS"] = ""
        df5["AV_longitude_TDS"] = "" 
        df5["AV_depth_USBL"] = ""
        df5["AV_SlantRange"] = ""
        df5["AV_z"] = ""
        df5["AV_Z"] = ""
        df5["AV_X"] = ""
        df5["AV_BRG"] = ""
        #df5["AV_D1"] = ""
        #df5["AV_D2"] = ""
        #df5["AV_D3"] = ""
        #df5["AV_D4"] = ""
        #df5["AV_D5"] = ""
       # df5["AV_D6"] = ""
      #  df5["AV_D7"] = ""
     #   df5["AV_D8"] = ""
    #    df5["AV_D9"] = ""
   #     df5["AV_D10"] = ""
  #      df5["AV_D11"] = ""
 #       df5["AV_D12"] = ""
#        df5["AV_D13"] = ""
        
        #df5["timestamp"] = df5["timestamp"].astype(str)
#        df5 = df5[["filename","timestamp","latitude_TDS","AV_latitude_TDS","longitude_TDS","AV_longitude_TDS","depth_TDS","latitude_SHIP","longitude_SHIP","sounder_SHIP","COG_SHIP","SOG_SHIP","Roll_TDV","Pitch_TDV","Yaw_TDV","depth_USBL","AV_depth_USBL","SlantRange","AV_SlantRange","z","AV_z","Z","AV_Z","X","AV_X","BRG","AV_BRG","D1","AV_D1","D2","AV_D2","D3","AV_D3","D4","AV_D4","D5","AV_D5","D6","AV_D6","D7","AV_D7","D8","AV_D8","D9","AV_D9","D10","AV_D10","D11","AV_D11","D12","AV_D12","D13","AV_D13"]]
        df5 = df5[["filename","timestamp","latitude_TDS","AV_latitude_TDS","longitude_TDS","AV_longitude_TDS","depth_TDS","latitude_SHIP","longitude_SHIP","sounder_SHIP","COG_SHIP","SOG_SHIP","Roll_TDV","Pitch_TDV","Yaw_TDV","depth_USBL","AV_depth_USBL","SlantRange","AV_SlantRange","z","AV_z","Z","AV_Z","X","AV_X","BRG","AV_BRG"]]
        df5.to_excel(fn_path, index=False)