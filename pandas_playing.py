# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 16:29:20 2015

@author: Jamie
"""

import pandas as pd
import numpy as np
import matplotlib as mpl

path = "C:\\Programming\\IPSA\\"

constituencies = pd.read_csv(path+"constituency.csv"
                             ,index_col = 2)

expenses = pd.read_csv(path+"combined.csv"
                     , skipinitialspace=True
                     , parse_dates = [2])

del (expenses['short_description'],expenses['details'],expenses['journey_type']
     ,expenses['from'],expenses['to'])

expenses = expenses[expenses.year != '15_16']

summary = expenses.pivot_table(index=['mp_name','mp_constituency','year','category'] 
                               ,values='amount_paid'
                               ,aggfunc=np.sum)

summary.to_csv(path+"output.csv" 
              , cols=['mp_name','constituency','year','vategory','amount_paid'])


#What are the total expenses for each MP in each Category?
mp_category = expenses.pivot_table(index="mp_name", 
                                    columns="category", 
                                    values="amount_paid", 
                                    aggfunc=np.sum)
                                    
                                    
year_category = expenses.pivot_table(index="category", 
                                     columns="year", 
                                     values="amount_paid", 
                                     aggfunc=np.sum)

mp_category_year = expenses.pivot_table(index=["mp_name","category"], 
                                     columns="year", 
                                     values="amount_paid", 
                                     aggfunc=np.sum)



#Data needed for:
# 1) Margin of Error (25%)
# 2) Mean by region
# 3) Quartlies by distance to London
# 4) P