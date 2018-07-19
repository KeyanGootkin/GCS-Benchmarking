#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Given our current setup, directories must be a list with items in the format
# "data/[acjkr]data".

from glob import glob
from re import search

def cme_match(directories):

    files, cmes = [], []
    
    for directory in directories:
        files.extend(glob(directory + "/[0-9]WLRT_[1-2]???-??-??.rt"))
    
    for file in files:
        cmes.append(file[-13:-3] + "cme" + file[-19:-18])
        cmes = list(set(cmes))

    cmes.sort()
    matches = {key: [] for key in cmes}

    for key in matches:
        matches[key].append([file for file in files if search(key[-1:] + "WLRT_" + key[:9],file)])
 
    return matches