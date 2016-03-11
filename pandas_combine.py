# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:29:20 2015

@author: Jamie
"""

import pandas as pd
import numpy as np
import matplotlib as mpl

path = "C:\\Programming\\IPSA\\combine\\DataDownload_20"

expenses = pd.DataFrame()

for i in range(10,16):
    expenses = expenses.append(
                        pd.read_csv(path+str(i)+".csv"))
    print("20"+str(i)+" completed")
    print(len(expenses))
                        
    
expenses.to_csv("C:\\Programming\\IPSA\\combine\\combined.csv"
               ,encoding="UTF-8")
    
print("completed")