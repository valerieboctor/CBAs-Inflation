from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

pd.set_option('display.max_columns', 100)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

agreements_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/RAIS/'
figures_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/documents/Proof_of_Concept_VB/figures/'
os.chdir(agreements_path)


df = pd.read_csv('2013_2017_firmlevel_paneldecember.csv')

sum_vars = ['wage_min','wage_pct50', 'share_white', 'male', 'age', 'numb_work']
CBA_sum_stats = df[sum_vars].describe()
CBA_sum_stats = CBA_sum_stats.rename(columns={'wage_min': 'Min Wage','wage_pct50':'Median Wage', 'share_white':'% White', 'male':'% Male', 'age':'Avg Age', 'numb_work':'No. Workers'})
CBA_sum_stats.to_latex(figures_path+'CBA_Firms_Summ_Stats.tex')

# ~~~~~~~~~~~~~~~~~  Contracts data  ~~~~~~~~~~~~~~~~~
cba = pd.read_stata('acordos_infosecnpjmerged.dta')

fig,a = plt.subplots(1, 3, figsize = (13,5))
a[0].hist(cba.duration, color='r')
a[0].set_title('Duration of Wage Contracts (in Years)')
a[1].hist(cba.month_begin, color='g')
for i in range(1,3):
	plt.sca(a[i])
	plt.xticks(np.arange(1,13), ['Jan', 'Feb', 'Mar', 'Apr', \
	'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', \
	 'Dec'], fontsize = 9)
a[1].set_title('Beginning Month')
a[2].hist(cba.month_end, color='b')
a[2].set_title('Ending Month')
plt.savefig(figures_path+'CBA_Timing.png')
plt.clf()

# Preliminary result: plot of CBAs against year
cba.begin = pd.to_datetime(cba.begin)
cba_count = cba.begin.groupby(cba.begin.dt.year).agg(['count'])

CBA = cba.begin.dt.year[cba.begin.dt.year<2020]
fig = plt.figure(figsize = (7,5))
plt.hist(CBA, color = 'green', bins = len(np.arange(2006,2020)))
plt.xticks(np.arange(2006,2020))
plt.savefig(figures_path+'CBAs_per_year.png')
