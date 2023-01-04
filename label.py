# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 13:34:46 2022

@author: user
"""

import numpy as np
data_a=[]
for i in range(202):
    data_a.append("ambulance")
for i in range(166):
    data_a.append("enviroment")
"""for i in range(176):
    data_a.append("fire")"""
for i in range(354):
    data_a.append("police")

np.save("labeldata",data_a)