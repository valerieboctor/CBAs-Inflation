from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os
#### Goal in this file is to merge compustat with agreements data and run preliminary regressions specified in the proof of concept file. 
# Specify directories
firms_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/compustat/'
agreements_path = '/Users/Valerie/Dropbox/Courses/CoursesSpring2020/ECON236B/236B_FinalPaper/CBA monetary policy and firms/data/clean/RAIS/'
os.chdir(agreements_path)	
agreements = pd.read_csv('2013_2017_firmlevel_paneldecember.csv')
