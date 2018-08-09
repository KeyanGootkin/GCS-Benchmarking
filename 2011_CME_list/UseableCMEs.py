#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from glob import glob

files_list = glob("/Users/rbroemme/Documents/NASA/2011 CMEs/univ*")

def find_cmes(file):
    data = pd.DataFrame(np.genfromtxt(file, usecols = (0,1,2,3,4), skip_header = 3, autostrip = True, dtype = str), columns = ["Date","Time","CPA","Width","Velocity"])
    dates,times = [],[]
    for w,v,d,t in zip(data["Width"],data["Velocity"],data["Date"],data["Time"]):
        if float(w) >= 50 and float(v) >= 500:
            dates.append(d)
            times.append(t)
            
    cmes = pd.DataFrame({"Dates":dates,"Times":times})
    return(cmes)

all_cmes = pd.DataFrame()    
for f in files_list:
    month_cmes = find_cmes(f)
    all_cmes = all_cmes.append(month_cmes,ignore_index=True)

print(all_cmes)

all_cmes.to_csv('all_cmes_500.txt', sep=' ')
