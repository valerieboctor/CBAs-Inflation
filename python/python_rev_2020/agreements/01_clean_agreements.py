from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os


agreements_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/RAIS/'
os.chdir(agreements_path)


# Define a function to merge the agreements data for each year
# def CBA_merge(year): # year should be in format 'XXXX'
#	cont = pd.read_stata(year+'_contracts_CBAfirms.dta')
#	firm = pd.read_stata(year+'_firmlevel_paneldecember_CBAfirms.dta')
#	df = cont.merge(firm, on = 'identificad')
#	return df 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~ Warning: this code is super slow ~~~~~~~~~~~~~~~~~
# ~~~~~~~~ Better to merge data one year at a time ~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Initialize a list of empty dataframes to hold the merged DataFrames
# for each year
# CBA_df = [pd.DataFrame()]*len(years)

# Get the years of the data in string format


	# df = CBA_merge(years[i])
	# CBA_df[i] = df
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# This loop appends years of the firm_level CBA data 
start = 2013
end = 2018
years = list(np.arange(start, end))
for i in range(len(years)):
	years[i] = str(years[i])

for i in range(len(years) - 1):
	if i == 0:
		df_old = pd.read_stata(years[i]+'_firmlevel_paneldecember_CBAfirms.dta')
		data_year = [years[i]]*len(df_old)
		df_old['year'] = data_year
	df_new  = pd.read_stata(years[i+1]+'_firmlevel_paneldecember_CBAfirms.dta')
	data_year = [years[i+1]]*len(df_new)
	df_new['year'] = data_year 
	df_new = pd.concat([df_old, df_new], axis = 0)
	df_old = df_new

df = df_new
df.to_csv(agreements_path + '2013_2017_firmlevel_paneldecember.csv')
