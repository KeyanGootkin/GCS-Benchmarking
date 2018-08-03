import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import croissant as cr
from glob import glob

figdir = "C:/Users/Keyan/Desktop/Science/Data/GCS/Figures/"
units = {"Lon": "(Degrees)", "Lat": "(Degrees)", "ROT": "(Degrees)",
         "Half Angle": "(Degrees)", "Ratio": '', "Velocity": "(km/s)"}
labels = {"Lon": "Longitude", "Lat": "Latitude", "ROT": "Tilt Angle",
          "Half Angle": "Half Angle", "Ratio": 'Aspect Ratio', "Velocity": "Velocity"}

all_cmes = cr.cme_match()
all_cmesdf, cmedf = cr.make_eUCLID(all_cmes)

dates = []

for t in cmedf["Time"]:
    dates.append(t[:10])

cr.plot_cmes(cmedf, all_cmesdf, dates, units, labels, figdir)
