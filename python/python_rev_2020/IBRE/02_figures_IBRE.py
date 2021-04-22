from __future__ import division
import numpy as np
import pandas as pd
import re
import os
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from collections import OrderedDict
# Connection to FRED
import os
from fredapi import Fred

os.environ['api_key'] = 'fd13f48c5556bfa5a8fb4e49e90876d3'
key =os.getenv('api_key')
fred = Fred(key)
actual_inflation = fred.get_series('CPALTT01BRM659N')
actual_inflation = actual_inflation.rolling(12).mean() #rolling average of 12 months ahead (monthly) inflation
#actual_inflation = actual_inflation.pct_change(periods = 12)
actual_inflation = actual_inflation.loc['2005-09-01':'2020-03-01']

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

figures_path = '/Users/Valerie/CBAs-Inflation-Git/drafts/old_figures'
new_figures_path = '/Users/Valerie/CBAs-Inflation-Git/drafts/tables-figures/'
ibre_clean_path = '/Users/Valerie/Dropbox/Research/CBA monetary policy and firms/data/clean/IBRE/'
os.chdir(ibre_clean_path)

# ~~~~~~~~~~~~~~~~~~~~~~ Summary statistics ~~~~~~~~~~~~~~~~~~~~~
df = pd.read_csv('IBRE_Firm_Expectations_Clean.csv', index_col='date')
df2 = pd.read_csv('IBRE_Consumer_Expectations_Clean.csv', index_col='date')

df_sum_stats = df[['manufacturing', 'services', 'trade', 'construction']].describe()
df_sum_stats = df_sum_stats.rename(columns={'manufacturing': 'Manufacturing','services' : \
	'Services', 'trade':'Trade', 'construction':'Construction'})
df_sum_stats.to_latex(figures_path+'IBRE_Firms_Summ_Stats.tex')

df2_sum_stats = df2[['exp_inflation', 'cons_confidence']].describe()
df2_sum_stats = df2_sum_stats.rename(columns = {'exp_inflation' : 'Expected Inflation', \
	'cons_confidence' : 'Consumer Confidence'})
df2_sum_stats.to_latex( figures_path+'IBRE_Consumers_Summ_Stats.tex')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Firms' Business Expectations Series ~~~~~~~~~~~~~~~~~~~~~~~~~~~
all_data_date = '07/2010' # date on which expectations for all sectors are available
dates = ["2010-07-01", "2020-01-01"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
t = np.array(list(OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in range((end - start).days)).keys()))

manufacturing = np.array(df.manufacturing[all_data_date :])
services = np.array(df.services[all_data_date :])
trade = np.array(df.trade[all_data_date :])
construction = np.array(df.construction[all_data_date :])
fig = plt.figure(figsize = (8,5))
man_plot = plt.plot(t, manufacturing, 'red', label = 'Manufacturing')
ser_plot = plt.plot(t, services, 'green', label = 'Services')
tra_plot = plt.plot(t, trade, 'm', label = 'Trade')
con_plot = plt.plot(t, construction, 'b', label = 'Construction')
plt.legend()
plt.xticks(np.arange(0,len(t), 6) ,rotation = 45)
plt.title('Brazilian Firms Expectations of Business Conditions')
plt.savefig(figures_path+'IBRE_Firm_Expectations.png')
fig.clear()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Consumer Expectations Series ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
dates = ["2005-09-01", "2020-04-01"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
t = np.array(list(OrderedDict(((start + timedelta(_)).strftime(r"%b-%y"), None) for _ in range((end - start).days)).keys()))
exp_inflation = np.array(df2.exp_inflation)
confidence = np.array(df2.cons_confidence)
present_confidence = np.array(df2.pres_cons_confidence)
fig2 = plt.figure(figsize = (8,5))
conf_plot = plt.plot(t, confidence, 'r', label = 'Consumer Confidence')
pres_conf_plot = plt.plot(t, present_confidence, 'b', label = 'Consumer Confidence of Present Situation')
plt.legend()
plt.xticks(np.arange(0, len(t), 7), rotation = 45)
plt.title('Consumer Confidence')
plt.savefig(figures_path+'IBRE_Consumer_Expectations.png')
fig.clear()
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Realized Inflation & Consumer Inflation Expectations ~~~~~~~~~~~~~~~~~~~~~~
exp_inflation = np.array(df2.exp_inflation)
max_exp_inflation = max(df2.exp_inflation)
loc_max_exp = np.where(exp_inflation == max_exp_inflation)[0][0]
preshock_position = 112
postshock_position = 151
inflation = np.array(actual_inflation)
fig3 = plt.figure(figsize = (14,8))
exp_inflation_plot = plt.plot(t, exp_inflation, 'r', label = 'Expected Inflation (12 months ahead forecast)')
inflation_plot = plt.plot(t, inflation, 'b', label = 'Actual Inflation (12 months ahead rolling average)')
plt.xticks(np.arange(0, len(t), 4), rotation = 45)
plt.legend()
plt.title('Realized Inflation and Consumer Expectations')
plt.axvline(x = loc_max_exp, color = 'black', linestyle='-')
plt.axvline(x = preshock_position, color = 'black', linestyle='--')
plt.axvline(x = postshock_position, color = 'black', linestyle='--')
plt.savefig(new_figures_path+'Realized_Inflation_and_Consumer_Expectations.png')
plt.clf()
