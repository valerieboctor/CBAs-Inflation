from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

orbis_raw_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/raw/orbis/'
orbis_clean_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/orbis/'
figures_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/documents/Proof_of_Concept_VB/figures/'

os.chdir(orbis_clean_path)

df = pd.read_csv('orbis10_19.csv')
orbis_sum_stats = df[['op_rev', 'employees', 'cf', \
 'c_st', 'd_c_st']].describe()

orbis_sum_stats = orbis_sum_stats.rename(columns \
	= {'op_rev':'Operating Revenue', 'employees' \
	:'Employees', 'cf':'Cash Flow','c_st':\
	'Cash + S.T. Investment', 'd_c_st': 'D(c+st)'})
orbis_sum_stats.to_latex(figures_path+'orbis_sum_stats.tex')