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
        Constructor, creates Object
        
        Parameters
        ----------
        f_in: 2-dim numpy array
            representing the to-be-transformed function
        """
        self.pix = f_in
        self.x, self.y = self.pix.shape[0:2]
        self.r = np.sqrt(functions.get_radius(f_in))

    
    def __call__(self, theta, sigma, step):
        """
        Called when the object is called, e.g Rf = RadonTransform(f); Rf(...)

        Parameters
        ----------
        theta : 2x1 numpy array
            representing an element of S^1, input of Rf
        sigma : float
            -1 <= sigma <= 1, input of Rf
        step : float
            step size for the integration rule

        Returns
        -------
        float
            Value of the Radon-Transform for the given input
        """
        ret = 0
        #starting point
        sp =  np.array([self.x/2, self.y/2]) + theta * sigma * self.r
        
        
        #dx,dy, original length one, gets length step
        dx,dy = theta[1] * step,-theta[0]*step
        #integration over half-straigt line starting in (x,y) with dir. dx,dy
        def half_axis(x,y,dx,dy):
            ret = 0
            x += dx
            y += dy
            while x >= 0 and x < self.x and y >= 0 and y < self.y:
                ret += self.pix[int(x), int(y)]
                x += dx
                y += dy
            return ret
        
        #get a factor so that sp + vf *(dx,dy) is inside the picture
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
            ret += half_axis(x,y, dx, dy)
            ret += half_axis(x, y, -dx, -dy)
        
        return ret/self.r
    
def filteredBackprojection(f_in, p, q, step = 0.5):
    """
    Calculates the filtered backprojection for f_in with p, q

    Parameters
    ----------
    f_in : 2-dim numpy array
           representing the to-be-reconstructed function
    p : int
        number of theta-samples (equidistant in [0, pi) )
    q : int
        number of sigma-samples (eqidistant in [-1,1])
    step : float, optional
        step-size for Radon-Transform integration rule. The default is 0.5.

    Returns
    -------
    fbi : 2-dim numpy array
        filtered backprojection (interpolated) of f_in
    rf_a : 2-dim numpy array
        discrete Radon Transform of f_in, dim = (2q+1)x p
    """
    #sampling
    rf = RadonTransform(f_in)
    theta = np.array([[np.cos(phi),np.sin(phi)] for phi in np.linspace(0, np.pi,num = p, endpoint = False)])
    sigma = np.linspace(-1,1, num = 2 * q + 1, endpoint = True)
    rf_a = np.zeros((p,(2*q+1)))
    for j in range(p):
        functions.update_progress((j+1)/p, prefix = "Sampling")
        for k in range(0, 2 * q+1):
            rf_a[j,k-q] = rf(theta[j],sigma[k], step)
    rf_a *= step
    
    #fbi
    fbi = np.zeros((rf.x, rf.y))
    v = np.zeros((p,(2*q+1)))

    #calculate v
    for j in range(p):
        functions.update_progress((j+1)/p, prefix = "Calculating v_j,k")
        for k in range(-q, q+1): 
            v[j,k] = np.sum([(1/(1 - (4 * (k-l) * (k-l)))) * rf_a[j,l] for l in range(-q,q+1)]) 

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
            sm = 0
            for j in range(p):
                frac = (theta[j,0] * x + theta[j,1] * y)*q
                k = int(frac)
                if frac < 0:
                    k -= 1
                t = frac - k
                sm += (1-t)* v[j,k] + t * v[j,k+1]
            fbi[xn,ym] =  sm 
    #multiply by factor
    fbi *= q/(np.pi * np.pi) * 2 * np.pi /p

    return fbi, rf_a
    