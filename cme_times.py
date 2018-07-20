#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import mktime, strptime

def cme_times(*times):
    
    timesmk = []
    minutes = [0]
    
    if len(times) <= 1:
        return "cme_times() requires at least two values."
    else:
        for time in times:
            timesmk.append(mktime(strptime(time, "%Y-%m-%dT%H:%M:00")))
        timesmk_index = 1
        for mk in timesmk:
            if len(timesmk) -1 >= timesmk_index:
                minutes.append((timesmk[timesmk_index] - mk) / 60)
                timesmk_index = timesmk_index + 1
            else:
                break
    
    return minutes