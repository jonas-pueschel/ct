# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 14:44:46 2021

@author: Jonas
"""

import fbi
from PIL import Image
import tkinter as tk, tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class GUI(tk.Tk):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.save = False
        self.file_in = None
        #self.pack()
        self.create_widgets()
        self.mainloop()
        
    def create_widgets(self):
        self.start_button = tk.Button(self)
        self.start_button["text"] = "start"
        self.start_button["command"] = self.start
        self.start_button.pack(side = "bottom")
        
        tk.Label(self,text="Input q:").pack(side = "top")
        self.input_q = tk.Entry(self)
        self.input_q.insert(10,"20")
        self.input_q.pack(side = "top")
       
        tk.Label(self,text="Input p (optional):").pack(side = "top")
        self.input_p = tk.Entry(self)
        self.input_p.pack(side = "top")
        
    def select_file(self):
        self.file_in = tkinter.filedialog.askopenfilename(parent=self, initialdir="/", title='Please select a picture')
    
    def start(self):
        try:
            q = int(self.input_q.get())
        except Exception as e:
            print(e)
            return
        while self.file_in == None:
            self.select_file()
        try:
            im = Image.open(self.file_in).convert('L') 
            f_in = np.array(im)  
        except Exception as e:
            print(e)
            return
        try:
            p = int(self.input_p.get())
        except Exception:
            p = int(np.pi * q)
        self.destroy()
        
        
        f_fbi, rf_a = fbi.filteredBackprojection(f_in, p, q)
        self.show_results(f_in, rf_a, f_fbi, p, q)
        
        
    def show_results(self, f_in, rf_a, f_fbi, p, q):   
        rf_b = np.zeros(rf_a.T.shape)
        rf_b[0 : q + 1] = rf_a.T[q : 2 * q + 1]
        rf_b[q + 1 : 2 * q + 1] = rf_a.T[0 : q]
        
        fig = plt.figure()
        ax = fig.add_subplot(2, 2, 1)
        imgplot1 = plt.imshow(f_in)
        ax.set_title('Original')
        #plt.colorbar(orientation='horizontal')
        ax = fig.add_subplot(2, 2, 2)
        plt.imshow(rf_b)
        ax.set_title('Radon Transform')
        #plt.colorbar(orientation='horizontal')
        ax = fig.add_subplot(2, 2, 3)
        plt.imshow(f_fbi)
        ax.set_title('Filtered Backprojection')
        #plt.colorbar(orientation='horizontal')
        ax = fig.add_subplot(2, 2, 4)
        plt.imshow(np.abs(f_fbi - f_in))
        ax.set_title('Absolute Error')
        #plt.colorbar(orientation='horizontal')
        fig.suptitle("CT: FBI with p=%s, q=%s" % (p,q))
        fig.subplots_adjust(right=0.8)
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        fig.colorbar(imgplot1, cax=cbar_ax)
        fig.show()
GUI()