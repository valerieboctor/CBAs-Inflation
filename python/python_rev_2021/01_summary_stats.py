from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os
import datetime

agreements_path = '/Users/Valerie/Dropbox/Research/CBA monetary policy and firms/data/clean'
os.chdir(agreements_path)
graph_df = pd.read_stata('panel_firmsCBA_jan2021.dta')
# want to make a graph that shows the difference in nominal wage growth among firms that had CBAs before Feb 2016 and those that had CBAs just after

month = graph_df.month.astype(int)
year = graph_df.year.astype(int)
monthly_date = 100*year + month
graph_df['monthly_date'] = monthly_date

date_vars = ['monthly_date']
for i in date_vars:
	graph_df[i] = pd.to_datetime(graph_df[i], yearfirst='True', format = '%Y%m')
#check number of non NaN observations:
# np.sum(cba_df.COLUMN_NAME.count())

# make a dummy variable that equals the sum of the month of contract and the contract duration is >= 12
graph_df = graph_df[['identificad', 'monthly_date', 'rem', 'real_earnings','duration', 'cba_month', 'num_workers', 'clascnae20']]
graph_df = graph_df.set_index('monthly_date')
graph_df = graph_df.loc['2015-01':'2017-12']
graph_df = graph_df.reset_index()
balanced_ids = graph_df.groupby('identificad')['monthly_date'].nunique()
balanced_ids = balanced_ids.reset_index()
balanced_ids = balanced_ids.rename(columns = {'monthly_date':'num_months'})
graph_df = balanced_ids.merge(graph_df, on = 'identificad', how = 'inner')
graph_df = graph_df.set_index('monthly_date')

graph_df = graph_df[graph_df.num_months == 36] # balanced panel!
# graph_df = graph_df[graph_df.duration >= 12]

graph_df = graph_df.reset_index()
graph_df['cba_time'] = graph_df.monthly_date[graph_df.cba_month ==1]
cba_jan16 = (graph_df.cba_time == '2016-01').astype('int')
cba_may16 = (graph_df.cba_time== '2016-05').astype('int')

N = graph_df.identificad.count() #this is the number of rows in the data set before merging, including rows with NaN values
graph_df['cba_jan16'] = cba_jan16
graph_df['cba_may16'] = cba_may16


# make dummy variables at the firm level which tell if firms had cbas in Jan 2016, may 2016.
#==================================================================================================
# Jan16 CBA dummy: 
cba_jan16_y_n = graph_df.cba_jan16.groupby(graph_df.identificad).max()
cba_jan16_y_n = cba_jan16_y_n.reset_index()

# may16 CBA dummy
cba_may16_y_n =graph_df.cba_may16.groupby(graph_df.identificad).max()
cba_may16_y_n = cba_may16_y_n.reset_index()

graph_df = cba_may16_y_n.merge(graph_df, on = 'identificad',how = 'inner')
graph_df = cba_jan16_y_n.merge(graph_df, on = 'identificad',how = 'inner')
graph_df= graph_df.rename(columns={"cba_may16_x": "cba_may16_y_n", "cba_may16_y": "cba_may16","cba_jan16_x":"cba_jan16_y_n", "cba_jan16_y": "cba_jan16"})

graph_df = graph_df[graph_df.cba_may16_y_n != graph_df.cba_jan16_y_n]

# graph_df.groupby('identificad')['monthly_date'].nunique()
# graph_df = graph_df.sort_values(['cba_jan16_y_n', 'identificad', 'monthly_date'])
# pd.options.display.max_columns = 6
# pd.options.display.max_rows = 6
graph_df['rem_cba_may16'] = graph_df.rem[graph_df.cba_may16_y_n == 1]
graph_df['rem_cba_jan16'] = graph_df.rem[graph_df.cba_jan16_y_n==1]
graph_df['real_rem_cba_may16']= graph_df.real_earnings[graph_df.cba_may16_y_n == 1]
graph_df['real_rem_cba_jan16']= graph_df.real_earnings[graph_df.cba_jan16_y_n == 1]
graph_df['emp_cba_may16'] = graph_df.num_workers[graph_df.cba_may16_y_n == 1]
graph_df['emp_cba_jan16'] = graph_df.num_workers[graph_df.cba_jan16_y_n == 1]
#==================================================================================================
# Average/Median Wage/Employment series
#Make average and median number of workers series for firms that had CBAs in May16, Jan16, and median of all firms
#==================================================================================================
#									NUMBER OF WORKERS SERIES
#==================================================================================================
emp_cba_jan16_avg = graph_df[['monthly_date', 'emp_cba_jan16']].groupby('monthly_date').mean()
emp_cba_jan16_avg = emp_cba_jan16_avg.reset_index()
emp_cba_jan16_avg = emp_cba_jan16_avg.rename(columns={"emp_cba_jan16": "emp_cba_jan16_avg"})
emp_cba_jan16_avg.monthly_date = pd.to_datetime(emp_cba_jan16_avg.monthly_date, yearfirst='True', format = '%Y%m')

