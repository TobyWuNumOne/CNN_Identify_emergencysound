# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:01:26 2022

@author: user
"""

import pyaudio
import wave

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
chunk = 11025 # 記錄聲音的樣本區塊大小

labels = [
            'ambulance',
            "enviroment",
            #'fire',
            'police'
    ]       
            

    #warnings.simplefilter("ignore")
model     = keras.models.load_model("models\\simple-train-nb50&20.hdf5")
sample_format = (
    pyaudio.paInt16
)  # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1  # 聲道數量
fs =22050
# 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
seconds = 1  # 錄音秒數
filename = "oxxostudio.wav"  # 錄音檔名

p = pyaudio.PyAudio()  # 建立 pyaudio 物件
def displaySpectrum(path): # 显示语音频域谱线
    sr=wave.open(path)
    print(sr.getframerate())
    x, sr = librosa.load(path,sr=sr.getframerate())
    print(len(x))
    # ft = librosa.stft(x)
    # magnitude = np.abs(ft)  # 对fft的结果直接取模（取绝对值），得到幅度magnitude
    # frequency = np.angle(ft)  # (0, 16000, 121632)

    ft = fft(x)
    #print(len(ft), type(ft), np.max(ft), np.min(ft))
    magnitude = np.absolute(ft)  # 对fft的结果直接取模（取绝对值），得到幅度magnitude
    frequency = np.linspace(0, sr, len(magnitude))  # (0, 16000, 121632)

    #print(len(magnitude), type(magnitude), np.max(magnitude), np.min(magnitude))
    #print(len(frequency), type(frequency), np.max(frequency), np.min(frequency))

    plt.plot(frequency[:], magnitude[:])  # magnitude spectrum

    plt.show()

    # # plot spectrum，不限定 [对称]
    # plt.figure(figsize=(18, 8))
    # plt.plot(frequency, magnitude)  # magnitude spectrum
    # plt.title("语音信号频域谱线")
    # plt.xlabel("频率（赫兹）")
    # plt.ylabel("幅度")
    # plt.show()

def displaySpectrogram(path):     
    
        x, sr = librosa.load(path)
    # compute power spectrogram with stft(short-time fourier transform):
    # 基于stft，计算power spectrogram
        spectrogram = librosa.amplitude_to_db(librosa.stft(x))
        
        print(len(x))
        # show
        librosa.display.specshow(spectrogram, x_axis="time",y_axis='log')
        plt.colorbar(format='%+2.0f dB')
       
        plt.show()
def displaymfccprediction(path):
            
    data_label=[]
    data_pred=[]
    
    wf=wave.open(path,"r")
    rate=wf.getframerate()
    print(rate)
    data, sr = librosa.load(path)
    #print(len(data))
    #print(sr)
    #plt.plot(data2)
    #plt.show()
    wf.close()
    mfccs = librosa.feature.mfcc(y=data, sr=sr,n_mfcc=13,dct_type=2,norm='ortho')

    #mfccs = sklearn.preprocessing.scale(mfccs)
    #print(np.shape(mfccs))
    normalized_mfcc = librosa.util.normalize(mfccs) #-1~1
    #normalized_mfcc=np.resize(normalized_mfcc,(13,44))
    img = librosa.display.specshow(normalized_mfcc,x_axis="time") 
    mfcc_reshaped = normalized_mfcc.reshape(1, 13, 44, 1)
    #fig.colorbar(img, ax=ax)

    plt.show()
    pred = model.predict(mfcc_reshaped)
    print(pred)       
    data_pred.append(pred)
    index = np.argmax(pred)
    prediction = labels[index]
    print(prediction) # 預測結果
    data_label.append(prediction)
    #os.remove(path)
    
def cut():
    
    filepath = path + str(count) + ".wav"
    wf = wave.open(filepath, "wb")  # 開啟聲音記錄檔
    wf.setnchannels(channels)  # 設定聲道
    wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
    wf.setframerate(fs)  # 設定取樣頻率
    wf.writeframes(b"".join(frames[int(2*(count-1)):int((2*count))]))  # 存檔
    wf.close()
    
   
    displaymfccprediction(filepath)
    #displaySpectrum(filepath)
    displaySpectrogram(filepath)

print("開始錄音...")

path = "./a/"

    # 開啟錄音串流
count = 1
start_time=time.time()
stream = p.open(
        format=sample_format,
        channels=channels,
        rate=fs,
        frames_per_buffer=chunk,
        input=True,
        #input_device_index = 1
    )

frames = []
j = 0
#def main()
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
frames = []
while(count!=5):
    #frames = []
    for i in range(0,4):
        data = stream.read(chunk)
        frames.append(data)
        
        #print(len(frames))
        #print(end_time-start_time)
        if(len(frames)==count*2):
            end_time=time.time()
            print(end_time-start_time)
            cut()
            count = count + 0.5
    #print(len(frames))
stream.stop_stream()  # 停止錄音
stream.close()  # 關閉串流
p.terminate()
#break
print("錄音結束...")

