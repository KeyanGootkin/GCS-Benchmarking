import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant as cr
from glob import glob

#Path to where you want plots to be stored
figdir = "C:/Users/Keyan/Desktop/Science/Data/GCS/Figures/"
#dictionary of units for the different parameters as you want them to appear in plots
units = {"Lon": "(Degrees)", "Lat": "(Degrees)", "ROT": "(Degrees)",
         "Half Angle": "(Degrees)", "Ratio": '', "Velocity": "(km/s)"}
#diction containing what you want each parameter to be called in the title of plots
labels = {"Lon": "Longitude", "Lat": "Latitude", "ROT": "Tilt Angle",
          "Half Angle": "Half Angle", "Ratio": 'Aspect Ratio', "Velocity": "Velocity"}

#match up all files that have measurements of the same CME
all_cmes = cr.cme_match()
#makes eUCLID (average measurements of each CME) and a DataFrame with all measurements of all CMEs
all_cmesdf, cmedf = cr.make_eUCLID(all_cmes)

#Make a list of only dates (so that different times are ignored
dates = []
for t in cmedf["Time"]:
    dates.append(t[:10])

#plot histograms and scatter plots
cr.plot_cmes(cmedf, all_cmesdf, dates, units, labels, figdir)
