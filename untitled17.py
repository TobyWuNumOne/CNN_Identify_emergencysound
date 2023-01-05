# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 22:58:28 2022

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 22:20:11 2022

@author: liuch
"""
import contextlib
import numpy as np
import pyaudio
import wave
import librosa
import matplotlib.pyplot as plt
import mfccs_value as mf
chunk = 1024                     # 記錄聲音的樣本區塊大小
sample_format = pyaudio.paInt16  # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1                     # 聲道數量
fs = 22050                      # 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
seconds = 5                      # 錄音秒數
filename = "oxxostudio.wav"      # 錄音檔名

p = pyaudio.PyAudio()            # 建立 pyaudio 物件
p2= pyaudio.PyAudio()   
print("開始錄音...")

# 開啟錄音串流
stream = p.open(format=sample_format, channels=channels, rate=fs,input_device_index = 1,input=True)

frames = []      

                # 建立聲音串列
for k in np.arange (0,50,1):
    if k==0:
        for i in np.arange(k,int(fs / chunk * 1)+k):
         data = stream.read(chunk) 
         frames.append(data)          # 將聲音記錄到串列中
         wf = wave.open(str(k)+".wav", 'wb')   # 開啟聲音記錄檔
         wf.setnchannels(channels)        # 設定聲道
         wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
         wf.setframerate(fs)              # 設定取樣頻率
         wf.writeframes(b''.join(frames)) # 存檔
         wf.close()
    if k!=0:
        del frames[0:2]
        for i in np.arange(k,int(fs / chunk * 1)+k-2):
            data = stream.read(chunk) 
            frames.append(data)          # 將聲音記錄到串列中
            wf = wave.open(str(k)+".wav", 'wb')   # 開啟聲音記錄檔
            wf.setnchannels(channels)        # 設定聲道
            wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
            wf.setframerate(fs)              # 設定取樣頻率
            wf.writeframes(b''.join(frames)) # 存檔
            wf.close()
    path=str(k)+'.wav'
    data,sr=librosa.load(path)
    #plt.plot(data)
    mf.displaymfccprediction(path)

print('錄音結束...')

stream.stop_stream()             # 停止錄音
stream.close()                   # 關閉串流
p.terminate()
