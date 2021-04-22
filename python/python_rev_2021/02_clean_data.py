# I have no idea what I'm doing, but here goes nothing!
from __future__ import division
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import os

data_path = '/Users/Valerie/Dropbox/Research/CBA monetary policy and firms/data/clean/RAIS/deidentified_RAIS'
os.chdir(data_path)
# Read in the masked raw data
# Need to generate the wage series for only incumbent workers
# cry sob

df15 = pd.read_csv('workers_bargainedfirms2015.csv')
df16 = pd.read_csv('workers_bargainedfirms2016.csv')
df17 = pd.read_csv('workers_bargainedfirms2017.csv')
