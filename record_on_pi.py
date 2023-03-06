# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:01:26 2022

@author: user
"""
import pyaudio
import wave
import time
import librosa
import keras
import numpy as np
import os

# import matplotlib.pyplot as plt
import librosa.display
from scipy import signal
import threading
import RPi.GPIO as GPIO

# from scipy.io.wavfile import read
# from keras.models import load_model
# import  soundfile as sf
# import math
# import tkinter as tk

# SETTING
labels = [
    "ambulance",
    "ambulance2",
    "ambulance3",
    "enviroment",
    # 'fire',
    "police",
]
frames = []
data_pred = []
chunk = 11025  # 記錄聲音的樣本區塊大小
channels = 1  # 聲道數量
fs = 22050
count = 1
path = "./a/"  # TODO
GPIO.setmode(GPIO.BCM)  # 設定腳位
GPIO.setup(18, GPIO.OUT)  # 設定腳位
GPIO.setup(23, GPIO.OUT)  # 設定腳位
model = keras.models.load_model(
    "./models/simple-train-nb_sec2_highpass_seperate_50&20.hdf5"  # TODO
)
sample_format = pyaudio.paInt16


def output_police():  # 還要更改腳位的位置 #控制ＬＥＤ燈亮
    for i in range(1, 10):
        # 在這裡進行輸出操作
        GPIO.output(18, GPIO.HIGH)
        time.sleep(0.03)
        GPIO.output(18, GPIO.LOW)
        time.sleep(0.03)


def output_ambulance():  # 還要更改腳位的位置 #控制ＬＥＤ燈亮
    for i in range(1, 10):
        # 在這裡進行輸出操作
        GPIO.output(23, GPIO.HIGH)
        time.sleep(0.03)
        GPIO.output(23, GPIO.LOW)
        time.sleep(0.03)


def displaymfccprediction(path):
    wf = wave.open(path, "r")
    rate = wf.getframerate()
    print(rate)
    data, sr = librosa.load(path)
    b, a = signal.butter(8, [0.045, 0.45], "bandpass")
    y = signal.filtfilt(b, a, data)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
    normalized_mfcc = librosa.util.normalize(mfccs)  # -1~1
    mfcc_reshaped = normalized_mfcc.reshape(1, 13, 87, 1)
    pred = model.predict(mfcc_reshaped)
    print(pred)
    pred = pred.reshape(5)
    data_pred.append(pred)
    if (pred[0] + pred[1] + pred[2]) >= 0.50 and pred[4] >= 0.5:
        print("ambulance&police")
    index = np.argmax(pred)
    print(index)
    prediction = labels[index]
    print(prediction)  # 預測結果
    if prediction == "police":
        pol = threading.Thread(target=output_police)
        pol.start()
    elif prediction == "police":
        a = threading.Thread(target=output_ambulance)
        a.start()
    os.remove(path)


def cut(path):
    filepath = path + str(count) + ".wav"
    wf = wave.open(filepath, "wb")  # 開啟聲音記錄檔
    wf.setnchannels(channels)  # 設定聲道
    wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
    wf.setframerate(fs)  # 設定取樣頻率
    wf.writeframes(b"".join(frames[int(4 * (count - 1)) : int((4 * count))]))  # 存檔
    wf.close()
    return filepath
    # displaySpectrum(filepath)
    # displaySpectrogram(filepath)


print("開始錄音...")


p = pyaudio.PyAudio()  # 建立 pyaudio 物件
stream = p.open(  # 開啟錄音串流
    format=sample_format,
    channels=channels,
    rate=fs,
    frames_per_buffer=chunk,
    input=True,
    # input_device_index = 1
)

"""
while(1):   
    data = stream.read(chunk)
    frames.append(data)
    #print(len(frames))
    end_time=time.time()
    print(end_time-start_time)
        # 將聲音記錄到串列中
        #print(i)
    if len(frames) == 100*count:
        print(count)
        cut()
        count = count + 0.5
"""

for i in range(1000):
    for i in range(0, 4):
        data = stream.read(chunk)
        frames.append(data)
        if len(frames) == count * 4:
            filepath = cut(path)  # 切割
            displaymfccprediction(filepath)  # 辨識
            count = count + 0.5
stream.stop_stream()  # 停止錄音
stream.close()  # 關閉串流
p.terminate()
print("錄音結束...")
