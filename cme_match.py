#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Given our current setup, directories must be in the format "data/[acjkr]data".

from glob import glob

def cme_match(*directories):

    files, cmes, matches = [], [], []

    if len(directories) == 0:
        files.extend(glob("data/[acjkr]data/[0-9]WLRT_[1-2]???-??-??.rt"))
    else:
        for directory in directories:
            files.extend(glob(directory + "/[0-9]WLRT_[1-2]???-??-??.rt"))
        
    for file in files:
        cmes.append(file[-19:])

    cmes = list(set(cmes))
    cmes.sort()
    
    for cme in cmes:
        matches.append([file for file in files if cme in file])
        
    return matches