emp_cba_jan16_med = graph_df[['monthly_date', 'emp_cba_jan16']].groupby('monthly_date').median()
emp_cba_jan16_med = emp_cba_jan16_med.reset_index()
emp_cba_jan16_med = emp_cba_jan16_med.rename(columns={"emp_cba_jan16": "emp_cba_jan16_med"})
emp_cba_jan16_med.monthly_date = pd.to_datetime(emp_cba_jan16_med.monthly_date, yearfirst='True', format = '%Y%m')

emp_cba_may16_avg = graph_df[['monthly_date', 'emp_cba_may16']].groupby('monthly_date').mean()
emp_cba_may16_avg = emp_cba_may16_avg.reset_index()
emp_cba_may16_avg = emp_cba_may16_avg.rename(columns={"emp_cba_may16": "emp_cba_may16_avg"})
emp_cba_may16_avg.monthly_date = pd.to_datetime(emp_cba_may16_avg.monthly_date, yearfirst='True', format = '%Y%m')

emp_cba_may16_med = graph_df[['monthly_date', 'emp_cba_may16']].groupby('monthly_date').median()
emp_cba_may16_med = emp_cba_may16_med.reset_index()
emp_cba_may16_med = emp_cba_may16_med.rename(columns={"emp_cba_may16": "emp_cba_may16_med"})
emp_cba_may16_med.monthly_date = pd.to_datetime(emp_cba_may16_med.monthly_date, yearfirst='True', format = '%Y%m')

