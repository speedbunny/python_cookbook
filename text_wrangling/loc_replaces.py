#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 12:17:18 2021
Text wrangling LOC REPLACES
@author: Sarah E
"""
import pandas as pd
#Create Dataframe
data = [['granny apple', 'juicy'], ['blood orange', 'refreshing'], ['spanish lemon', 'tangy']]
df = pd.DataFrame(data, columns = ['fruit', 'taste'])
#Shortcut for name
fruit='fruit'
#Single Replace
df.loc[df[fruit].str.contains('apple', case=False)==True, fruit] = "red granny apple"

#Double Replace
df.loc[[df[fruit].str.contains('apple', case=False)==True] and df[fruit].str.contains('granny', case=False)==True,fruit] = "big red granny apple"
