# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 13:40:36 2019

@author: Lea
"""
import csv

with open('eggs.csv', newline='') as csvfile:
     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
     for row in spamreader:
         print(', '.join(row))