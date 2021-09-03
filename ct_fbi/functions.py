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
    r2 = 0
    mi = f_in.shape[0]
    mj = f_in.shape[1]
    for i in range(mi):
        for j in range(mj):
            if f_in[i,j] != 0:
                rnew = (i - mi/2 + 0.5)**2 + (j -mj/2 + 0.5)**2
                if  rnew > r2:
                    r2 = rnew         
    return r2

def draw_circle(f_in, r2):
    xr,y = f_in.shape[0:2]
    r = np.sqrt(r2)
    for xn in range(xr):
        if xn < xr/2 - r or xn > xr/2 + r:
            f_in[xn,:] = np.ones(y) * 240
            continue
        x = (xn-xr/2 + 0.5)
        border = np.sqrt(max(r2 - x**2,0)) #(max_y/2 + 0.5)
        lower = max(int(y/2 + 0.5 - border),0)
        upper = min(int(np.ceil(y/2 + 0.5 + border)), y)
        for ym in range(0,lower):
            f_in[xn,ym] = 240
        for ym in range(upper, y):
            f_in[xn,ym] = 240
            


