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
import wave
from keras.models import load_model
import librosa.display
import numpy as np
import keras
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(BASE_DIR)


def displaymfccs(path):
    filepath = path
    data, sr = librosa.load(filepath)
    print(len(data))
    # plt.plot(data)
    mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
    # mfccs = sklearn.preprocessing.scale(mfccs)
    normalized_mfcc = librosa.util.normalize(mfccs)
    fig, ax = plt.subplots()
    print(normalized_mfcc.shape)
    # img = librosa.display.specshow(normalized_mfcc, x_axis="time", ax=ax)
    # fig.colorbar(img, ax=ax)
    # plt.show()


def displaySpectrogram(path):

    filepath = path
    x, sr = librosa.load(filepath)
    # compute power spectrogram with stft(short-time fourier transform):
    # 基于stft，计算power spectrogram
    spectrogram = librosa.amplitude_to_db(librosa.stft(x))

    print(len(x))
    # show
    librosa.display.specshow(spectrogram, y_axis="log")
    plt.colorbar(format="%+2.0f dB")

    plt.show()


def displaymfccprediction(path):

    labels = [
        "ambulance",
        "enviroment",
        #'fire',
        "police",
    ]
    data_label = []
    data_pred = []
    # warnings.simplefilter("ignore")
    model = keras.models.load_model("./models/simple-train-nb1.hdf5")
    data, sr = librosa.load(path)

    wf = wave.open(path, "r")
    rate = wf.getframerate()
    print(rate)
    # print(sr)

    fig, ax = plt.subplots()
    mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
    # mfccs = sklearn.preprocessing.scale(mfccs)
    # print(np.shape(mfccs))
    normalized_mfcc = librosa.util.normalize(mfccs)  # -1~1
    # print(normalized_mfcc.shape)
    normalized_mfcc = np.resize(normalized_mfcc, (13, 44))

    # img = librosa.display.specshow(normalized_mfcc, x_axis="time")

    mfcc_reshaped = normalized_mfcc.reshape(1, 13, 44, 1)

    # fig.colorbar(img, ax=ax)

    # plt.show()
    pred = model.predict(mfcc_reshaped)
    # print(pred)
    data_pred.append(pred)
    """if pred[0,0]<=0.99 and pred[0,2]<=0.99:
        pred[0,1]=1"""
    # print(pred)
    index = np.argmax(pred)
    prediction = labels[index]
    print(prediction)  # 預測結果
    data_label.append(prediction)
    # os.remove(path)
