import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant as cr
from glob import glob
from cme_match import cme_match

datdir = str(os.path.dirname(os.path.realpath(__file__))) + "/data"
datafolders = glob(datdir + '/*')
datafiles = []

for folder in datafolders:
    for file in glob(folder + '/*'):
        datafiles.append(file)

# Crawford does some stuff that will help me get a df that just has all the measurements for one CME in one place
all_cmes = cme_match(datafolders)
#print(all_cmes[0])
df = pd.read_csv(all_cmes[0][0], names=["Lon", "Lat", "ROT", "Height", "Ratio", "Half Angle"],
                          delim_whitespace=True, header=0, usecols=[1,2,3,4,5,6])

cmedf = pd.DataFrame()
for cme in all_cmes:
    for mf in cme:
        measurement = pd.read_csv(mf, names=["Lon", "Lat", "ROT", "Height", "Ratio", "Half Angle"],
                                  delim_whitespace=True, header=0, usecols=[1,2,3,4,5,6])

        measurement = measurement.mean()
        measurement = pd.DataFrame({'Lon':measurement['Lon'],'Lat':measurement['Lat'],'ROT':measurement['ROT'],'Height':measurement['Height'],'Ratio':measurement['Ratio'],'Half Angle':measurement['Half Angle']}, index=[0])
        cmedf = cmedf.append(measurement)

print(cmedf)


'''


eUCLID = pd.DataFrame()
for file in datafiles:
    average_df, start_t, start_h = cr.function_name(file)
    enlil_start_time = cr.find_cme_start(
        start_t, start_h, average_df["Velocity"])
    average_df["Time at 21.5"] = pd.Series([enlil_start_time])
    eUCLID = eUCLID.append(average_df)
print(eUCLID)
eUCLID.to_csv(str(os.path.dirname(os.path.realpath(__file__))) + "/eUCLID.txt")
'''
