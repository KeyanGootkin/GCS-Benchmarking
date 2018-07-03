import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

datafile = str(os.path.dirname(os.path.realpath(__file__)))+"/cmedata.txt"
print(datafile)
table = pd.read_csv(datafile, sep = ':',header=0)
print(table)
