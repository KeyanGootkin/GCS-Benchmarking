import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant as cr
from glob import glob





datdir = str(os.path.dirname(os.path.realpath(__file__))) + "/data"
datafolders = glob(datdir+'/*')
datafiles = []
for folder in datafolders:
    for file in glob(folder+'/*'):
        datafiles.append(file)
#Crawford does some stuff that will help me get a df that just has all the measurements for one CME in one place
cmes = []
for file in datafiles:
    cmes.append(cr.single_cme_function(file))



eUCLID = pd.DataFrame()
for file in datafiles:
    average_df,start_t,start_h = cr.function_name(file)
    enlil_start_time = cr.find_cme_start(start_t,start_h,average_df["Velocity"])
    average_df["Time at 21.5"] = pd.Series([enlil_start_time])
    eUCLID = eUCLID.append(average_df)
print(eUCLID)
eUCLID.to_csv(str(os.path.dirname(os.path.realpath(__file__)))+"/eUCLID.txt")
