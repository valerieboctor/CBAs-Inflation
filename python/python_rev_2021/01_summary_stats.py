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

graph_df = cba_df[cba_df.monthly_date.between(201501, 201712, inclusive=True)]
cba_date = np.array(graph_df.monthly_date * graph_df.cba_month).astype(float) #zero if no CBA that month
cba_jan16 = (cba_date == 201601).astype(int)
cba_mar16 = (cba_date == 201603).astype(int)
graph_df['cba_jan16'] = cba_jan16
graph_df['cba_mar16'] = cba_mar16

# make dummy variables at the firm level which tell if firms had cbas in Jan 2016, Mar 2016.
#=======================================================================================================================
# Jan16 CBA dummy: 
cba_jan16_y_n = graph_df.cba_jan16.groupby(graph_df.identificad).max()
cba_jan16_y_n = cba_jan16_y_n.reset_index()

# Mar16 CBA dummy:
cba_mar16_y_n =graph_df.cba_mar16.groupby(graph_df.identificad).max()
cba_mar16_y_n = cba_mar16_y_n.reset_index()

graph_df = cba_mar16_y_n.merge(graph_df, on = 'identificad',how = 'outer')
graph_df = cba_jan16_y_n.merge(graph_df, on = 'identificad',how = 'outer')
graph_df= graph_df.rename(columns={"cba_mar16_x": "cba_mar16_y_n", "cba_mar16_y": "cba_mar16","cba_jan16_x": 
	"cba_jan16_y_n", "cba_jan16_y": "cba_jan16"})
graph_df = graph_df.sort_values(['cba_jan16_y_n', 'identificad', 'monthly_date'])
# pd.options.display.max_columns = 6
# pd.options.display.max_rows = 6
graph_df['rem_cba_mar16'] = graph_df.rem[graph_df.cba_mar16_y_n==1]
graph_df['rem_cba_jan16'] = graph_df.rem[graph_df.cba_jan16_y_n==1]

#=======================================================================================================================
# Make average wage series for firms that had CBAs in Mar16, Jan16, and average of all firms.
rem_cba_jan16_avg = graph_df[['monthly_date', 'rem_cba_jan16']].groupby('monthly_date').mean()
rem_cba_jan16_avg = rem_cba_jan16_avg.reset_index()
rem_cba_jan16_avg = rem_cba_jan16_avg.rename(columns={"rem_cba_jan16": "rem_cba_jan16_avg"})
rem_cba_jan16_avg.monthly_date = pd.to_datetime(rem_cba_jan16_avg.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_jan16_med = graph_df[['monthly_date', 'rem_cba_jan16']].groupby('monthly_date').median()
rem_cba_jan16_med = rem_cba_jan16_med.reset_index()
rem_cba_jan16_med = rem_cba_jan16_med.rename(columns={"rem_cba_jan16": "rem_cba_jan16_med"})
rem_cba_jan16_med.monthly_date = pd.to_datetime(rem_cba_jan16_med.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_mar16_avg = graph_df[['monthly_date', 'rem_cba_mar16']].groupby('monthly_date').mean()
rem_cba_mar16_avg = rem_cba_mar16_avg.reset_index()
rem_cba_mar16_avg = rem_cba_mar16_avg.rename(columns={"rem_cba_mar16": "rem_cba_mar16_avg"})
rem_cba_mar16_avg.monthly_date = pd.to_datetime(rem_cba_mar16_avg.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_mar16_med = graph_df[['monthly_date', 'rem_cba_mar16']].groupby('monthly_date').median()
rem_cba_mar16_med = rem_cba_mar16_med.reset_index()
rem_cba_mar16_med = rem_cba_mar16_med.rename(columns={"rem_cba_mar16": "rem_cba_mar16_med"})
rem_cba_mar16_med.monthly_date = pd.to_datetime(rem_cba_mar16_med.monthly_date, yearfirst='True', format = '%Y%m')

fig1 = plt.figure(figsize = (7,5))
plt.plot(rem_cba_mar16_avg.monthly_date, rem_cba_mar16_avg.rem_cba_mar16_avg, label = "Average Remuneration -- CBAs in Mar 2016")
plt.plot(rem_cba_jan16_df.monthly_date, rem_cba_jan16_avg.rem_cba_jan16_avg, label = "Average Remuneration -- CBAs in Jan 2016")  
plt.plot(rem_cba_mar16_med.monthly_date, rem_cba_mar16_med.rem_cba_mar16_med, label = "Median Remuneration -- CBAs in Mar 2016")
plt.plot(rem_cba_jan16_df.monthly_date, rem_cba_jan16_med.rem_cba_jan16_med, label = "Median Remuneration -- CBAs in Jan 2016")  
plt.legend()

plt.savefig('avg_med_rem_2015_2017.png')
plt.close()


# want to plot demeaned wages from 201506 - 201606 for firms that had cbas in march vs those that had cbas in jan
	