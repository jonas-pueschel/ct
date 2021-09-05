# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 21:14:11 2021

@author: Jonas
"""


import csv, sys, os
import numpy as np
from PIL import Image

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
                rnew = max(np.abs(i - mi/2),np.abs(i - mi/2 + 1))**2 + max(np.abs(j - mj/2),np.abs(j - mj/2 + 1))**2
                if  rnew > r2:
                    r2 = rnew         
    return r2

def add_data(image_name, p, q, avg_err, max_err, step):
    print("saving data...")
    BASEPATH = os.path.abspath(os.path.dirname(__file__)).replace('\\','/') + "/result_save"
    filename = BASEPATH + "/" + image_name + ".csv"
    with open(filename, 'a') as file:
        file.write("{};{};{};{};{}\n".format(p,q,avg_err, max_err, step))
        
def import_data(image_name):
    BASEPATH = os.path.abspath(os.path.dirname(__file__)).replace('\\','/') + "/result_save"
    filename = BASEPATH + "/" + image_name + ".csv"
    try:
        with open(filename, newline ='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            arr_in = list(reader)
        result = dict()
        for i in range(len(arr_in)):
            key = arr_in[i][0] + "/" + arr_in[i][1] + "/" + arr_in[i][4]
            if key not in result.keys():
                result[key] = (float(arr_in[i][2]), float(arr_in[i][3])) 
            else:
                print("WARNING: duplicate "+image_name+"-entry '"+ arr_in[i][0] + "/" + arr_in[i][1]+ "'")
        return result
    except Exception:
        return dict()

def draw_circle(f_in, r2, val = 240):
    xr,y = f_in.shape[0:2]
    r = np.sqrt(r2)
    for xn in range(xr):
        if xn < xr/2 - r or xn > xr/2 + r:
            f_in[xn,:] = np.ones(y) * val
            continue
        x = (xn-xr/2 + 0.5)
        border = np.sqrt(max(r2 - x**2,0)) #(max_y/2 + 0.5)
        lower = max(int(y/2 + 0.5 - border),0)
        upper = min(int(np.ceil(y/2 + 0.5 + border)), y)
        for ym in range(0,lower):
            f_in[xn,ym] = val
        for ym in range(upper, y):
            f_in[xn,ym] = val
            
def main():
    with Image.open("presets/shepp_logan.png").convert('L')  as img:
        f_in = np.array(img)
        x,y = f_in.shape[0:2]
        r_2 = np.sqrt(get_radius(f_in))
        r_1 = (np.linalg.norm(np.array([x,y]) ,2) /2)
        def draw_mod(r, pth):
            d = max(2*r, 2*y, 2* x)
            f_in_big = np.zeros((d,d))
            r = int(r)
            f_in_big[int(d/2-x/2):int(d/2-x/2)+x,int(d/2-y/2):int(d/2-y/2)+y] = f_in 
            f_in_big = f_in_big[int(d/2)-r:int(d/2)+r,int(d/2)-r:int(d/2)+r]
            draw_circle(f_in_big, r*r, val = 255)
            Image.fromarray(f_in_big.astype(np.uint8)).save(pth)
        draw_mod(r_1, "naive.png")
        draw_mod(r_2, "improved.png")
        

        

if __name__ == "__main__":
    main()