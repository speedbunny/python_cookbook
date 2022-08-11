#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 15:33:57 2022

@author: saraheaglesfield
"""
import pandas as pd 
import os
import glob 

os.chdir('/Your/Working/Directory/')

def read_json_folder(json_folder: str):
    transactions_files = glob.glob("{}*/*.json".format(json_folder))

    return pd.concat(pd.read_json(tf, lines=True) for tf in transactions_files)

#Define Locations
customers_csv = "customers.csv"
transactions_json = "/transactions_folder/"
products_csv = "products.csv"

#Create DFs
customers_df = pd.read_csv(customers_csv)
products_df = pd.read_csv(products_csv)
transactions_df = read_json_folder(transactions_json)


#Flatten Basket
exploded_df = transactions_df.explode('basket')
df_out = pd.DataFrame([i for i in exploded_df['basket'].to_numpy()], index=exploded_df['basket']).reset_index()
temp = exploded_df.join(df_out, lsuffix='_orig', rsuffix='_other')
flat = temp.drop(['basket_other', 'basket_orig','price'], axis=1)

#Count Items
counted = flat.groupby(['customer_id', 'product_id'], as_index=False).count()
counted.rename(columns={'date_of_purchase': 'purchase_count'}, inplace=True)

#Look up Customer and Prodcut Info
counted = counted.merge(customers_df, on='customer_id', how='left')
counted = counted.merge(products_df, on='product_id', how='left')

#Produce Final Table
final = counted.drop(['product_description'], axis=1)
