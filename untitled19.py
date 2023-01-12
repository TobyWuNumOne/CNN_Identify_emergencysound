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
import matplotlib.pyplot as plt
j=0
number=498
number2=(number-1)/3

normalized_mfcc1=np.zeros((36,13,44))
path="D:\\voice_data\\police\\data4_22050\\"
audiolist=os.listdir(path)
normalized_mfcc=np.zeros((len(audiolist),13,44))
import matplotlib.pyplot as plt
for i in audiolist:
    
    """filepath="C:\\Users\\user\\Desktop\\voice_data\\env\\data4"
    path=filepath+"\\e_1-"+str(i)+".wav"""
    data, sr = librosa.load(path+i)
    print(sr)
    mfccs = librosa.feature.mfcc(y=data, sr=sr,n_mfcc=13,dct_type=2,norm='ortho')
    #mfccs = sklearn.preprocessing.scale(mfccs)
    print(np.shape(mfccs))
    normalized_mfcc[j] = librosa.util.normalize(mfccs) #-1~1
    mfcccs=normalized_mfcc[j]
    print(j)
    j=j+1
    #np.save(int(j),normalized_mfcc)
np.save("police",normalized_mfcc)