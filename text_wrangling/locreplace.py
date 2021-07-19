#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 12:17:18 2021
Text wrangling LOC REPLACES
@author: Sarah E
"""
import pandas as pd
#Locreplace Function
import pandas as pd

def locreplace(df,col,needle,replace,needle2=''):
   if (needle2==''):
      df.loc[df[col].str.contains(needle, case=False)==True,col] = replace
   else:
     df.loc[df[col].str.contains(needle, case=False) & df[col].str.contains(needle2, case=False), col] = replace


#In Action
data = [['granny apple', 'juicy'], ['granny blood orange', 'refreshing'], ['spanish lemon', 'tangy']]
fruitdf = pd.DataFrame(data, columns = ['fruit', 'taste'])

locreplace(fruitdf,'fruit','apple','big red apple','granny')

#Single replace
#locreplace(fruitdf,'fruit','apple','big red nice apple')

#Will fail
#locreplace(fruitdf,'fruit','apple','big red apple','uncle')
