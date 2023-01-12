# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 18:53:09 2023

@author: Administrator
"""

import os
import wave
path="D:\\voice_data\\test\\"
audiolist=os.listdir(path)

for i in audiolist:
    wf=wave.open(path+i,"r")
    print(wf.getframerate())