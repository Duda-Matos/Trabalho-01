# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 15:50:14 2025

@author: dudad
"""

#%%
import os
import pandas as pd
import numpy as np
#%%

dataDir = "C:/Users/dudad/Documents/GitHub/ENS5132/Trabalho/inputs/rios"

dataList = os.listdir(dataDir)

os.chdir(dataDir)

for fileInList in dataList:
    #print (fileInList)
    dfConc = pd.read_csv(fileInList,encoding ='latin1')
    allFiles.append(dfConc)
    
allFiles = pd.concat(allFiles)


