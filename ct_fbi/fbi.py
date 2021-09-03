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
        self.r = np.sqrt(functions.get_radius(f_in)) + 1
        self.med = np.array([self.x/2, self.y/2])
        #self.med = np.array([self.x/2 - 0.5, self.y/2 - 0.5])
        #self.messungen = np.reshape(np.zeros(self.x * self.y), (self.x, self.y))

    
    def __call__(self, theta, sigma):
        ret = 0
        sp =  self.med +  sigma * self.r *  theta
        
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
            ret += half_axis(x, y, -dx, -dy)
        
        return ret/self.r
    
def filteredBackprojection(f_in, p, q, step = 1):
    rf = RadonTransform(f_in)
    #sampling
    rf_a = np.zeros((p,(2*q+1)))
    h = 1/q
    theta = np.array([[np.cos(phi),np.sin(phi)] for phi in np.linspace(0, np.pi,num = p, endpoint = False)])
    for j in range(p):
        functions.update_progress((j+1)/p, prefix = "Sampling")
        for k in range(-q,q+1):
            sigma = k * h
            rf_a[j,k] = rf(step * theta[j],sigma)
    rf_a *= step
    
    #fbi
    fbi = np.zeros((rf.x, rf.y))
    v = np.zeros((p,(2*q+1)))

    for j in range(p):
        functions.update_progress((j+1)/p, prefix = "Calculating v_j,k")
        for k in range(-q, q+1):
            ar = [(1/(1 - (4 * (k-l) * (k-l)))) * rf_a[j,l] for l in range(-q,q+1)]
            v[j,k] = sum(ar) 
    
    r_inv = 1/rf.r
    lwr = max(int(rf.x/2 + 0.5 - rf.r),0)
    upr = min(int(np.ceil(rf.y/2 + 0.5 + rf.r)), rf.x)
    for xn in range(lwr, upr):
        x = (xn-rf.x / 2 + 0.5)
        functions.update_progress((xn+1-lwr)/(upr-lwr), prefix = "Reconstructing")
        border = np.sqrt(max(rf.r**2 - x**2,0)) #(max_y/2 + 0.5)
        lower = max(int(rf.y/2 + 0.5 - border),0)
        upper = min(int(np.ceil(rf.y/2 + 0.5 + border)), rf.y)
        x *= r_inv
        for ym in range(lower,upper):
            y = (ym - rf.y / 2 + 0.5)*r_inv
            pnt = np.array([x,y])
            if np.linalg.norm(pnt)>= rf.r:
                fbi[xn,ym] = 0
                continue
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
    