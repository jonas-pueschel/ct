# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 14:44:46 2021

@author: Jonas
"""

import fbi
from PIL import Image
import tkinter as tk, tkinter.filedialog
import numpy as np

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
        self.start_button["state"] = "disabled"
        
        f_fbi, rf_a = fbi.filteredBackprojection(f_in, p, q)
        
        def picturized(ndarr, shift0 = 0, shift1 = 0):
            ret = np.zeros(ndarr.shape, np.uint8)
            for j in range(ndarr.shape[0]):
                js = j - shift0
                for k in range(ndarr.shape[1]):
                    ks = k - shift1
                    if(ndarr[js,ks] < 0):
                        ret[j,k] = 0
                    elif(ndarr[js,ks] > 255):
                        ret[j,k] = 255
                    else:
                        ret[j,k] = int(ndarr[js,ks])
            return ret
        
        im_rf = Image.fromarray(picturized(np.rot90(rf_a), shift0 = q))
        im_fbi = Image.fromarray(picturized(f_fbi))
        im_err = Image.fromarray(picturized(np.abs(f_in - f_fbi)))
        if(self.save):
            try:
                im.save(self.file_in[0:-4] + "_bw.png")
                im_rf.save(self.file_in[0:-4] + "_rf.png")
                im_fbi.save(self.file_in[0:-4] + "_fbi.png")
                im_err.save(self.file_in[0:-4] + "_err.png")
            except Exception as e:
                print(e)
                return
        self.show_results(im, im_rf, im_fbi, im_err)
                
        self.start_button["state"] = "normal"
        
    def show_results(self, im, im_rf, im_fbi, im_err):
        result_win = tk.Tk()
        l_im = tk.Label(result_win, image = im)
        l_im.grid(row = 0, column = 1)
        l_imt = tk.Label(result_win, text="Original (b/w)")
        l_imt.grid(row = 0, column = 1)
        result_win.mainloop()
GUI()