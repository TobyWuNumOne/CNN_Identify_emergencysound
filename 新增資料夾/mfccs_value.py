# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 18:12:05 2022

@author: user
"""
import os
import wave
import numpy as np
import pylab as plt
import librosa.display
import matplotlib.pyplot as plt
import sklearn
import numpy
def displaymfccs(path):   
    filepath=path
    data, sr = librosa.load(filepath)
    print(sr)
    mfccs = librosa.feature.mfcc(y=data, sr=sr,n_mfcc=13,dct_type=2,norm='ortho')
    #mfccs = sklearn.preprocessing.scale(mfccs)
    normalized_mfcc = librosa.util.normalize(mfccs)
    fig, ax = plt.subplots()
    img = librosa.display.specshow( normalized_mfcc,x_axis="time",ax=ax) 
    fig.colorbar(img, ax=ax)
    plt.show()

def displaySpectrogram(path,number):
    for i in range(2,number):
        filepath=path+str(i)+".wav"
        x, sr = librosa.load(filepath, sr=8000)
    # compute power spectrogram with stft(short-time fourier transform):
    # 基于stft，计算power spectrogram
        spectrogram = librosa.amplitude_to_db(librosa.stft(x))
        
        print(len(x))
        # show
        librosa.display.specshow(spectrogram, y_axis='log')
        plt.colorbar(format='%+2.0f dB')
       
        plt.show()