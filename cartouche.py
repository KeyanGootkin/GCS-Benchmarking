# -*- coding: utf-8 -*-
# Takes dates in the format 1970-01-01T00:00:00 but ignores the last two digits.

import time
import bisect
import numpy as np




def cr2sh(date,carrington):
    carrots = np.loadtxt(str(os.path.dirname(os.path.realpath(__file__))) + "/carrots.txt")
    # turn input date into a mathable value
    datemk = time.mktime(time.strptime(date,"%Y-%m-%dT%H:%M:00"))

    # identify start and end times for the rotation
    rotation = bisect.bisect(carrots,datemk)
    start = carrots[rotation - 1]
    end = carrots[rotation]

    # the math part
    stonyhurst = carrington - 360 * (1 - (datemk - start) / (end - start))

    # make sure results are in bounds
    if stonyhurst < 0:
        return stonyhurst + 360
    else:
        return stonyhurst

def sh2cr(date,stonyhurst):
    carrots = np.loadtxt(str(os.path.dirname(os.path.realpath(__file__))) + "/carrots.txt")

    # re-commenting this is beneath my dignity
    datemk = time.mktime(time.strptime(date,"%Y-%m-%dT%H:%M:00"))

    rotation = bisect.bisect(carrots,datemk)
    start = carrots[rotation - 1]
    end = carrots[rotation]

    # note plus sign
    carrington = stonyhurst + 360 * (1 - (datemk - start) / (end - start))

    if carrington > 360:
       return carrington - 360
    else:
        return carrington
