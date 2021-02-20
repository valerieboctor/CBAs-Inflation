	from __future__ import division
	import numpy as np
	import pandas as pd
	import re
	from matplotlib import pyplot as plt
	import os

	orbis_raw_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/raw/orbis/'
	orbis_clean_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/orbis/'
	figures_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/documents/Proof_of_Concept_VB/figures/'
	os.chdir(orbis_raw_path)

	columns = ['name', 'inactive', 'quoted', 'branch', 'own_data',\
	 'woco', 'country', 'nace', 'consolidation','last_year',\
	 'op_rev', 'employees', 'cf', 'st', \
	 'c_st', 'd_c_st','investments', 'd_investments' ]

	df10 = pd.read_excel('orbis10.xlsx', sheet_name = 'Results', \
		header = 0, names = columns)
	df10 = df10.replace('n.a.', np.nan)

	years = list(np.arange(10,20))
	for i in range(0, len(years)):
		years[i] = str(years[i])

	for i in range(len(years) - 1):
		if i == 0:
			df_old = pd.read_excel('orbis'+years[i]+'.xlsx',\
				sheet_name = 'Results', header = 0, \
				names = columns)
			data_year = ['20'+years[i]]*len(df_old)
			df_old['year'] = data_year
			df_old = df_old.replace('n.a.', np.nan)
		df_new  = pd.read_excel('orbis'+years[i+1]+'.xlsx',\
				sheet_name = 'Results', header = 0, \
				names = columns)
		data_year = ['20'+years[i+1]]*len(df_new)
		df_new['year'] = data_year 
		df_new = df_new.replace('n.a.', np.nan)
		df_new = pd.concat([df_old, df_new], axis = 0)
		df_old = df_new

	orbis = df_new

	cnpj = pd.read_excel(orbis_clean_path+'orbis_cnpj.xlsx',header = 0, \
		names = ['name', 'identificad'])
	# Excel file contains two types of ID for each firm
	# in no particular order, and some firms contain only the
	# relevant ID (CNPJ). The following code extracts CNPJ codes for
	# each firm.

	# First get the ID codes with form 'XX.XXX' (CNPJ)
	cnpj['identificad']= cnpj.identificad.str.extract(r'(^[0-9]{2}\..*)')
	# Make an array of the data.
	# Put firm names on the same line as cnpj codes
	_cnpj = np.array(cnpj)
	for i in range(1, len(_cnpj)):
		if type(_cnpj[i, 0]) == float:
			_cnpj[i, 0] = _cnpj[i-1, 0]           
	# Put the array back into a pandas dataframe
	cnpj = pd.DataFrame(_cnpj, columns = ['name', 'identificad'])
	# Drop duplicates. How = 'any' means the whole row is excluded
	# if any entries in the row are NaN.
	cnpj = cnpj.dropna(how = 'any')
	cnpj = cnpj.drop_duplicates()
	cnpj.to_csv(orbis_clean_path+'orbis_cnpj.csv')


	#id2= cnpj.identificad.str.extract(r'(^[0-9]{2}\.[0-9]{3}\.[0-9]{3})')
	#cnpj['id2'] = id2
	#cnpj = cnpj.drop_duplicates(subset = 'id2')
	orbis = orbis.merge(cnpj, on = 'name')
	orbis = orbis.drop_duplicates()
	orbis.to_csv(orbis_clean_path+'orbis10_19.csv')

