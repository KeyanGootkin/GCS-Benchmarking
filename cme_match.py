#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Given our current setup, directories must be a list with items in the format
# "data/[acjkr]data".

from glob import glob
from re import search

def cme_match(directories):

    files, cmes, matches = [], [], []

    for directory in directories:
        files.extend(glob(directory + "/[0-9]WLRT_[1-2]???-??-??.rt"))

    for file in files:
        cmes.append(file[-13:-3] + file[-19:-18])
        cmes = list(set(cmes))

    cmes.sort()

    for cme in cmes:
        matches.append([file for file in files if search(cme[-1:] + "WLRT_" +
        cme[:9],file)])

    return matches
