import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant as cr
from glob import glob


datdir = str(os.path.dirname(os.path.realpath(__file__))) + "/data"
figdir = "C:/Users/Keyan/Desktop/Science/Data/GCS/Figures/"

all_cmes = cr.cme_match()

all_cmesdf,cmedf = cr.make_eUCLID(all_cmes)

print(all_cmesdf)
print(cmedf)

dates = []
for t in cmedf["Time"]:
    dates.append(t[:10])

normarray = []
for name in all_cmesdf.columns:
    if all_cmesdf[name].dtypes != 'object':
        name_norm_array = []
        new_norm = pd.Series()
        for base_time in dates:
            temp_storage = []
            for ind_time,x in zip(all_cmesdf["Time"],all_cmesdf[name]):
                if base_time[:10] == ind_time[:10]:
                    temp_storage.append(x)

            if name == "Velocity":
                norms = ((np.array(temp_storage)-np.mean(np.array(temp_storage)))/np.mean(np.array(temp_storage)))*100
            else:
                norms = (np.array(temp_storage)-np.mean(np.array(temp_storage)))

            for i in norms:
                name_norm_array.append(i)
            normarray.append(norms)
            plt.hist(norms)
            plt.title(name +' '+ base_time + ' std: ' + str(np.std(name_norm_array)))
            plt.savefig(figdir + 'Individual_CMEs/' + name + "_" + base_time,overwrite=True)
            plt.clf()
        plt.hist(name_norm_array)
        plt.title(name+ ' std: ' + str(np.std(name_norm_array)))
        plt.savefig(figdir + 'Individual_Parameters/'+name,overwrite=True)
        plt.clf()

    """
    if all_cmesdf[name].dtypes != 'object' and name == "Half Angle":

        new_norm = pd.Series()
        for base_time in cmedf["Time"]:
            temp_storage = []
            for ind_time,x in zip(all_cmesdf["Time"],all_cmesdf[name]):
                if base_time[:9] == ind_time[:9]:
                    temp_storage.append(x)
            norms = (np.array(temp_storage)-np.mean(np.array(temp_storage)))/np.mean(np.array(temp_storage))

            normarray.append(norms)
"""

all_measurements = []
for name in normarray:
    for i in name:
        all_measurements.append(i)
#normdf.hist()
#plt.show()

"""
all_measurements=(np.array(all_measurements))
plt.figure(figsize=[10,10])
plt.hist(all_measurements,bins=30)
plt.title("CME Measurement Distrubution", size=20, fontname='Times New Roman')
# Labels the x and y axis.
plt.gca().set_xlabel("Percent Spread in Measurement", size=17, fontname='Times New Roman')
plt.ylabel("Frequency", size=17, fontname='Times New Roman')
# Makes the axis look nice (Thank you Cayenne)
plt.xticks(fontsize=15, fontname='Times New Roman', color='darkslategrey')
plt.yticks(fontsize=15, fontname='Times New Roman', color='darkslategrey')
# Creates a grid on the plot to make it more readable
plt.savefig("C:/Users/Keyan/Desktop/cmespread.png",overwrite=True)

plt.show()
print(np.std(all_measurements))
"""
