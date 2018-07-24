import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant as cr
from glob import glob


datdir = str(os.path.dirname(os.path.realpath(__file__))) + "/data"

all_cmes = cr.cme_match()
cmedf = pd.DataFrame()
all_cmesdf = pd.DataFrame()

for cme in all_cmes:
    for mf in cme:
        measurement = pd.read_csv(mf, names=["Time", "Lon", "Lat", "ROT", "Height", "Ratio", "Half Angle"],
                                  delim_whitespace=True, header=0, usecols=[0, 1, 2, 3, 4, 5, 6])
        ave_measurement = measurement.mean()
        times_list = cr.cme_times(measurement["Time"])
        velocity = cr.cme_line_fit(times_list, measurement["Height"], return_slope = True)
        ave_measurement = pd.DataFrame({"Time":measurement["Time"][len(measurement["Time"])-1], 'Lon': ave_measurement['Lon'], 'Lat': ave_measurement['Lat'], 'ROT': ave_measurement['ROT'],
                                    "Velocity":velocity, 'Ratio': ave_measurement['Ratio'], 'Half Angle': ave_measurement['Half Angle']}, index=[0])
        all_cmesdf = all_cmesdf.append(ave_measurement,ignore_index=True)
    cmedf = cmedf.append(ave_measurement,ignore_index=True)
cmedf.to_csv(str(os.path.dirname(os.path.realpath(__file__))) +'/eUCLID.txt',sep = ":")
print(all_cmesdf)
normarray = []
for name in all_cmesdf.columns:
    if all_cmesdf[name].dtypes != 'object' and name != 'ROT':

        new_norm = pd.Series()
        for base_time in cmedf["Time"]:
            temp_storage = []
            for ind_time,x in zip(all_cmesdf["Time"],all_cmesdf[name]):
                if base_time[:9] == ind_time[:9]:
                    temp_storage.append(x)
            norms = (np.array(temp_storage)-np.mean(np.array(temp_storage)))/np.mean(np.array(temp_storage))

            normarray.append(norms)


all_measurements = []
for name in normarray:
    for i in name:
        all_measurements.append(i)
#normdf.hist()
#plt.show()
print(all_measurements)

all_measurements=(np.array(all_measurements)*100)

plt.hist(all_measurements,bins=30)
plt.title("Measurement Distrubution", size=23, fontname='Times New Roman')
# Labels the x and y axis.
plt.gca().set_xlabel("Percent Error", size=17, fontname='Times New Roman')
plt.ylabel("Frequency", size=17, fontname='Times New Roman')
# Makes the axis look nice (Thank you Cayenne)
plt.xticks(fontsize=15, fontname='Times New Roman', color='darkslategrey')
plt.yticks(fontsize=15, fontname='Times New Roman', color='darkslategrey')
# Creates a grid on the plot to make it more readable
plt.show()
print(np.std(all_measurements))
