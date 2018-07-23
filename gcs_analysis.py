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
        all_cmesdf = all_cmesdf.append(ave_measurement)
    cmedf = cmedf.append(ave_measurement)
cmedf.to_csv(str(os.path.dirname(os.path.realpath(__file__))) +'/eUCLID.txt',sep = ":")

normdf = pd.DataFrame()

for name in all_cmesdf.columns:
    if all_cmesdf[name].dtypes != 'object':
        normdf[name] = abs(all_cmesdf[name]/all_cmesdf[name].median())
all_measurements = []
for name in normdf:
    for i in normdf[name]:
        all_measurements.append(i)
all_measurements=np.array(all_measurements)*100-100
plt.hist(all_measurements)
plt.title("Measurement Distrubution", size=23, fontname='Times New Roman')
# Labels the x and y axis.
plt.gca().set_xlabel("Percent Error", size=17, fontname='Times New Roman')
plt.ylabel("Frequency", size=17, fontname='Times New Roman')
# Makes the axis look nice (Thank you Cayenne)
plt.xticks(fontsize=15, fontname='Times New Roman', color='darkslategrey')
plt.yticks(fontsize=15, fontname='Times New Roman', color='darkslategrey')
# Creates a grid on the plot to make it more readable
plt.show()



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
