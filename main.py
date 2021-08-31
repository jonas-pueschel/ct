# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:41:22 2021

@author: Jonas
"""

import fbi.gui
import fbi.fbi

if __name__ == "__main__":
    try:
        fbi.gui.GUI()
    except Exception as e:
        print(e)