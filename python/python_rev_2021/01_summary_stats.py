from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

agreements_path = '/Users/Valerie/Dropbox/Research/CBA monetary policy and firms/data/clean'
os.chdir(agreements_path)
graph_df = pd.read_stata('panel_firmsCBA_jan2021.dta')
# want to make a graph that shows the difference in nominal wage growth among firms that had CBAs before Feb 2016 and those that had CBAs just after

month = graph_df.month.astype(int)
year = graph_df.year.astype(int)
monthly_date = 100*year + month
graph_df['monthly_date'] = monthly_date

#check number of non NaN observations:
# np.sum(cba_df.COLUMN_NAME.count())

# make a dummy variable that equals the sum of the month of contract and the contract duration is >= 12
graph_df = graph_df[['identificad', 'monthly_date', 'rem','duration', 'cba_month']]
graph_df['cba_time'] = graph_df.monthly_date[graph_df.cba_month ==1]
cba_jan16 = (graph_df.cba_time == 201601).astype(int)
cba_mar16 = (graph_df.cba_time== 201603).astype(int)

N = graph_df.identificad.count() #this is the number of rows in the data set before merging, including rows with NaN values
graph_df['cba_jan16'] = cba_jan16
graph_df['cba_mar16'] = cba_mar16

date_vars = ['monthly_date']
for i in date_vars:
	graph_df[i] = pd.to_datetime(graph_df[i], yearfirst='True', format = '%Y%m')

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
# Make average and median wage series for firms that had CBAs in Mar16, Jan16, and average of all firms.
wage_graph_df = graph_df[graph_df['monthly_date'].astype('float').between(201501, 201712, inclusive=True)]
rem_cba_jan16_avg = wage_graph_df[['monthly_date', 'rem_cba_jan16']].groupby('monthly_date').mean()
rem_cba_jan16_avg = rem_cba_jan16_avg.reset_index()
rem_cba_jan16_avg = rem_cba_jan16_avg.rename(columns={"rem_cba_jan16": "rem_cba_jan16_avg"})
rem_cba_jan16_avg.monthly_date = pd.to_datetime(rem_cba_jan16_avg.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_jan16_med = wage_graph_df[['monthly_date', 'rem_cba_jan16']].groupby('monthly_date').median()
rem_cba_jan16_med = rem_cba_jan16_med.reset_index()
rem_cba_jan16_med = rem_cba_jan16_med.rename(columns={"rem_cba_jan16": "rem_cba_jan16_med"})
rem_cba_jan16_med.monthly_date = pd.to_datetime(rem_cba_jan16_med.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_mar16_avg = wage_graph_df[['monthly_date', 'rem_cba_mar16']].groupby('monthly_date').mean()
rem_cba_mar16_avg = rem_cba_mar16_avg.reset_index()
rem_cba_mar16_avg = rem_cba_mar16_avg.rename(columns={"rem_cba_mar16": "rem_cba_mar16_avg"})
rem_cba_mar16_avg.monthly_date = pd.to_datetime(rem_cba_mar16_avg.monthly_date, yearfirst='True', format = '%Y%m')

rem_cba_mar16_med = wage_graph_df[['monthly_date', 'rem_cba_mar16']].groupby('monthly_date').median()
rem_cba_mar16_med = rem_cba_mar16_med.reset_index()
rem_cba_mar16_med = rem_cba_mar16_med.rename(columns={"rem_cba_mar16": "rem_cba_mar16_med"})
rem_cba_mar16_med.monthly_date = pd.to_datetime(rem_cba_mar16_med.monthly_date, yearfirst='True', format = '%Y%m')


med_rem = wage_graph_df[['monthly_date', 'rem']].groupby('monthly_date').median()
med_rem = med_rem.reset_index()
med_rem.monthly_date = pd.to_datetime(med_rem.monthly_date, yearfirst='True', format = '%Y%m')


# Graph Average and Median Wages for Groups of Firms (All, CBA Mar16, CBA Jan16)
fig1 = plt.figure(figsize = (10,7))
plt.plot(rem_cba_mar16_avg.monthly_date, rem_cba_mar16_avg.rem_cba_mar16_avg, label = "Average -- CBAs in Mar 2016")
plt.plot(rem_cba_jan16_avg.monthly_date, rem_cba_jan16_avg.rem_cba_jan16_avg, label = "Average -- CBAs in Jan 2016")  
plt.plot(rem_cba_mar16_med.monthly_date, rem_cba_mar16_med.rem_cba_mar16_med, label = "Median -- CBAs in Mar 2016")
plt.plot(rem_cba_jan16_med.monthly_date, rem_cba_jan16_med.rem_cba_jan16_med, label = "Median -- CBAs in Jan 2016")  
plt.plot(med_rem.monthly_date, med_rem.rem, label = "Median -- All Firms in Sample" )
plt.title("Monthly Remuneration 2015-2017")
plt.legend()
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/tables-figures/avg_med_rem_2015_2017.png')
plt.clf()
plt.close()
rem_cba_jan16_avg['rem_cba_jan16_growth'] = rem_cba_jan16_avg.rem_cba_jan16_avg.pct_change()
rem_cba_mar16_avg['rem_cba_mar16_growth'] = rem_cba_mar16_avg.rem_cba_mar16_avg.pct_change()

#==========================================================================================================================
# plot normalized version of the graph above
# first generate the normalized series
plot_dfs = [rem_cba_mar16_avg, rem_cba_jan16_avg, rem_cba_mar16_med, rem_cba_jan16_med, med_rem]
plot_series = ["rem_cba_mar16_avg", "rem_cba_jan16_avg", "rem_cba_mar16_med", "rem_cba_jan16_med", "rem"]
labels = ["Average -- CBAs in Mar 2016", "Average -- CBAs in Jan 2016", "Median -- CBAs in Mar 2016", "Median -- CBAS in Jan 2016", "Median -- All Firms"]
preshock_date = "2015-12-01"

fig2 = plt.figure(figsize = (10,7))
for i in range(0, len(plot_dfs)):
	norm_factor = np.array(plot_dfs[i][plot_series[i]][plot_dfs[i].monthly_date == preshock_date])
	plot_dfs[i]['norm_'+plot_series[i]] = plot_dfs[i][plot_series[i]] / norm_factor
	plt.plot(plot_dfs[i]['monthly_date'], plot_dfs[i]['norm_'+plot_series[i]], label = labels[i])
plt.legend()
plt.title("Normalized Monthly Remuneration 2015-2017")
plt.savefig('/Users/Valerie/CBAs-Inflation-Git/tables-figures/normalized_avg_med_rem_2015_2017.png')
plt.clf()
plt.close()	
#==========================================================================================================================
#==========================================================================================================================


# plot the probability of having a CBA given time since last CBA
# -------------------------------------------------------------------------------------------------------------------------

# Define Helper Function:
def fill_missing(grp):  
    res = grp.set_index('monthly_date')\
    .replace(to_replace=pd.NaT, method='ffill') #need this line to replace NaT, not zero
    del res['identificad']
    return res
# Replace zeroes in the cba_time_variable with date of previous CBA
graph_df = graph_df.set_index('monthly_date')
df = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]  

main_df =[graph_df[['identificad', 'cba_time']], graph_df[['identificad', 'cba_time']].loc['2014-04':'2016-01'],  \
graph_df[['identificad', 'cba_time']].loc['2016-03':'2017-12']] 
# main_df[0] #whole series
# main_df[1] #pre shock
# main_df[2] #post shock
#--------------------------------------------------------------------------------------------------------------------------
for i in range(len(df)):
	main_df[i] = main_df[i].reset_index()
	df[i] = main_df[i]
	df[i] = df[i].groupby(['identificad']).apply(
    lambda grp: fill_missing(grp)
	)
	df[i] = df[i].reset_index()    	
	#--------------------------------------------------------------------------------------------------------------------------
	# Merge with main dataset
	df[i]= df[i].rename(columns={"cba_time": "date_last_cba"})
	df[i] = main_df[i].merge(df[i], on = ['identificad', 'monthly_date'], how = 'inner')
#--------------------------------------------------------------------------------------------------------------------------
bar_dfs = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]
bar_dfs_transformed = [pd.DataFrame(), pd.DataFrame(), pd.DataFrame()]

for i in range(len(bar_dfs)):
	bar_dfs[i] = df[i][df[i].date_last_cba==df[i].date_last_cba]
	bar_dfs[i].date_last_cba = pd.to_datetime(bar_dfs[i].date_last_cba.astype(int), yearfirst = True, format = "%Y%m")
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
	print(hazard_rate)

fig3 = plt.figure(figsize = (10,7))
time_since_cba = hazard_rate.time_since_cba
probability = hazard_rate.probability_of_cba_next_period

time_since_cba = hazard_rate.time_since_cba
probability = hazard_rate.probability_of_cba_next_period

plt.bar(time_since_cba,probability, label = "Full sample Jan 2011 - December 2017")
plt.bar()
plt.xticks(np.arange(0, 84, step = 3))
plt.title("CBA Hazard Rate 2011-2017")
plt.xlabel("Months Since Last CBA")
plt.show()


#==========================================================================================================================
# separately plot the probability of having a CBA in each month over the entire sample
#==========================================================================================================================