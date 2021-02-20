from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

# Specify directories
firms_raw_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/raw/compustat/'
firms_clean_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/compustat/'
os.chdir(firms_raw_path)	

df = pd.read_csv('compustat10_20.csv')
df = df[['gvkey', 'conm','isin', 'datacqtr','datafqtr', 'datadate', 'actq', 'atq', 'gpq', 'invtq', 'teqq', 'xstq']]

# gvkey	= unique firm ID
# conm 	= company name
# actq 	= current assets -- quarterly total
# atq 	= assets -- quarterly total
# invtq = inventories -- quarterly total
# xstq	= staff expenses -- quarterly wages/ salaries
# gpq 	= quarterly gross profits (loss)
# teqq 	= shareholders equity -- quarterly total

date_vars = ['datacqtr', 'datafqtr','datadate']
for i in range(len(date_vars)):
	df[date_vars[i]] = pd.to_datetime(df.datacqtr)

# Check fiscal year and calendar year is the same for all observations:
for i in range(len(df)):
	if df.datacqtr[i] != df.datafqtr[i]:
		print('Check dates for row %d' %(i)) 

os.chdir(firms_clean_path)
df.to_csv(firms_clean_path+'compustat10_20.csv')

comp = pd.read_csv(firms_clean_path+'compustat10_20.csv', index_col= 0)
comp = comp.set_index('datacqtr')

bridge = pd.read_stata(firms_clean_path+'compustat_bridge10_20.dta')
bridge = bridge[['conm', 'CNPJ']]
test = comp.merge(bridge, on = 'conm')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The code below checks whether the CNPJs are the same for every entry of a particular firm. Note that the CNPJs are matched on firm name, but 
# it might be the case that the within-firm CNPJs should vary by branch, so check on this later.
for i in range(len(test)-1):
	if test.conm[i] == test.conm[i+1] and test.CNPJ[i] == test.CNPJ[i+1]:
		print(str(test.conm[i]+': row '+str(i)))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

