# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 16:16:56 2021

@author: Jonas
"""


import numpy as np
from PIL import Image

def generate_wave(n = 500, k = 0, j = 0, out = "wave.png", norm = 2, vanish = 0.0, force_r = True, smooth = True, white_center = False):
    ar = np.zeros((n, n))
    r2 = (n/2)**2
    for x in range(n):
        for y in range(n):
            if force_r and (x- n/2 + 0.5) ** 2 + (y-n/2 + 0.5)**2 > r2:
                ar[x,y] = 0
                continue
            if k != 0 or vanish != 0:
                if norm == "inf" or norm == "infty" or norm == "infinity":
                    d = max(abs(x- n/2 + 0.5), abs(y-n/2 + 0.5))
                else:
                    d = np.linalg.norm(np.array([x- n/2 + 0.5, y - n/2 + 0.5]), norm)
                if k != 0:
                    if white_center:
                        vk = 0.5 + 0.5 * np.cos(d * (4 * k *np.pi)/n)
                    else:
                        vk = 0.5 - 0.5 * np.cos(d * (4 * k *np.pi)/n)
                else:
                    vk = 1
                if vanish != 0: 
                    #vanish with norm
                    vf = (1-vanish) + vanish * ((n - 2 * d))/n
                    if vf < 0:
                        vf = 0
                else:
                    vf = 1
            else:
                vk = 1
                vf = 1
            if j != 0:
                deg = np.arccos((x+ 0.5 - n/2)/np.linalg.norm(np.array([x + 0.5 - n/2, y + 0.5 - n/2]), 2))
                vj = 0.5 + 0.5 * np.cos(deg * j)
            else:
                vj = 1
            ar[x,y] = int(255 * vf * vk * vj)
            if not smooth:
                ar[x,y] = 255 * np.round(ar[x,y]/255)

    im = Image.fromarray(ar.astype(np.uint8))
    im.save(out)
    
def generate_flat_wave(n = 500, k = 0, force_r = True, out = "wave.png"):
    ar= np.zeros((n,n))
    r = n/2
    for x in range(n):
        val = ((0.5 - 0.5 * np.cos(2*k*np.pi * x/n)) * 255)
        xn2 = (x- n/2 + 0.5) ** 2
        for y in range(n):
            rad = np.sqrt(xn2 + (y-n/2 + 0.5)**2)
            if force_r and rad > r:
                continue
            if rad > 0.9 * r:
                vf = 10 * (r - rad)/r
            else:
                vf = 1
            ar[x,y] = int(val * vf)
    im = Image.fromarray(ar.astype(np.uint8))
    im.save(out)
            
    
if __name__ == "__main__":
    #generate_wave(k = 5.5,j = 0, vanish = 0, norm = 2, white_center = True, out = "wave.png", smooth = True, force_r = True)
    generate_flat_wave(k=18)