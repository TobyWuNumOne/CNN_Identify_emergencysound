# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:01:26 2022

@author: user
"""
import pyaudio
import wave
import tkinter as tk
import time
from keras.models import load_model
import librosa
import keras
import numpy as np
import os
import matplotlib.pyplot as plt
import librosa.display
from scipy.io.wavfile import read
from scipy.fft import fft
from scipy import signal
import scipy.io.wavfile
import  soundfile as sf
import math
chunk = 11025 
labels = [
        'ambulance',
        'ambulance2',
        'ambulance3',
        "enviroment",
        # 'fire',
        'police1',
        'police2'
        ]    
data_label=[]     
data_pred=[]
data_db=[]

#models\\simple_seperate_sec2_new2_retrain5_bandpassfilter50&30.hdf5 音檔未分開
#models\\simple_seperate_sec2_new2_retrain6_bandpassfilter100&50.hdf5 音檔分開可用
#7_200&65
model     = keras.models.load_model("models\\simple_seperate_sec2_new2_retrain6_bandpassfilter100&50.hdf5")
sample_format = (    
    pyaudio.paInt16
)  
# 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1  # 聲道數量
fs =22050
# 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
seconds = 1  # 錄音秒數
p = pyaudio.PyAudio()  # 建立 pyaudio 物件
def displaySpectrum(path): 
    #print(sr.getframerate())
    sr,x=scipy.io.wavfile.read(path)
    #print(db)
    #x, sr = librosa.load(path,sr=sr.getframerate())
    b,a=signal.butter(8,[0.045,0.272],'bandpass')
    y = signal.filtfilt(b, a, x)
    #print(len(x))
    # ft = librosa.stft(x)
    # magnitude = np.abs(ft) 
    # frequency = np.angle(ft) 
    ft = fft(y)
    #print(len(ft), type(ft), np.max(ft), np.min(ft))
    magnitude = np.absolute(ft)
    frequency = np.linspace(0, sr, len(magnitude))  # (0, 16000, 121632)
    plt.plot(frequency[:10000], magnitude[:10000])  # magnitude spectrum
    plt.show()
def displaySpectrogram(path):     
    x, sr = librosa.load(path)
    spectrogram = librosa.amplitude_to_db(librosa.stft(x))
    print(len(x))
    librosa.display.specshow(spectrogram, x_axis="time",y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.show()
def displaymfccprediction(path):      
    data2, sr = librosa.load(path)
    print(type(data2[0]))
    b,a=signal.butter(8,[0.045,0.272],'bandpass')
    y = signal.filtfilt(b, a, data2)
    mfccs = librosa.feature.mfcc(y=y, sr=sr,n_mfcc=13,dct_type=2,norm='ortho')
    normalized_mfcc = librosa.util.normalize(mfccs) #-1~1
    #img = librosa.display.specshow(normalized_mfcc,x_axis="time") 
    mfcc_reshaped = normalized_mfcc.reshape(1, 13,87, 1)
    #fig.colorbar(img, ax=ax)
    #plt.show()
    pred = model.predict(mfcc_reshaped)
    print(pred)
    pred=pred.reshape(5)
    #print(pred.shape)   
    #a = tk.StringVar()  # 建立文字變數
    data_pred.append(pred)
    if(pred[0]+pred[1]+pred[2]>0.1):
        pred[0]=1
    if(pred[4]>=0.3):
        pred[4]=1
        pred[0]=pred[1]=pred[2]=0
    np.save("prediction7.npy",data_pred)
    #print(pred)
    index = np.argmax(pred)
    #print(index)
    prediction = labels[index]
    print(prediction) # 預測結果
    
    #a.set(prediction)
    #label_url=tk.Label(window,textvariable=a, font=('Arial', 40))
    #label_url.place(x=0,y=0)     
    data_label.append(prediction)
    np.save("label7.npy",data_label)
def cut():
    #frame=[]
    filepath = path + str(number) + ".wav"
    wf = wave.open(filepath, "wb")  # 開啟聲音記錄檔
    wf.setnchannels(channels)  # 設定聲道
    wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
    wf.setframerate(fs)  # 設定取樣頻率
    #frame=frames[int(4*(count-1)):int((4*count))]
    wf.writeframes(b"".join(frames[int(4*(count-1)):int((4*count))]))  # 存檔
    wf.close()
    displaymfccprediction(filepath)
    #displaySpectrum(filepath)
    #displaySpectrogram(filepath)
    #os.remove(filepath)
print("開始錄音...")
path = "D:\\voice_data\\test2\\"
    # 開啟錄音串流
count = 1
number=0
stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
    )
frames = []
#start_time=time.time()
frames = []
number_p=0
for i in range(1000):
    start_time=time.time()
    #frames = []
   #print(labels)
    #label_url=tk.Label(window,textvariable=a, font=('Arial', 40))
    #label_url.place(x=0,y=0)  
    #a.set("                                                                                 ")
#for i in range(0,4):
    data = stream.read(chunk)
    frames.append(data) 
        #print(len(frames))
        #print(end_time-start_time)
    if(len(frames)==count*4):
            #label_url=tk.Label(window,text=" ", font=('Arial', 24))
            #end_time=time.time()
            #print(end_time-start_time)
        cut()
        end_time=time.time()
        print(end_time-start_time)
        count = count + 0.5
        number=number+1
            #window.update()
            #print(count)
    #print(len(frames))
stream.stop_stream()  # 停止錄音
stream.close()  # 關閉串流
p.terminate()

print("錄音結束...")
#window.mainloop()

