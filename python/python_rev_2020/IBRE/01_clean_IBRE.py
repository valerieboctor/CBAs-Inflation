import numpy as np
import pandas as pd
import os

# Specify directories
expectations_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/IBRE/'
os.chdir('/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/raw/IBRE/')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IBRE Firm Expectations ~~~~~~~~~~~~~~~~~~~~~~~~
# read in the data
# encoding = "ISO-8859-1", but don't need to specify here
firm_expectations_columns = ['date', 'manufacturing', 'services', 'trade', 'construction', 'consumers', 'prev_employment', 'current_employment']
df = pd.read_csv('IBRE_Firm_Expectations.csv', sep = '[;\n]', \
	decimal=',', engine='python', header=0,\
	 names = firm_expectations_columns)

# clean data slightly
df = df.set_index('date')
df = df.replace(' - ', np.nan)
df = df.replace(' -', np.nan)
for i in range(1, len(firm_expectations_columns)):
	df[firm_expectations_columns[i]] = df[firm_expectations_columns[i]].astype('float')

df.to_csv(expectations_path+'IBRE_Firm_Expectations_Clean.csv', sep = ',')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ IBRE Consumer Expectations ~~~~~~~~~~~~~~~~~~~~~~~~
consumer_expectations_columns = ['date', 'exp_inflation', 'cons_confidence', 'pres_cons_confidence']
df2= pd.read_csv('IBRE_Consumer_Expectations.csv', sep = '[;\n]', \
	decimal=',', engine='python', header = 0,\
	names = consumer_expectations_columns)

df2 =  df2.set_index('date')
df2.to_csv(expectations_path +'IBRE_Consumer_Expectations_Clean.csv')