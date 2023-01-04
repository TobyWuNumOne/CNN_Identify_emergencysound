# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 14:01:26 2022

@author: user
"""

import pyaudio
import wave
import mfccs_value as mf
chunk = 1024                     # 記錄聲音的樣本區塊大小
sample_format = pyaudio.paInt16  # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1                     # 聲道數量
fs = 45057
                       # 取樣頻率，常見值為 44100 ( CD )、48000 ( DVD )、22050、24000、12000 和 11025。
seconds = 1                      # 錄音秒數
filename = "oxxostudio.wav"      # 錄音檔名

p = pyaudio.PyAudio()            # 建立 pyaudio 物件

print("開始錄音...")
while(1):
# 開啟錄音串流
    count=1
   
    stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
    frames = []  
    j=0
    for i in range(0,2200):
        data = stream.read(chunk)
        frames.append(data)
          # 將聲音記錄到串列中
          
        if i==(44*count):
             wf = wave.open(str(count)+".wav", 'wb')   # 開啟聲音記錄檔
             wf.setnchannels(channels)        # 設定聲道
             wf.setsampwidth(p.get_sample_size(sample_format))  # 設定格式
             wf.setframerate(fs)              # 設定取樣頻率
             wf.writeframes(b''.join(frames[int(44*(count-1)):int(44*count)])) # 存檔
             wf.close()
             path=str(count)+".wav"
             count=count+0.5
             mf.displaymfccs(path)
    """stream.stop_stream()             # 停止錄音
    stream.close()                   # 關閉串流
    p.terminate()"""
    print('錄音結束...')
    