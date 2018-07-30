import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant as cr
from glob import glob

figdir = "C:/Users/Keyan/Desktop/Science/Data/GCS/Figures/"

all_cmes = cr.cme_match()

all_cmesdf, cmedf = cr.make_eUCLID(all_cmes)


dates = []
for t in cmedf["Time"]:
    dates.append(t[:10])
units = {"Lon": "(Degrees)", "Lat": "(Degrees)", "ROT": "(Degrees)",
         "Half Angle": "(Degrees)", "Ratio": '', "Velocity": "(km/s)"}
labels = {"Lon": "(Degrees)", "Lat": "(Degrees)", "ROT": "(Degrees)",
         "Half Angle": "(Degrees)", "Ratio": '', "Velocity": "(km/s)"}
normarray = []

for name in all_cmesdf.columns:
    if all_cmesdf[name].dtypes != 'object':
        mean_list, std_list, range_list = [], [], []

        name_norm_array = []
        new_norm = pd.Series()
        for base_time in dates:
            temp_storage = []
            for ind_time, x in zip(all_cmesdf["Time"], all_cmesdf[name]):
                if base_time[:10] == ind_time[:10]:
                    temp_storage.append(x)
            mean_p = np.mean(temp_storage)
            mean_list.append(mean_p)
            std_p = np.std(temp_storage)
            std_list.append(std_p)
            range_p = max(temp_storage) - min(temp_storage)
            range_list.append(range_p)

            if name == "Velocity":
                norms = ((np.array(temp_storage) - np.mean(np.array(temp_storage))
                          ) / np.mean(np.array(temp_storage))) * 100
            else:
                norms = (np.array(temp_storage) -
                         np.mean(np.array(temp_storage)))

            for i in norms:
                name_norm_array.append(i)
            normarray.append(norms)

        cr.make_hist(std_list, range_list, name, units, figdir)
        cr.make_scatter(std_list, range_list, mean_list, name, units, figdir)
