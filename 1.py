# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 22:24:06 2022

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 00:29:29 2022

@author: user
"""
import numpy as np
import pyaudio
import wave
import librosa
import matplotlib.pyplot as plt
import mfccs_value as mf
chunk = 1024                     # 記錄聲音的樣本區塊大小
sample_format = pyaudio.paInt16  # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1                     # 聲道數量
fs = 10240                       # 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
seconds = 5                      # 錄音秒數      # 錄音檔名

p = pyaudio.PyAudio()            # 建立 pyaudio 物件

print("開始錄音...")

# 開啟錄音串流
stream = p.open(format=sample_format, channels=channels, rate=fs,input_device_index = 1,input=True)
frames = [] 
j=0                     # 建立聲音串列
for i in np.arange(j,int(fs / chunk * 1)+j):
    data = stream.read(chunk) 
    frames.append(data)          # 將聲音記錄到串列中
    wf = wave.open(str(j+1)+".wav", 'wb')   # 開啟聲音記錄檔
    wf.setnchannels(channels)        # 設定聲道
    wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
    wf.setframerate(fs)              # 設定取樣頻率
    wf.writeframes(b''.join(frames)) # 存檔
    print("j:",j) 
    path=str(j+1)+".wav"
    #mf.displaymfccs(path)
    j+=1
    wf.close()
        
   



print('錄音結束...')
stream.stop_stream()             # 停止錄音
stream.close()                   # 關閉串流
p.terminate()