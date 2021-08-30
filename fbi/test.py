import numpy as np
import PIL

n = np.arange(100*100*3)
n = 
nar = np.array(PIL.Image.open("index.jpg"))
print(len(nar[0,0]))
im = PIL.Image.fromarray(nar)
im.save("filename.jpeg")

  def alt_call(self, theta, sigma):
        """
        

        Parameters
        ----------
        theta : TYPE
            DESCRIPTION.
        sigma : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        ret = np.array([0.0,0.0,0.0]) #rgb
        #Ursprung entspricht den koord. (len_x/2, len_y/2)^T
        #Wert in einem nat. intervall entspricht dem Wert "links oben"
        #(per Konvention)
                
        
        def next_int(x, dx, y, dy):
            """
            Parameters
            ----------
            x : float
            dx : float
            y : float
            dy : float
                DESCRIPTION.
        
            Returns
            -------
            (x_n,y_n,d)
            new x, new y, distance traveled
            """
            #dx > 0, da 

            def get_d(z, dz):
                if dz == 0:
                    return float('inf')
                if np.ceil(z) == z:
                    return 1/np.abs(dz)
                elif dz > 0:
                    return (np.ceil(z)-z)/dz
                else:
                    return (np.floor(z)-z)/dz
            d1 = get_d(x, dx)
            d2 = get_d(y, dy)
            if d1 < d2:
                return (np.round(x+ d1 * dx), y + d1 * dy, d1)
            elif d2 < d1:
                return (x+ d2 * dx, np.round(y + d2 * dy), d2)
            else:
                return (np.round(x+ d1 * dx), np.round(y + d1 * dy), d1)
        
        #starting point
        sp =  np.array([self.x/2, self.y/2]) +  sigma * self.r *  theta
        dx,dy = theta[0],theta[1]
        if dy == 0:
            #dx = 1
            x = 0
            y = sp[1]
        elif dx == 0:
            #dy = 1
            x = sp[0]
            y = 0
        else:
            x = sp[0] - sp[1]/dy * dx
            if x < 0:
                y = sp[1] - sp[0]/dx * dy
                x = 0
            elif x > self.x:
                y = sp[1] + sp[0]/dx * dy
                x = self.x
            else:
                y = 0
        x,y,d = next_int(x, dx, y, dy)
        if dx > 0:
            while x <= self.x and y <= self.y:
                #endet bei y = self.y oder x = self.x
                ret += d * self.pix[int(np.ceil(x)-1), int(np.ceil(y)-1)]
                x,y,d = next_int(x, dx, y, dy)
        else:
            while x >= 0 and y <= self.y:
                #endet bei y = self.y oder x = 0
                ret += d * self.pix[int(x), int(np.ceil(y)-1)]
                x,y,d = next_int(x, dx, y, dy)
        return ret/self.r