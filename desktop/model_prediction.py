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
from scipy import signal

# from keras.utils import to_categorical
import matplotlib.pyplot as plt
import warnings

labels = [
    "ambulance",
    "ambulance2",
    "ambulance3",
    "enviroment",
    # 'fire',
    "police1",
    "police2",
]
data_label = []
data_pred = []
data_db = []
warnings.simplefilter("ignore")
model = keras.models.load_model(
    "./models/simple_seperate_sec2_new2_retrain6_bandpassfilter100&50.hdf5"
)
model.summary()

for i in range(300):
    path = "test_audio/test" + "-" + str(i) + ".wav"
    data2, sr = librosa.load(path)
    print(type(data2[0]))
    b, a = signal.butter(8, [0.045, 0.272], "bandpass")
    y = signal.filtfilt(b, a, data2)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
    normalized_mfcc = librosa.util.normalize(mfccs)  # -1~1
    # img = librosa.display.specshow(normalized_mfcc,x_axis="time")
    mfcc_reshaped = normalized_mfcc.reshape(1, 13, 87, 1)
    # fig.colorbar(img, ax=ax)
    # plt.show()
    pred = model.predict(mfcc_reshaped)
    print(pred)
    pred = pred.reshape(5)
    # print(pred.shape)
    # a = tk.StringVar()  # 建立文字變數
    data_pred.append(pred)
    if pred[0] + pred[1] + pred[2] > 0.1:
        pred[0] = 1
    if pred[4] >= 0.3:
        pred[4] = 1
        pred[0] = pred[1] = pred[2] = 0
    np.save("prediction7.npy", data_pred)
    # print(pred)
    index = np.argmax(pred)
    # print(index)
    prediction = labels[index]
    print(prediction)  # 預測結果
