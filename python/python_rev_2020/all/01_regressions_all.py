from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import statsmodels.api as sm
import os

agreements_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/RAIS/'
orbis_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/orbis/'
ibre_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/IBRE/'
all_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/all/'
figures_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/documents/Proof_of_Concept_VB/figures/'

	os.chdir(all_path)
	orbis = pd.read_csv(orbis_path+'orbis10_19.csv')
	orbis = orbis.iloc[:,1:orbis.shape[1]]
	rais_firms = pd.read_csv(agreements_path+\
		'2013_2017_firmlevel_paneldecember.csv')
rais_firms = rais_firms.iloc[:,1:rais_firms.shape[1]]
agreements = pd.read_stata(agreements_path+\
	'acordos_infosecnpjmerged.dta')
identificad = list(np.zeros(len(orbis.identificad)))
for i in range((len(orbis.identificad))):
	identificad[i] = str(re.sub('[./-]', '', orbis.identificad.loc[i]))
orbis['identificad'] = identificad	

orbis = orbis.rename(columns = {'year':'year_begin'})
df = orbis.merge(agreements, on = ['identificad', 'year_begin'], how = 'outer')

# Generate a dummy variable for whether the firm
# had a CBA in a given year:

CBA = np.zeros(len(df))
for i in range(len(CBA)):
	if df.duration.loc[i] == df.duration.loc[i]:
		CBA[i] = 1 #replace value to 1 if we have data
		# on a CBA agreement in a given firm-year
		# note: if NaN, var!=var
df['CBA'] = CBA

df15 = df[df.year_begin == 2015]
df15 = df15[['name', 'd_c_st', 'CBA']]
df15 = df15.dropna(how = 'any')
df15 = df15.drop_duplicates()

CBA = np.array(df15.CBA).reshape(len(df15.CBA), 1)
FE = np.array(pd.get_dummies(df15.name)) #get fixed effects 

Y = np.array(df15.d_c_st)
X = np.concatenate((CBA, FE), axis = 1)
X = sm.add_constant(X)
model = sm.OLS(Y, X)
results15 = model.fit()
reg15_tex = results15.summary().as_latex()

f = open(figures_path+'reg15.tex', 'w')
f.write(str(reg15_tex))
f.close()

df16 = df[df.year_begin == 2016]
df16 = df16[['name', 'd_c_st', 'CBA']]
df16 = df16.dropna(how = 'any')
df16 = df16.drop_duplicates()

CBA = np.array(df16.CBA).reshape(len(df16.CBA), 1)
FE = np.array(pd.get_dummies(df16.name)) #get fixed effects 

Y = np.array(df16.d_c_st)
X = np.concatenate((CBA, FE), axis = 1)
X = sm.add_constant(X)
model = sm.OLS(Y, X)
results16 = model.fit()
reg16_tex = results16.summary().as_latex()

f = open(figures_path+'reg16.tex', 'w')
f.write(str(reg16_tex))
f.close()