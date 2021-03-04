from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

agreements_path = '/Users/Valerie/Dropbox/Research/CBA monetary policy and firms/data/clean'
os.chdir(agreements_path)
cba_df = pd.read_stata('panel_firmsCBA_jan2021.dta')
# want to make a graph that shows the difference in nominal wage growth among firms that had CBAs before Feb 2016 and those that had CBAs just after

cba_df['monthly_date'] = monthly_date
month = cba_df.month.astype(int)
year = cba_df.year.astype(int)
monthly_date = 100*year + month
cba_df['monthly_date'] = monthly_date

#check number of non NaN observations:
# np.sum(cba_df.COLUMN_NAME.count())

# make a dummy variable that equals the sum of the month of contract and the contract duration is >= 12
N = cba_df.identificad.count() #this is the number of rows in the data set, including rows with NaN values
duration = cba_df.duration.astype(float) 


# graph_df = cba_df[cba_df.year == "2016"]
# graph_df = graph_df[['identificad', 'month', 'year', 'rem','duration', 'cba_month']]

cba_date = np.array(cba_df.monthly_date * cba_df.cba_month).astype(float) #zero if no CBA that month
cba_jan16 = (cba_date == 201601).astype(int)
cba_march16 = (cba_date == 201603).astype(int)

graph_df = cba_df[cba_df.monthly_date.between(201506, 201606, inclusive=True)]
cba_date = np.array(graph_df.monthly_date * graph_df.cba_month).astype(float) #zero if no CBA that month
cba_jan16 = (cba_date == 201601).astype(int)
cba_mar16 = (cba_date == 201603).astype(int)
graph_df['cba_jan16'] = cba_jan16
graph_df['cba_mar16'] = cba_mar16

# want to plot demeaned wages from 201506 - 201606 for firms that had cbas in march vs those that had cbas in jan
	