med_emp = graph_df[['monthly_date', 'num_workers']].groupby('monthly_date').median()
med_emp = med_emp.reset_index()
med_emp.monthly_date = pd.to_datetime(med_emp.monthly_date, yearfirst='True', format = '%Y%m')
# Make average and median wage series for firms that had CBAs in may16, Jan16, and average of all firms.
#==================================================================================================
#								NOMINAL MONTHLY REMUNERATION SERIES
#==================================================================================================
rem_cba_jan16_avg = graph_df[['monthly_date', 'rem_cba_jan16']].groupby('monthly_date').mean()
rem_cba_jan16_avg = rem_cba_jan16_avg.reset_index()
rem_cba_jan16_avg = rem_cba_jan16_avg.rename(columns={"rem_cba_jan16": "rem_cba_jan16_avg"})
rem_cba_jan16_avg.monthly_date = pd.to_datetime(rem_cba_jan16_avg.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_jan16_med = graph_df[['monthly_date', 'rem_cba_jan16']].groupby('monthly_date').median()
rem_cba_jan16_med = rem_cba_jan16_med.reset_index()
rem_cba_jan16_med = rem_cba_jan16_med.rename(columns={"rem_cba_jan16": "rem_cba_jan16_med"})
rem_cba_jan16_med.monthly_date = pd.to_datetime(rem_cba_jan16_med.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_may16_avg = graph_df[['monthly_date', 'rem_cba_may16']].groupby('monthly_date').mean()
rem_cba_may16_avg = rem_cba_may16_avg.reset_index()
rem_cba_may16_avg = rem_cba_may16_avg.rename(columns={"rem_cba_may16": "rem_cba_may16_avg"})
rem_cba_may16_avg.monthly_date = pd.to_datetime(rem_cba_may16_avg.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_may16_med = graph_df[['monthly_date', 'rem_cba_may16']].groupby('monthly_date').median()
rem_cba_may16_med = rem_cba_may16_med.reset_index()
rem_cba_may16_med = rem_cba_may16_med.rename(columns={"rem_cba_may16": "rem_cba_may16_med"})
rem_cba_may16_med.monthly_date = pd.to_datetime(rem_cba_may16_med.monthly_date, yearfirst='True', format = '%Y%m')

med_rem = graph_df[['monthly_date', 'rem']].groupby('monthly_date').median()
med_rem = med_rem.reset_index()
med_rem.monthly_date = pd.to_datetime(med_rem.monthly_date, yearfirst='True', format = '%Y%m')

#==================================================================================================
#									REAL MONTHLY REMUNERATION SERIES
#==================================================================================================
real_rem_cba_jan16_avg = graph_df[['monthly_date', 'real_rem_cba_jan16']].groupby('monthly_date').mean()
real_rem_cba_jan16_avg = real_rem_cba_jan16_avg.reset_index()
real_rem_cba_jan16_avg = real_rem_cba_jan16_avg.rename(columns={"real_rem_cba_jan16": "real_rem_cba_jan16_avg"})
real_rem_cba_jan16_avg.monthly_date = pd.to_datetime(real_rem_cba_jan16_avg.monthly_date, yearfirst='True', format = '%Y%m')

real_rem_cba_jan16_med = graph_df[['monthly_date', 'real_rem_cba_jan16']].groupby('monthly_date').median()
real_rem_cba_jan16_med = real_rem_cba_jan16_med.reset_index()
real_rem_cba_jan16_med = real_rem_cba_jan16_med.rename(columns={"real_rem_cba_jan16": "real_rem_cba_jan16_med"})
real_rem_cba_jan16_med.monthly_date = pd.to_datetime(real_rem_cba_jan16_med.monthly_date, yearfirst='True', format = '%Y%m')

real_rem_cba_may16_avg = graph_df[['monthly_date', 'real_rem_cba_may16']].groupby('monthly_date').mean()
real_rem_cba_may16_avg = real_rem_cba_may16_avg.reset_index()
real_rem_cba_may16_avg = real_rem_cba_may16_avg.rename(columns={"real_rem_cba_may16": "real_rem_cba_may16_avg"})
real_rem_cba_may16_avg.monthly_date = pd.to_datetime(real_rem_cba_may16_avg.monthly_date, yearfirst='True', format = '%Y%m')

real_rem_cba_may16_med = graph_df[['monthly_date', 'real_rem_cba_may16']].groupby('monthly_date').median()
real_rem_cba_may16_med = real_rem_cba_may16_med.reset_index()
real_rem_cba_may16_med = real_rem_cba_may16_med.rename(columns={"real_rem_cba_may16": "real_rem_cba_may16_med"})
real_rem_cba_may16_med.monthly_date = pd.to_datetime(real_rem_cba_may16_med.monthly_date, yearfirst='True', format = '%Y%m')

real_med_rem = graph_df[['monthly_date', 'real_earnings']].groupby('monthly_date').median()
real_med_rem = real_med_rem.reset_index()
real_med_rem.monthly_date = pd.to_datetime(real_med_rem.monthly_date, yearfirst='True', format = '%Y%m')
#==================================================================================================

# Graph Average and Median Wages for Groups of Firms (All, CBA May16, CBA Jan16)
#==================================================================================================
#									NUMBER OF WORKERS GRAPH
#==================================================================================================
fig0 = plt.figure(figsize = (10,7))
plt.plot(emp_cba_may16_avg.monthly_date, emp_cba_may16_avg.emp_cba_may16_avg, label = "Average -- CBAs in May 2016")
plt.plot(emp_cba_jan16_avg.monthly_date, emp_cba_jan16_avg.emp_cba_jan16_avg, label = "Average -- CBAs in Jan 2016")  
plt.title("Workers per Firm (Monthly) 2015-2017")
plt.axvline(x = '2016-03', color = 'black', linestyle='-')
plt.legend()
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/avg_emp_2015_2017.png')
plt.plot(emp_cba_may16_med.monthly_date, emp_cba_may16_med.emp_cba_may16_med, label = "Median -- CBAs in May 2016")
plt.plot(emp_cba_jan16_med.monthly_date, emp_cba_jan16_med.emp_cba_jan16_med, label = "Median -- CBAs in Jan 2016")  
plt.plot(med_emp.monthly_date, med_emp.num_workers, label = "Median -- All Firms in Sample" )
plt.legend()
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/avg_med_emp_2015_2017')
plt.clf()
plt.close()

#==================================================================================================
#									NOMINAL REMUNERATION GRAPH
#==================================================================================================
fig1 = plt.figure(figsize = (10,7))
plt.plot(rem_cba_may16_avg.monthly_date, rem_cba_may16_avg.rem_cba_may16_avg, label = "Average -- CBAs in May 2016")
plt.plot(rem_cba_jan16_avg.monthly_date, rem_cba_jan16_avg.rem_cba_jan16_avg, label = "Average -- CBAs in Jan 2016")  
plt.title("Monthly Nominal Remuneration 2015-2017")
plt.legend()
plt.axvline(x = '2016-03', color = 'black', linestyle='-')
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/avg_rem_2015_2017.png')
plt.plot(rem_cba_may16_med.monthly_date, rem_cba_may16_med.rem_cba_may16_med, label = "Median -- CBAs in May 2016")
plt.plot(rem_cba_jan16_med.monthly_date, rem_cba_jan16_med.rem_cba_jan16_med, label = "Median -- CBAs in Jan 2016")  
plt.plot(med_rem.monthly_date, med_rem.rem, label = "Median -- All Firms in Sample" )
plt.legend()
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/avg_med_rem_2015_2017.png')
plt.clf()
plt.close()
# rem_cba_jan16_avg['rem_cba_jan16_growth'] = rem_cba_jan16_avg.rem_cba_jan16_avg.pct_change()
# rem_cba_may16_avg['rem_cba_may16_growth'] = rem_cba_may16_avg.rem_cba_may16_avg.pct_change()

#==================================================================================================
#									REAL REMUNERATION GRAPH
#==================================================================================================
fig1 = plt.figure(figsize = (10,7))
plt.plot(real_rem_cba_may16_avg.monthly_date, real_rem_cba_may16_avg.real_rem_cba_may16_avg, label = "Average -- CBAs in May 2016")
plt.plot(real_rem_cba_jan16_avg.monthly_date, real_rem_cba_jan16_avg.real_rem_cba_jan16_avg, label = "Average -- CBAs in Jan 2016")  
plt.title("Monthly Real Remuneration 2015-2017")
plt.legend()
plt.axvline(x = '2016-03', color = 'black', linestyle='-')
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/real_avg_rem_2015_2017.png')
plt.plot(real_rem_cba_may16_med.monthly_date, real_rem_cba_may16_med.real_rem_cba_may16_med, label = "Median -- CBAs in May 2016")
plt.plot(real_rem_cba_jan16_med.monthly_date, real_rem_cba_jan16_med.real_rem_cba_jan16_med, label = "Median -- CBAs in Jan 2016")  
plt.plot(real_med_rem.monthly_date, real_med_rem.real_earnings, label = "Median -- All Firms in Sample" )
plt.legend()
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/real_avg_med_rem_2015_2017.png')
plt.clf()
plt.close()

# plot normalized version of the graph above
# first generate the normalized series
#==================================================================================================
#								NORMALIZED NOMINAL REMUNERATION GRAPH
#==================================================================================================
plot_dfs = [rem_cba_may16_avg, rem_cba_jan16_avg, rem_cba_may16_med, rem_cba_jan16_med, med_rem]
plot_series = ["rem_cba_may16_avg", "rem_cba_jan16_avg", "rem_cba_may16_med", "rem_cba_jan16_med", "rem"]
labels = ["Average -- CBAs in May 2016", "Average -- CBAs in Jan 2016", "Median -- CBAs in May 2016", "Median -- CBAS in Jan 2016", "Median -- All Firms"]
preshock_date = "2015-12-01"

fig2 = plt.figure(figsize = (10,7))
for i in range(0, len(plot_dfs)):
	norm_factor = np.array(plot_dfs[i][plot_series[i]][plot_dfs[i].monthly_date == preshock_date])
	plot_dfs[i]['norm_'+plot_series[i]] = plot_dfs[i][plot_series[i]] / norm_factor
	if i <2:
		plt.plot(plot_dfs[i]['monthly_date'], plot_dfs[i]['norm_'+plot_series[i]], label = labels[i])
		plt.legend()
		plt.axvline(x = '2016-03', color = 'black', linestyle='-')
		plt.title("Normalized Nominal Monthly Remuneration 2015-2017")
		plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/normalized_avg_rem_2015_2017.png')
	if i >=2:
		plt.plot(plot_dfs[i]['monthly_date'], plot_dfs[i]['norm_'+plot_series[i]], label = labels[i])
		plt.legend()
		plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/normalized_avg_med_rem_2015_2017.png')
plt.clf()
plt.close()
#==================================================================================================
#								NORMALIZED REAL REMUNERATION GRAPH
#==================================================================================================
plot_dfs = [real_rem_cba_may16_avg, real_rem_cba_jan16_avg, real_rem_cba_may16_med, real_rem_cba_jan16_med, real_med_rem]
plot_series = ["real_rem_cba_may16_avg", "real_rem_cba_jan16_avg", "real_rem_cba_may16_med", "real_rem_cba_jan16_med", "real_earnings"]
labels = ["Average -- CBAs in May 2016", "Average -- CBAs in Jan 2016", "Median -- CBAs in May 2016", "Median -- CBAS in Jan 2016", "Median -- All Firms"]
preshock_date = "2015-12-01"

fig3 = plt.figure(figsize = (10,7))
for i in range(0, len(plot_dfs)):
	norm_factor = np.array(plot_dfs[i][plot_series[i]][plot_dfs[i].monthly_date == preshock_date])
	plot_dfs[i]['norm_'+plot_series[i]] = plot_dfs[i][plot_series[i]] / norm_factor
	if i <2:
		plt.plot(plot_dfs[i]['monthly_date'], plot_dfs[i]['norm_'+plot_series[i]], label = labels[i])
		plt.legend()
		plt.axvline(x = '2016-03', color = 'black', linestyle='-')
		plt.title("Normalized Real Monthly Remuneration 2015-2017")
		plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/normalized_real_avg_rem_2015_2017.png')
	if i >=2:
		plt.plot(plot_dfs[i]['monthly_date'], plot_dfs[i]['norm_'+plot_series[i]], label = labels[i])
		plt.legend()
		plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/normalized_real_avg_med_rem_2015_2017.png')
plt.clf()
plt.close()
#==================================================================================================
#								NORMALIZED NUMBER OF WORKERS GRAPH
#==================================================================================================
plot_dfs = [emp_cba_may16_avg, emp_cba_jan16_avg, emp_cba_may16_med, emp_cba_jan16_med, med_emp]
plot_series = ["emp_cba_may16_avg", "emp_cba_jan16_avg", "emp_cba_may16_med", "emp_cba_jan16_med", "num_workers"]
labels = ["Average -- CBAs in May 2016", "Average -- CBAs in Jan 2016", "Median -- CBAs in May 2016", "Median -- CBAS in Jan 2016", "Median -- All Firms"]
preshock_date = "2015-12-01"

fig4 = plt.figure(figsize = (10,7))
for i in range(0, len(plot_dfs)):
	norm_factor = np.array(plot_dfs[i][plot_series[i]][plot_dfs[i].monthly_date == preshock_date])
	plot_dfs[i]['norm_'+plot_series[i]] = plot_dfs[i][plot_series[i]] / norm_factor	
	if i < 2:
		plt.plot(plot_dfs[i]['monthly_date'], plot_dfs[i]['norm_'+plot_series[i]], label = labels[i])
		plt.legend()
		plt.axvline(x = '2016-03', color = 'black', linestyle='-')
		plt.title("Normalized Number of Workers 2015-2017")
		plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/normalized_avg_emp_2015_2017.png')
	if i >=2:
		plt.plot(plot_dfs[i]['monthly_date'], plot_dfs[i]['norm_'+plot_series[i]], label = labels[i])
		plt.legend()
		plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/normalized_avg_med_emp_2015_2017.png')
plt.clf()
plt.close()	
#==================================================================================================
#==================================================================================================


# plot the probability of having a CBA given time since last CBA
# -------------------------------------------------------------------------------------------------
graph_df = graph_df.reset_index()
# Define Helper Function:
def fill_missing(grp):  
    res = grp.set_index('monthly_date')\
    .replace(to_replace=pd.NaT, method='ffill') #need this line to replace NaT, not zero
    del res['identificad']
    return res
# Replace zeroes in the cba_time_variable with date of previous CBA
graph_df = graph_df.set_index('monthly_date')
df = [pd.DataFrame(), pd.DataFrame()]  

main_df =[graph_df[['identificad', 'cba_time']].loc['2014-06':'2016-01'], graph_df[['identificad', 'cba_time']].loc['2016-03':'2017-12']] 
# main_df[0] #pre shock
# main_df[1] #post shock
#--------------------------------------------------------------------------------------------------
for i in range(len(df)):
	main_df[i] = main_df[i].reset_index()
	main_df[i] = main_df[i].sort_values(['identificad', 'monthly_date'])
	df[i] = main_df[i]
	df[i] = df[i].groupby(['identificad']).apply(
    lambda grp: fill_missing(grp)
	)
	df[i] = df[i].reset_index()    	
	#--------------------------------------------------------------------------------------------------------------------------
	# Merge with main dataset
	df[i]= df[i].rename(columns={"cba_time": "date_last_cba"})
	df[i] = main_df[i].merge(df[i], on = ['identificad', 'monthly_date'], how = 'inner')
#--------------------------------------------------------------------------------------------------
bar_dfs = [pd.DataFrame(), pd.DataFrame()]
bar_dfs_transformed = [pd.DataFrame(), pd.DataFrame()]

for i in range(len(bar_dfs)):
	bar_dfs[i] = df[i][df[i].date_last_cba==df[i].date_last_cba]
	bar_dfs[i].date_last_cba = pd.to_datetime(bar_dfs[i].date_last_cba, yearfirst = True, format = "%Y%m")
	bar_dfs[i]['time_since_cba'] = round((bar_dfs[i]['monthly_date'] - bar_dfs[i]['date_last_cba'])/np.timedelta64(1, 'M'))
	# make a dummy variable = 1 if the firm will have a CBA in the next period
	# take sum of 1's for every possible horizon length in time_since_cba variable
	# divide by sum of firms who have reached each of those horizon lengths
	last_period_in_spell = (bar_dfs[i].time_since_cba.shift(-1) == 0).astype(int)
	intermediate_step = (bar_dfs[i].identificad == bar_dfs[i].identificad.shift(-1)).astype(int)
	last_period_in_spell = last_period_in_spell * intermediate_step
	bar_dfs[i]['last_period_in_spell'] = last_period_in_spell
	spell_freq = bar_dfs[i].last_period_in_spell.groupby(by=[bar_dfs[i].time_since_cba]).sum() 
	number_firms = bar_dfs[i].last_period_in_spell.groupby(by=[bar_dfs[i].time_since_cba]).count() 
	hazard_rate = spell_freq/number_firms
	hazard_rate = hazard_rate.reset_index()
	hazard_rate = hazard_rate.rename(columns = {'last_period_in_spell': 'probability_of_cba_next_period'})
	hazard_rate.time_since_cba = hazard_rate.time_since_cba +1
	bar_dfs_transformed[i] = hazard_rate

graph_labels= ["Pre-Shock June 2014 - Jan 2016", "Post-Shock May 2016 - Dec 2017" ]
shift_factor = [-.25, 0 ]
fig3 = plt.figure(figsize = (10,7))
for i in range(len(bar_dfs)):
	plt.bar(bar_dfs_transformed[i].time_since_cba + shift_factor[i], bar_dfs_transformed[i].probability_of_cba_next_period, \
		width=.5, label = graph_labels[i])
	plt.xticks(np.arange(0, 20, step = 3))

plt.title("CBA Hazard Rate June 2014 - December 2017")
plt.xlabel("Months Since Last CBA")	
plt.legend()
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/cba_hazard.png')
plt.clf()
plt.close()	



#==================================================================================================
# separately plot the probability of having a CBA in each month over the entire sample
#==================================================================================================
graph_df = graph_df.reset_index()
cba_freq = graph_df.cba_month.groupby(by=[graph_df.monthly_date]).sum() 
number_firms = graph_df.cba_month.groupby(by=[graph_df.monthly_date]).count() 
cba_probability = cba_freq/number_firms
cba_probability = cba_probability.reset_index()
fig4 = plt.figure(figsize= (15,8))
data = pd.DataFrame({"date": pd.period_range('2011-01-01', freq = 'M', periods = 84), "prob":cba_probability.cba_month.values}).set_index('date')
data['prob'].plot.bar(color='dodgerblue', rot=90)
plt.title('Probabilty of CBA')
plt.xticks(np.arange(0,84, step = 2))
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/cba_probability.png')
plt.show()