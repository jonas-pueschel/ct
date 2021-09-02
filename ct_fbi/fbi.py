# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 13:44:14 2021

@author: Jonas
"""
import numpy as np
import functions


class RadonTransform:
    def __init__(self, f_in):
        """
        Parameters
        ----------
        img_path : String
            image path.
        """
        
        self.pix = f_in
        self.x, self.y = self.pix.shape[0:2]
        self.r = np.sqrt(self.x*self.x+self.y*self.y)/2
        #self.messungen = np.reshape(np.zeros(self.x * self.y), (self.x, self.y))

    
    def __call__(self, theta, sigma):
        ret = 0
        sp =  np.array([self.x/2, self.y/2]) +  sigma * self.r *  theta
        dx,dy = theta[1],-theta[0]
        
        def half_axis(x,y,dx,dy):
            ret = 0
            x += dx
            y += dy
            while x >= 0 and x < self.x and y >= 0 and y < self.y:
                ret += self.pix[int(x), int(y)]
                #self.messungen[int(x), int(y)] = 255
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
                #self.messungen[int(x), int(y)] = 255
            ret += half_axis(x,y, dx, dy)
            ret += half_axis(x, y, -dx, dy)        
        
        return ret/self.r
    
def filteredBackprojection(f_in, p, q):
    rf = RadonTransform(f_in)
    n = f_in.shape[0]
    m = f_in.shape[1]
    #sampling
    rf_a = np.zeros((p,(2*q+1)))
    h = 1/q
    theta = np.array([[np.cos(phi),np.sin(phi)] for phi in np.linspace(0, np.pi,num = p, endpoint = False)])
    for j in range(p):
        if p>1:
            functions.update_progress(j/(p-1), prefix = "Sampling")
        else:
            functions.update_progress(1.0, prefix = "Sampling")
        for k in range(-q,q+1):
            sigma = k * h
            rf_a[j,k] = rf(theta[j],sigma)

    #fbi
    fbi = np.reshape(np.zeros(rf.x * rf.y), (rf.x, rf.y))
    v = np.reshape(np.zeros(p*(2*q+1)), (p,(2*q+1)))

    for j in range(p):
        if p>1:
            functions.update_progress(j/(p-1), prefix = "Calculating v_j,k")
        else:
            functions.update_progress(1.0, prefix = "Calculating v_j,k")
        for k in range(-q, q+1):
            ar = [(1/(1 - (4 * (k-l) * (k-l)))) * rf_a[j,l] for l in range(-q,q+1)]
            v[j,k] = sum(ar) 
    
    for xn in range(n):
        x = (xn-rf.x / 2 + 0.5)/rf.r
        functions.update_progress(xn/(n-1), prefix = "Reconstructing")
        for ym in range(m):
            y = (ym - rf.y / 2 + 0.5)/rf.r
            sm = 0
            for j in range(p):
                frac = (theta[j,0] * x + theta[j,1] * y)*q
                k = int(frac)
                if frac < 0:
                    k -= 1
                t = frac - k
                sm += (1-t)* v[j,k] + t * v[j,k+1]
            fbi[xn,ym] =  sm
            
    factor1 = q/(np.pi * np.pi) * 2 * np.pi /p
    fbi *= factor1
    return fbi, rf_a
    