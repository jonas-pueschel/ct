# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 14:44:46 2021

@author: Jonas
"""

#TODO: Array input for p,q
#TODO: multithreading? multiprocessing?

import fbi
from PIL import Image, ImageTk
import tkinter as tk, tkinter.filedialog
import numpy as np
import matplotlib.pyplot as plt
import os
#from matplotlib import rc
#rc('font', **{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)
#LaTeX installation required!

class GUI(tk.Tk):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pic_p_arr = []
        self.preset_dir = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')+ "/presets"
        for filename in next(os.walk(self.preset_dir), (None, None, []))[2]:
            if filename.endswith(".gif") or filename.endswith(".png") or filename.endswith(".jpg"):
                self.pic_p_arr += [self.preset_dir + "/" + filename]


        self.index = 0
        self.tkim = None            

        self.create_widgets()
        self.mainloop()
        
    def show_preset(self, im = None):
        if len(self.pic_p_arr) == 0:
            return
        
        if self.index < 0:
            self.index = len(self.pic_p_arr) - 1
        elif self.index >= len(self.pic_p_arr):
            self.index = 0
        file = self.pic_p_arr[self.index]
        if im == None:
            im = Image.open(file).convert('L') 
        self.im = im.copy()
        w = im.width
        h = im.height
        
        self.im_desc["text"] = (file.split("/")[-1].split("\\")[-1]
                                + " ({}x{})".format(w,h))
        
        if w > h:
            size = 200, int(h / w * 200)
        elif w < h:
            size = int(w / h * 200), 200
        else:
            size = 200, 200
        im.thumbnail(size, Image.ANTIALIAS)
        self.tkim = ImageTk.PhotoImage(im)
        if self.im_label == None:
            self.im_label = tk.Label(self, image=self.tkim)
            self.im_label.place(x = 100, y = 30, width = 200, height = 200)
        else:
            self.im_label["image"] = self.tkim
            self.im_label.config(image = self.tkim)
        

    def create_widgets(self):
        self.title("Filtered Backprojection v1.0")
        self.config(width = 400, height = 400)
        self.resizable(width=False, height=False)
        
        tk.Button(self, text = "Show CT", command = lambda: self.start(show = True, chart = False)).place(x = 60, y = 360, width = 80, height = 25)
        tk.Button(self, text = "Show errors", command = lambda: self.start(show = False, chart = True)).place(x = 160, y = 360, width = 80, height = 25)
        tk.Button(self, text = "Show both", command = lambda: self.start(show = True, chart = True)).place(x = 260, y = 360, width = 80, height = 25)
        
        tk.Label(self,text="Input q:").place(x = 50, y = 300, width = 100, height = 15)
        self.input_q = tk.Entry(self)
        self.input_q.insert(10,"20")
        self.input_q.place(x = 150, y = 300, width = 150, height = 15)
       
        tk.Label(self,text="Input p:").place(x = 50, y = 320, width = 100, height = 15)
        self.input_p = tk.Entry(self)
        self.input_p.insert(10, "optimal")
        self.input_p.place(x = 150, y = 320, width = 150, height = 15)
        
        self.im_label = None
        self.im_desc = tk.Label(self)
        self.im_desc.place(x = 0, y = 230, width = 400, height = 15)
        self.show_preset()
        
        tk.Button(self, text = "add image", command = self.select_file).place(x = 160 ,y = 250,width = 80, height = 20)
        tk.Button(self, text = "next", command = self.next_p).place(x = 250 ,y = 250,width = 60, height = 20)
        tk.Button(self, text = "prev", command = self.prev_p).place(x = 90 ,y = 250,width = 60, height = 20)   
        
    def select_file(self):
        file = tkinter.filedialog.askopenfilename(parent=self, initialdir="/", title='Please select a picture')
        try:
            #test if it can be opened:
            im = Image.open(file).convert('L') 
            #SAVE FILE, MAY BE DEACTIVATED!
            if(True):
                file_end = file.split("/")[-1].split("\\")[-1]
                file = self.preset_dir + "/" + file_end
                im.save(file)
            self.pic_p_arr += [file]
            self.index = len(self.pic_p_arr) - 1
            self.show_preset(im = im)
            print("File loaded")
        except Exception:
            print("Couldn't load image: invalid file")
            return

    def next_p(self):
        self.index += 1
        self.show_preset()
        
    def prev_p(self):        
        self.index -= 1
        self.show_preset()
    
    def get_vals(self):

        def get_val(st):
            if len(st) == 0:
                return []
            if ":" in st:
                spl = st.split(",")
                st1 = spl[0]
                try:
                    spl2 = st1.split(":")
                    if len(spl) == 1:
                        step = 1
                    elif len(spl) == 2:
                        step = int(spl[1])
                    else:
                        return []
                    return range(int(spl2[0]), int(spl2[1])+1, step)
                except Exception as e:
                    print(e)
                    return []
            else:
                ar = []
                for s in st.split(","):
                    try:
                        i = int(s)
                        ar += [i]
                    except Exception as e:
                        print(e)
                        return []
                return ar
        
        qs = sorted(get_val(self.input_q.get()))
        inp = self.input_p.get()
        ps = []
        if  inp.strip() == "optimal":
            for j in range(len(qs)):
                ps += [int(np.pi * qs[j])]
        elif inp.strip()[0:5] == "const":
            cs = inp.split("const")[1].strip()
            if cs == "":
                cc = qs[int(len(qs)/2)]**2 * np.pi
            else:
                try:
                    cc = 1.03 * (qs[int(len(qs)/2)])**2 * float(cs)
                except Exception:
                    print("Error: invalid input for p ('const' must only be followed with an optional number)")
                    return [],[]
            for q in qs:
                ps += [int(cc/(q))]
        else:           
            ps = get_val(inp)
            if len(ps) == 0:
                for j in range(len(qs)):
                    ps += [int(np.pi * qs[j])]
            elif len(qs) < len(ps):
                while len(qs) < len(ps):
                    qs += qs
                qs = qs[0:len(ps)]
            else:
                while len(qs) > len(ps):
                    ps += ps
                ps = ps[0:len(qs)]
        if(min(ps) <= 0 or min(qs) <= 0):
            print("Error: invalid input: p and q may not be <= 0")
            return [],[]
        return ps,qs
    
    
    def start(self, show = True, chart = True):
        while self.index == -1:
            self.select_file()
        ps, qs = self.get_vals()
        if len(qs) == 0:
            print("Error: Invalid Input for p,q")
        f_in = [None for i in qs]
        f_fbi = [None for i in qs]
        rf_a = [None for i in qs]
        for i in range(len(qs)):
            q = qs[i]
            p = ps[i]
            im = Image.open(self.pic_p_arr[self.index]).convert('L')
            f_in[i] = np.array(im)
            print("Calculating fbi with p={}, q = {}".format(p,q))
            print("img: " + self.pic_p_arr[self.index])
            f_fbi[i], rf_a[i] = fbi.filteredBackprojection(f_in[i], p, q)
        if show:
            for i in range(len(f_in)):
                self.show_results(f_in[i], rf_a[i], f_fbi[i], ps[i], qs[i])
                #save??
        if chart:
            max_err = [None for i in qs]
            avg_err =  [None for i in qs]
            
            for i in range(len(max_err)):
                f_err = np.abs(f_in[i] - f_fbi[i])
                avg_err[i] = np.sum(f_err) / (f_err.shape[0] * f_err.shape[1])
                max_err[i] = np.amax(f_err)
            self.show_plots(ps, qs, avg_err, max_err)

        
    def show_plots(self, ps, qs, avg_err, max_err):
        #pq = [str((ps[i], qs[i])) for i in range(len(ps))]
        plt.subplot(121)
        plt.plot(qs, avg_err, 'go')
        plt.xlabel('q')
        plt.ylabel('avg. error')
        
        plt.subplot(122)
        plt.plot(qs, max_err, 'ro')
        plt.xlabel('q')
        plt.ylabel('max. error')
        plt.suptitle("Error Analysis for the FBI-Alogrithm")
        plt.tight_layout()
        plt.show()
        
        pass
    
    def show_results(self, f_in, rf_a, f_fbi, p, q):   
        rf_b = np.zeros(rf_a.T.shape)
        rf_b[0 : q] = rf_a.T[q+1 : 2 * q + 1]
        rf_b[q : 2 * q + 1] = rf_a.T[0 : q+1]
        
        fig = plt.figure()
        ax = fig.add_subplot(2, 2, 1)
        imgplot1 = plt.imshow(f_in, vmin = 0, vmax = 255)
        ax.set_title('Original')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        
        ax = fig.add_subplot(2, 2, 2)
        plt.imshow(rf_b, extent=[0, p, q, -q], cmap="hot")# vmin = 0, vmax = 255)
        #different scale for better visibility
        plt.colorbar()
        ax.set_title('Radon Transform')
        ax.set_xlabel("j = 0,...,p-1" )
        ax.set_ylabel("k = -q,...,q")

        ax = fig.add_subplot(2, 2, 3)
        plt.imshow(f_fbi, vmin = 0, vmax = 255)
        ax.set_title('Filtered Backprojection')
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        ax = fig.add_subplot(2, 2, 4)
        f_err = np.abs(f_fbi - f_in)
        avg_error = np.sum(f_err) / (f_err.shape[0] * f_err.shape[1])
        plt.imshow(f_err, vmin = 0, vmax = 255)
        ax.set_title("Error (avg: {:0.3f})".format(avg_error))
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        fig.suptitle("Computerized Tomography: FBI with p=%s, q=%s" % (p,q))
        plt.tight_layout()
        fig.subplots_adjust(right=0.8)
        
        cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
        fig.colorbar(imgplot1, cax=cbar_ax)
        
        fig.show()
