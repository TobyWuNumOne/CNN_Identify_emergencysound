# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 23:27:29 2022

@author: user
"""

from keras.models import load_model
import librosa.display
import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
#from keras.utils import to_categorical
import matplotlib.pyplot as plt
import warnings

labels = [
        'ambulance',
        "enviroment",
        #'fire',
        'police'
       
        
    ]
data_label=[]
data_pred=[]
warnings.simplefilter("ignore")
model     = keras.models.load_model("C:\\Users\\user\\Desktop\\0103\\voice_data\\models\\simple-train-nb9.hdf5")
model.summary()

for i in range(300):
    path="C:\\Users\\user\\Desktop\\0103\\"+str(i)+".wav"
    #path="C:\\Users\\user\\Desktop\\0103\\voice_data\\test\\10-"+str(i)+".wav"
    data, sr = librosa.load(path)
    print(len(data))
    #print(sr)
    #fig, ax = plt.subplots()
    mfccs = librosa.feature.mfcc(y=data, sr=sr,n_mfcc=13,dct_type=2,norm='ortho')
    #mfccs = sklearn.preprocessing.scale(mfccs)
    #print(np.shape(mfccs))
    normalized_mfcc = librosa.util.normalize(mfccs) #-1~1
    #img = librosa.display.specshow(normalized_mfcc,x_axis="time") 
    mfcc_reshaped = normalized_mfcc.reshape(1, 13, 44, 1)
    #fig.colorbar(img, ax=ax)
    print(i)
    plt.show()
    pred = model.predict(mfcc_reshaped)
    print(pred)
    data_pred.append(pred)
    if pred[0,0]<=0.99 and pred[0,2]<=0.99:
        pred[0,1]=1
    print(pred)
    index = np.argmax(pred)
    prediction = labels[index]
    print(prediction) # 預測結果
    data_label.append(prediction)