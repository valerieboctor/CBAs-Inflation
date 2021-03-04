from __future__ import division
import numpy as np
import pandas as pd
import re
import os
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from collections import OrderedDict

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

figures_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/documents/Proof_of_Concept_VB/figures/'
ibre_clean_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/IBRE/'
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Consumer Inflation Expectations ~~~~~~~~~~~~~~~~~~~~~~
exp_inflation = np.array(df2.exp_inflation)
fig3 = plt.figure(figsize = (8,5))
exp_inflation_plot = plt.plot(t, exp_inflation, 'r', label = 'Expected Inflation')
plt.xticks(np.arange(0, len(t), 7), rotation = 45)
plt.title('Consumer Inflation Expectations')
plt.savefig(figures_path+'IBRE_Consumer_Inflation_Expectations.png')
plt.clf()
