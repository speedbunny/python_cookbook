#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 22:07:04 2022
Splits a large text or XML file into smaller files using a delimiter.
@author: saraheaglesfield
"""

def files():
    n = 0
    while True:
        n += 1
        yield open('vr%d.xml' % n, 'w')

input_file = "large_text_file.xml" #Any type of txt file
split_pattern = "Pattern to find. This will be the first line of the file that is created"

pattern = split_pattern
fs = files()
outfile = next(fs) 

with open(input_file) as infile:
    for line in infile:
        if pattern not in line:
            outfile.write(line)
        else:
            items = line.split(pat)
            outfile.write(items[0])
            for item in items[1:]:
                outfile = next(fs)
                outfile.write(pattern + item) #remove pattern to exclude the split_pattern
