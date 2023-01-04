# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 16:36:41 2022

@author: user
"""

import numpy as np
a=np.load("data.npy")
b=np.load("data2.npy")
c=np.load("data3.npy")
d=np.load("data4.npy")
e=np.load("data5.npy")
f=np.load("data6.npy")
g=np.load("data7.npy")
h=np.load("data8.npy")
i=np.load("data9.npy")
k=np.load("data10.npy")
j=np.load("labeldata.npy")

final=np.concatenate((a,b,c,d,k,g,h,i),axis=0)
np.save("finaldata",final)
