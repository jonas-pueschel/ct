# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:14:11 2021

@author: Jonas
"""


import sys
import numpy as np

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress, prefix="Progress"):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...              \r\n"
    if progress >= 1:
        progress = 1
        status = "Done...              \r\n"
    block = int(round(barLength*progress))
    text = "\r"+prefix+": [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()


def get_radius(f_in):
    r = 0
    mi = f_in.shape[0]
    mj = f_in.shape[1]
    for i in range(mi):
        for j in range(mj):
            if f_in[i,j] != 0:
                if (i -mj/2 + 0.5)**2 + (i -mj/2 + 0.5)**2 > r:
                    r = (i -mj/2 + 0.5)**2
    return np.sqrt(r)