from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

ipca_clean_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/IPCA/'
ibre_clean_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/IBRE/'
figures_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/documents/Proof_of_Concept_VB/figures/'
os.chdir(ipca_clean_path)

for root, dirs, files in os.walk("."):
    for filename in files:
        print(filename)

# Read in daily financial firms' inflation expectations
df = pd.read_csv('IPCA_Clean_Average05_19.csv') # The IPCA data is given at the daily level
df = df[['Date', 'Avg']] 
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%m/%d/%y')
fig = plt.figure(figsize = (5,5))
plt.plot(df.Date, df.Avg, 'b', label = 'Average')
plt.xticks(np.arange(0, len(df.Date), 30), rotation = 45, fontsize = 8)
plt.title('Financial Firms Average Inflation Expectations')
plt.savefig(figures_path+'IPCA_Financial_Firms_Expectations.png')
fig.clear()


# Get monthly firm inflation expectations
df_m = df
df_m.set_index('Date', inplace=True)
df_m.index = pd.to_datetime(df_m.index)
df_m = df_m.resample('1M').mean() 
df_m = df_m.reset_index()
df_m.Date = pd.to_datetime(df_m.Date)
df_m.Date = df_m.Date.dt.strftime('%m/%y') # Now these dates match those in the consumer inflation expectations series

# Read in consumer inflation expectations 
df2 = pd.read_csv(ibre_clean_path + 'IBRE_Consumer_Expectations_Clean.csv')
df2.date =pd.to_datetime(df2.date)
df2.date = df2.date.dt.strftime('%m/%y')

# Read in actual (annual inflation) Note: need to find monthly series!
df_actual = pd.read_csv(ipca_clean_path+'Actual_Inflation05_19.csv')
df_actual.Date = pd.to_datetime(df_actual.Date)
df_actual.Date = df_actual.Date.dt.strftime('%m/%y') # Now these dates match those in the consumer inflation expectations series, too.

# Plot Inflation Expectations
fig,ax = plt.subplots()
ax.plot(df2.exp_inflation, 'r', label = 'Consumers')
ax.plot(df_m.Date[8:], df_m.Avg[8:], 'b', label= 'Financial Firms')
plt.title('Expected Inflation Over Next 12 Months')
plt.xticks(np.arange(0,len(df2.date),6), rotation = 45, fontsize = 8)
ax.legend()
plt.savefig(figures_path+'Inflation_Expectations.png')
plt.clf()

# Plot Actual Inflation
fig,ax = plt.subplots()
plt.title('Actual Inflation (Percent Change From Previous Year)')
ax.plot(df_actual.Date, df_actual.Inflation, 'g', label = 'Actual Inflation (Annual)')
plt.xticks(np.arange(0,len(df_actual.Date)), rotation = 45, fontsize = 8)
plt.savefig(figures_path+'Annual_Inflation.png')
plt.clf()
# Get inflation summary statistics
df_m = df_m.set_index('Date')
df2 = df2.set_index('date')
inflation = pd.concat([df_m.Avg, df2.exp_inflation], axis = 1, sort  = False)
inflation_sum_stats = inflation[['Avg', 'exp_inflation']].describe()
inflation_sum_stats = inflation_sum_stats.rename(columns = {'Avg':'Financial Firms', \
	'exp_inflation' :'Consumers'})
inflation_sum_stats.to_latex( figures_path+'Inflation_Expectations_Summ_Stats.tex')
