# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 22:21:07 2022

@author: user
"""

import numpy as np
import os
import wave
import pylab as plt
import librosa.display
import sklearn
j=0
number=498
number2=(number-1)/3
normalized_mfcc=np.zeros((166,13,44))
normalized_mfcc1=np.zeros((36,13,44))
import matplotlib.pyplot as plt
for i in range(0,number,3):
    
    filepath="C:\\Users\\user\\Desktop\\voice_data\\env\\data4"
    path=filepath+"\\e_1-"+str(i)+".wav"
    data, sr = librosa.load(path)
    print(sr)
    mfccs = librosa.feature.mfcc(y=data, sr=sr,n_mfcc=13,dct_type=2,norm='ortho')
    #mfccs = sklearn.preprocessing.scale(mfccs)
    print(np.shape(mfccs))
    normalized_mfcc[j] = librosa.util.normalize(mfccs) #-1~1
    mfcccs=normalized_mfcc[j]
    print(j)
    j=j+1
    #np.save(int(j),normalized_mfcc)
np.save("data10",normalized_mfcc)