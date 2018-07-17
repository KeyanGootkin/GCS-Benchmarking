import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant.py as cr

datdir = str(os.path.dirname(os.path.realpath(__file__))) + "/data/"
datafiles = glob(datdir+'*')
#Crawford does some stuff and then I get an average
eUCLID = pd.DataFrame()
for file in datafiles:
    average_df,start_t,start_h = cr.function_name(file)
    enlil_start_time = cr.find_cme_start(start_t,start_h,average_df["Velocity"])
    average_df["Time at 21.5"] = pd.Series([enlil_start_time])
    eUCLID = eUCLID.append(average_df)






    # use scipy's curve fit to optimize the slope and intercept of the line
    popt, pcov = curve_fit(funct, ts, hs)
    s, i = popt[0], popt[1]


table = pd.read_csv(datafile, header=0, names=["Time", "Lon", "Lat", "ROT", "Height", "Ratio", "Half Angle"],
                    usecols=[0, 1, 2, 3, 4, 5, 6], delim_whitespace=True)
replace_list = []
for x in table["Lon"]:
    if x >= 360:
        replace_list.append(x)
table["Lon"] = table["Lon"].replace(replace_list,np.array(replace_list)-360)

print(table)
