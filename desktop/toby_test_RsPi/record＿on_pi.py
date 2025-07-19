# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:01:26 2022

@author: user
"""

import pyaudio
import wave

# import tkinter as tk
import time

# from keras.models import load_model
import librosa
import keras
import numpy as np
import os
import matplotlib.pyplot as plt
import librosa.display

# from scipy.io.wavfile import read
from scipy.fft import fft
from scipy import signal
import threading
import RPi.GPIO as GPIO

# import  soundfile as sf
# import math

chunk = 11025  # 記錄聲音的樣本區塊大小
# window = tk.Tk()
GPIO.setmode(GPIO.BCM)  # TODO
GPIO.setup(18, GPIO.OUT)  # 設定腳位
# 設定視窗標題
# window.title('alarm')
# window.geometry("600x180")
labels = [
    "ambulance",
    "ambulance2",
    "ambulance3",
    "enviroment",
    # 'fire',
    "police",
]
# nb50&20
data_pred = []
# warnings.simplefilter("ignore")
model = keras.models.load_model(
    "./models/simple-train-nb_sec2_highpass_seperate_50&20.hdf5"
)
# model     = keras.models.load_model("test.hdf5")
sample_format = (
    pyaudio.paInt16
)  # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1  # 聲道數量
fs = 22050
# 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
seconds = 1  # 錄音秒數
filename = "oxxostudio.wav"  # 錄音檔名

p = pyaudio.PyAudio()  # 建立 pyaudio 物件
# label_select=tk.Label(window)

# a = tk.StringVar()  # 建立文字變數
def output_thread():  # 還要更改腳位的位置
    for i in range(1, 10):
        # 在這裡進行輸出操作
        GPIO.output(18, GPIO.HIGH)
        # print("1")
        time.sleep(0.02)
        GPIO.output(18, GPIO.LOW)
        # print("0")
        time.sleep(0.02)


def displaySpectrum(path):  # 显示语音频域谱线
    sr = wave.open(path)
    # print(sr.getframerate())
    x, sr = librosa.load(path, sr=sr.getframerate())
    b, a = signal.butter(8, [0.045, 0.45], "bandpass")
    y = signal.filtfilt(b, a, x)
    # print(len(x))
    # ft = librosa.stft(x)
    # magnitude = np.abs(ft)  # 对fft的结果直接取模（取绝对值），得到幅度magnitude
    # frequency = np.angle(ft)  # (0, 16000, 121632)

    ft = fft(y)
    # print(len(ft), type(ft), np.max(ft), np.min(ft))
    magnitude = np.absolute(ft)  # 对fft的结果直接取模（取绝对值），得到幅度magnitude
    frequency = np.linspace(0, sr, len(magnitude))  # (0, 16000, 121632)

    # print(len(magnitude), type(magnitude), np.max(magnitude), np.min(magnitude))
    # print(len(frequency), type(frequency), np.max(frequency), np.min(frequency))

    plt.plot(frequency[:10000], magnitude[:10000])  # magnitude spectrum

    plt.title(count)
    plt.show()


def displaySpectrogram(path):

    x, sr = librosa.load(path)
    # compute power spectrogram with stft(short-time fourier transform):
    # 基于stft，计算power spectrogram
    spectrogram = librosa.amplitude_to_db(librosa.stft(x))

    print(len(x))
    # show
    librosa.display.specshow(spectrogram, x_axis="time", y_axis="hz")
    plt.colorbar(format="%+2.0f dB")

    plt.show()


def displaymfccprediction(path):

    data_label = []
    i = 0

    wf = wave.open(path, "r")
    rate = wf.getframerate()
    print(rate)
    data, sr = librosa.load(path)

    b, a = signal.butter(8, [0.045, 0.45], "bandpass")
    y = signal.filtfilt(b, a, data)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
    FILE = "D:\\voice_data\\" + str(i) + ".wav"
    # sf.write("D:\\voice_data\\"+str(i),y,22050,subtype='PCM_24')
    # mfccs = sklearn.preprocessing.scale(mfccs)
    # print(np.shape(mfccs))
    normalized_mfcc = librosa.util.normalize(mfccs)  # -1~1
    # normalized_mfcc=np.resize(normalized_mfcc,(13,44))
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

    if (pred[0] + pred[1] + pred[2]) >= 0.50 and pred[4] >= 0.5:
        print("ambulance&police")
        t = threading.Thread(target=output_thread)
        t.start()
        """
        label_url=tk.Label(window,textvariable=a, font=('Arial', 40))
        a.set('ambulance&police') 
        label_url.place(x=0,y=0)    
        """
        return
    """
    elif (pred[0]+pred[1]+pred[2])>=0.33:
        pred[0]=1
                
            #if i[2]>=0.15:
                #i[2]=1
     
    """
    np.save("prediction.npy", data_pred)
    index = np.argmax(pred)
    print(index)
    prediction = labels[index]
    print(prediction)  # 預測結果
    # a.set(prediction)
    # label_url=tk.Label(window,textvariable=a, font=('Arial', 40))
    # label_url.place(x=0,y=0)
    data_label.append(prediction)
    np.save("label.npy", data_label)


def cut():

    filepath = path + str(count) + ".wav"
    wf = wave.open(filepath, "wb")  # 開啟聲音記錄檔
    wf.setnchannels(channels)  # 設定聲道
    wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
    wf.setframerate(fs)  # 設定取樣頻率
    wf.writeframes(b"".join(frames[int(4 * (count - 1)) : int((4 * count))]))  # 存檔
    wf.close()

    displaymfccprediction(filepath)

    # displaySpectrum(filepath)

    # displaySpectrogram(filepath)
    # os.remove(filepath)


print("開始錄音...")
path = "./testwav/"

# 開啟錄音串流
count = 1
number = 0
stream = p.open(
    format=sample_format,
    channels=channels,
    rate=fs,
    frames_per_buffer=chunk,
    input=True,
    # input_device_index = 1
)

frames = []


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
start_time = time.time()
frames = []
# while(count==26.0):
for i in range(1000):
    # frames = []
    # print(labels)
    # label_url=tk.Label(window,textvariable=a, font=('Arial', 40))
    # label_url.place(x=0,y=0)
    # a.set("                                                                                 ")
    for i in range(0, 4):
        data = stream.read(chunk)
        frames.append(data)

        # print(len(frames))
        # print(end_time-start_time)
        if len(frames) == count * 4:
            # label_url=tk.Label(window,text=" ", font=('Arial', 24))
            end_time = time.time()
            # print(end_time-start_time)
            cut()
            # print("第",number,"到第",number+2,"秒音檔")
            count = count + 0.5
            number = number + 1
            # window.update()
            # print(count)
    # print(len(frames))
stream.stop_stream()  # 停止錄音
stream.close()  # 關閉串流
p.terminate()
# break
print("錄音結束...")
# window.mainloop()
