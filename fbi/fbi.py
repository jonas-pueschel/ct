# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:44:14 2021

@author: Jonas
"""

import numpy as np
import sys
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
"""
"""
class RadonTransform:
    def __init__(self, img_path):
        """
        Parameters
        ----------
        img_path : String
            image path.
        """
        
        self.pix =np.array(Image.open(img_path).convert('L') )
        self.x, self.y = self.pix.shape[0:2]
        self.r = np.sqrt(self.x*self.x+self.y*self.y)/2
        self.messungen = np.reshape(np.zeros(self.x * self.y), (self.x, self.y))

    
    def __call__(self, theta, sigma):
        ret = 0
        sp =  np.array([self.x/2, self.y/2]) +  sigma * self.r *  theta
        dx,dy = theta[1],-theta[0]
        
        def half_axis(x,y,dx,dy,ret):
            ret = 0
            x += dx
            y += dy
            while x >= 0 and x < self.x and y >= 0 and y < self.y:
                ret += self.pix[int(x), int(y)]
                self.messungen[int(x), int(y)] = 255
                x += dx
                y += dy
            return ret
    
        def get_vf(x,dx):
            if dx == 0:
                return 0
            vf = -x/dx
            if(vf < 0):
                vf -= 1
            else: 
                vf +=1
            return int(vf)
        x,y = sp[0],sp[1]
        vf = 0
        if x < 0:
            vf = get_vf(x,dx)
        elif x > self.x:
            vf = get_vf(x-self.x,dx)
        elif y < 0:
            vf = get_vf(y,dy)
        elif y > self.y:
            vf = get_vf(y-self.y,dy)  
        x += vf * dx
        y += vf * dy
        if x >= 0 and x <= self.x and y >= 0 and y <= self.y:
            if x != self.x and y != self.y:
                ret += self.pix[int(x), int(y)]
                self.messungen[int(x), int(y)] = 255
            ret += half_axis(x,y,dx,dy,ret)
            ret += half_axis(x, y, -dx, -dy,ret)        
        
        return ret/self.r
    
def filteredBackprojection(img_in, img_out, radon_out = None, 
                           q =10, p = None):
    if p == None:
        p = int(np.pi * q)
    rf = RadonTransform(img_in)
    
    #sampling
    rf_a = np.reshape(np.zeros(p*(2*q+1)), (p,(2*q+1)))
    h = 1/q
    theta = np.array([[np.cos(phi),np.sin(phi)] for phi in np.linspace(0, np.pi,num = p, endpoint = False)])
    for j in range(p):
        update_progress(j/(p-1), prefix = "Sampling")
        for k in range(-q,q+1):
            sigma = k * h
            rf_a[j,k] = rf(theta[j],sigma)

    #fbi
    fbi = np.reshape(np.zeros(rf.x * rf.y), (rf.x, rf.y))
    v = np.reshape(np.zeros(p*(2*q+1)), (p,(2*q+1)))

    for j in range(p):
        update_progress(j/(p-1), prefix = "Calculating v_j,k")
        for k in range(-q, q+1):
            ar = [(1/(1 - (4 * (k-l) * (k-l)))) * rf_a[j,l] for l in range(-q,q+1)]
            v[j,k] = sum(ar) 
            #print(v[j,k])
    
    for xn in range(rf.x):
        x = (xn-rf.x / 2 + 0.5)/rf.r
        update_progress(xn/(rf.x-1), prefix = "Reconstructing")
        for yn in range(rf.y):
            y = (yn - rf.y / 2 + 0.5)/rf.r
            sm = 0
            for j in range(p):
                frac = (theta[j,0] * x + theta[j,1] * y)*q
                k = int(frac)
                if frac < 0:
                    k -= 1
                t = frac - k
                sm += (1-t)* v[j,k] + t * v[j,k+1]
            fbi[xn,yn] =  sm
            
    factor1 = q/(np.pi * np.pi) * 2 * np.pi /p
    fbi *= factor1
    mx = np.amax(fbi)
    print(mx)
    fbi_pic = np.array(fbi)
    for i in range (rf.x):
        for j in range (rf.y):
            if fbi_pic[i,j] < 0:
                fbi_pic[i,j] = 0
            elif fbi_pic[i,j] > 255:
                fbi_pic[i,j] = 255
    im = Image.fromarray(fbi_pic.astype(np.uint8))
    im.save(img_out)
    im2 = Image.fromarray(rf.messungen.astype(np.uint8))
    im2.save("messungen.png")
    
    
if __name__ == "__main__":
    filteredBackprojection("indexmod.png", "im.png")
    #rf = RadonTransform("grey.png")
    #print(rf(np.array([np.sin(np.pi/8),np.cos(np.pi/8)]),0.77))
    
