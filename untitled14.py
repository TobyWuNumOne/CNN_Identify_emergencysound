# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 17:07:21 2022

@author: user
"""

import os
import wave
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
import sklearn
import numpy
from mfccs_value import *
CutTimeDef = 1 #以1s截斷檔案
# CutFrameNum =0
#path=r"C:\Users\user\Desktop\wav2"
files = ['police\\police_1.wav']
for file in files:
    print (file)
    
def SetFileName(WavFileName):
    for i in range(len(files)*10):
        FileName = files[i]
        print("SetFileName File Name is ", FileName)
        FileName = WavFileName;

def CutFile():
    for i in range(len(files)):
        FileName = files[i]
        print("CutFile File Name is ",FileName)
        f = wave.open(r"" + FileName, "rb")
        params = f.getparams()
        #print(params)
        print("================")
        nchannels, sampwidth, framerate, nframes = params[:4]
        CutFrameNum = framerate * CutTimeDef
        #print("CutFrameNum=%d" % (CutFrameNum))
        #print("nchannels=%d" % (nchannels))
        #print("sampwidth=%d" % (sampwidth))
        print("framerate=%d" % (framerate))#採樣頻率
        print("nframes=%d" % (nframes))#總偵數
        #nframe/framerate=時長
        str_data = f.readframes(nframes)
        #f.close()# 將波形資料轉換成陣列
        print("===================")
        Cutnum =nframes/framerate
        print(Cutnum)
        
        wave_data = np.fromstring(str_data, dtype=np.short)
        wave_data.shape = -1, 2
        wave_data = wave_data.T
        temp_data = wave_data.T
        # StepNum = int(nframes/200)
        StepNum = int(CutFrameNum/10)
        print(StepNum)
        print(nframes)
        StepTotalNum = 0;
        haha = 0
        i=0
        #while StepTotalNum < nframes:
        for j in range(0,int(Cutnum*10),3):
            
            print("Stemp=%d" % (j))
            #print(files[i])
            print(Cutnum)
            FileName ="test" +"-"+ str(i) + ".wav"
           
            print(FileName)
            print("===============")
            temp_dataTemp = temp_data[StepNum*j : StepNum*(j+10)]
            #plt.plot(temp_dataTemp)
            #plt.show()
            #temp_dataTemp = temp_data[StepNum *(moveframenum+(haha)):StepNum *(moveframenum+(haha+1))]
            #haha = haha + 1;
            StepTotalNum = haha * nframes;
            temp_dataTemp.shape = -1, 2
            temp_dataTemp = temp_dataTemp.astype(np.short)# 開啟WAV文件
            f = wave.open(FileName, "wb")
            print(StepTotalNum)
            f.setnchannels(nchannels)
            f.setsampwidth(sampwidth)
            f.setframerate(framerate)
            f.writeframes(temp_dataTemp.tostring())
            f.close()
            displaymfccs(FileName)
            i+=1
            #displaySpectrogram(FileName)
            os.remove(FileName)
if __name__ == '__main__' :
    print("Run")
    CutFile()
    print("Run Over")