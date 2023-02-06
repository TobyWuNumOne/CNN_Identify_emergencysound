import wave
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.animation import FuncAnimation
import pyaudio
import time
import threading
from scipy.fftpack import fft, ifft, irfft
from threading import Lock, Thread
import codecs
import pyaudio
import wave
import librosa.display
import librosa
from keras.models import load_model
import keras
import mfccs_value as mf
import soundfile as sf


class Audiowave:
    def __init__(self):

        self.wavewidth = 2
        self.wavechannel = 1
        self.framerate = 22050
        self.fps = 24
        self.data = []
        self.frames = []
        self.path = "C:\\Users\\Administrator\\Documents\\GitHub\\CNN_Identify_emergencysound\\Toby\\soundfile\\"

        # self.fig, self.ax = plt.subplots(2, 1, figsize=(10, 8))
        # plt.subplot_tool()
        self.p = pyaudio.PyAudio()  # 實例化對象

        if self.wavewidth == 1:
            self.format = pyaudio.paInt8
        elif self.wavewidth == 2:
            self.format = pyaudio.paInt16
        elif self.wavewidth == 3:
            self.format = pyaudio.paInt24
        elif self.wavewidth == 4:
            self.format = pyaudio.paFloat32

        # fps=waveframerate/waveCHUNK #每秒數據更新次數
        self.waveCHUNK = 1024  # int(self.framerate / self.fps)

        self.stream = self.p.open(
            format=self.format,
            channels=self.wavechannel,
            rate=self.framerate,
            input=True,
            frames_per_buffer=self.waveCHUNK,
        )  # 錄音

    def micdata(self):  # 錄音數據
        self.data = self.stream.read(self.waveCHUNK)  # 錄音
        self.frames.append(self.data)

    def identify(self):
        time.sleep(0.5)
        count = 1
        for i in range(0, 19 * 22):

            if i == (44 * count):
                filepath = self.path + str(count) + ".wav"
                wf = wave.open(filepath, "wb")  # 開啟聲音記錄檔
                wf.setnchannels(self.wavechannel)  # 設定聲道
                wf.setsampwidth(self.p.get_sample_size(self.format))  # 設定格式
                wf.setframerate(self.framerate)  # 設定取樣頻率

                wf.writeframes(
                    b"".join(self.frames[int(22 * (count - 1)) : int(22 * count)])
                )  # 存檔

                wf.close()
                count = count + 0.5
                time.sleep(0.5)
                #self.resample(filepath)
                end_time=time.time()
                print(end_time-start_time)
                mf.displaymfccprediction(filepath)

        self.stream.stop_stream()  # 停止錄音
        self.stream.close()  # 關閉串流
        self.p.terminate()
        
        
        return print("錄音結束...")

    def mfcc(self):
        data, sr = librosa.load(self.path)
        mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
        normalized_mfcc = librosa.util.normalize(mfccs)
        return normalized_mfcc

    def resample(self, filepath):
        y, sr = librosa.load(filepath)
        y_8k = librosa.resample(y, sr, 8000)
        sf.write(filepath, y_8k, 8000)


a = Audiowave()


def recorder_run():
    while 1:
        a.micdata()


if __name__ == "__main__":
    start_time=time.time()
    t1 = threading.Thread(target=recorder_run, args=())
    t1.setDaemon(True)
    t1.start()
    mf.print_model()
    a.identify()
