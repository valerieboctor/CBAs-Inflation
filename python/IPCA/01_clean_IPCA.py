from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

ipca_raw_path = '/Users/Valerie/Dropbox/Research/CBA monetary policy and firms/data/raw/IPCA/'
ipca_clean_path = '/Users/Valerie/Dropbox/Research/CBA monetary policy and firms/data/clean/IPCA/'
os.chdir(ipca_raw_path)

# for root, dirs, files in os.walk("."):
#     for filename in files:
#         print(filename)

# Clean inflation expectations of financial firms (IPCA)
raw_files = ['Average05_06.csv', 'Average07_08.csv', \
'Average09_10.csv','Average11_12.csv', 'Average13_14.csv', \
'Average15_16.csv', 'Average17_18.csv', \
'Average19.csv']

def clean_IPCA(filename):
	df_new = pd.read_csv(filename, sep = '[;| ]',engine='python', \
	skiprows = 1)
	df_new = df_new.dropna(axis = 1)
	df_new = df_new.rename(columns={"Unnamed: 1": "Avg"})
	df_new = df_new.set_index('Date')
	df_new.index = pd.to_datetime(df_new.index)	
	df_new.to_csv(ipca_clean_path+'IPCA_Clean_'+str(filename))

for i in range(0, len(raw_files)):
	clean_IPCA(raw_files[i])
	if i == len(raw_files)-1:
		print('All clean!')

dfs = [pd.DataFrame()]*len(raw_files)
for i in range(0, len(dfs)):
	dfs[i] = pd.read_csv(ipca_clean_path+'IPCA_Clean_'+raw_files[i])
	if i > 0:
		dfs[i] = dfs[i].append(dfs[i-1])
		if i == len(raw_files) - 1:
			dfs[i] = dfs[i].sort_values(by='Date')
			dfs[i].to_csv(ipca_clean_path+'IPCA_Clean_Average05_19.csv')

# Lightly Clean the actual inflation data, downloaded from FRED (series ID: FPCPITOTLZGBRA)
actual_inflation = pd.read_csv('Actual_Inflation05_19.csv', names = ['Date', 'Inflation'], header = 0)
actual_inflation['Date'] = pd.to_datetime(actual_inflation.Date)
actual_inflation = actual_inflation.set_index('Date', drop=True)
actual_inflation.to_csv(ipca_clean_path+'Actual_Inflation05_19.csv')