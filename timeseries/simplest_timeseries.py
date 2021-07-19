#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 05:23:09 2021
Simplest Time Series Plot using Pandas
@author: Sarah E
"""
import pandas as pd
import matplotlib.pyplot as plt

complaints = pd.read_excel ('../complaints.xlsx',
                     usecols = [1,3,9],
                     index_col=None,
                     sheet_name = 'Sheet 1')

complaints_ts=complaints.groupby(['Response Date']).size()
plot_date_format = DateFormatter("%d/%m")
complaints_ts.plot().xaxis.set_major_formatter(plot_date_format)
complaints_ts.plot().set(xlabel="Date",
       ylabel="Complaints",
       title="Daily Complaints\n Month Year ")
plt.savefig('complaints_ts.png', bbox_inches='tight')
plt.show()
