import numpy as np
import pandas as pd

datafile = "C:/Users/Keyan/Desktop/Science/Data/GCS/cmedata.txt"
table = pd.read_csv(datafile, sep = ':',header=0)
