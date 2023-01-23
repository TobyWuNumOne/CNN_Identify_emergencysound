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
import librosa.display
from matplotlib import cm


class Audiowave:
    def __init__(self):

        self.wavedata = []
        self.wavewidth = 2
        self.wavechannel = 1
        self.framerate = 48000
        self.fps = 1
        self.Timedata = []
        self.nframes = 0
        self.N = 0
        self.data = []
        self.path = "./a/1.wav"

        self.fig, self.ax = plt.subplots(1, 1, figsize=(10, 8))
        # plt.subplot_tool()
        self.p = pyaudio.PyAudio()  # 實例化對象

        if self.wavewidth == 1:
            format = pyaudio.paInt8
        elif self.wavewidth == 2:
            format = pyaudio.paInt16
        elif self.wavewidth == 3:
            format = pyaudio.paInt24
        elif self.wavewidth == 4:
            format = pyaudio.paFloat32

        # fps=waveframerate/waveCHUNK #每秒數據更新次數
        self.waveCHUNK = int(self.framerate / self.fps)

        self.stream = self.p.open(
            format=format,
            channels=self.wavechannel,
            rate=self.framerate,
            input=True,
            frames_per_buffer=self.waveCHUNK,
        )  # 錄音

        # self.stream1 = self.q.open(
        #     format=format,
        #     channels=self.wavechannel,
        #     rate=self.framerate,
        #     output=True,
        #     frames_per_buffer=self.waveCHUNK,
        # )  # 播放

        self.c = 0
        self.a = time.time()
        self.b = 0
        self.x = []
        self.y = []
        self.fft_int = []

        np.array(self.x)
        np.array(self.y)

        self.wf = wave.open(r"D:\pythonProject2\wav\test.wav", "wb")
        self.wf.setnchannels(self.wavechannel)  # 聲道設置
        self.wf.setsampwidth(self.p.get_sample_size(format))  # 採樣位數設置
        self.wf.setframerate(self.framerate)

        self.wf1 = wave.open(r"D:\pythonProject2\wav\test1.wav", "wb")
        self.wf1.setnchannels(self.wavechannel)  # 聲道設置
        self.wf1.setsampwidth(self.p.get_sample_size(format))  # 採樣位數設置
        self.wf1.setframerate(self.framerate)

    def to_fft(self, N, data):  # 轉換為頻域數據，並進行取半、歸一化等處理
        # N=self.nframes #取樣點數
        df = self.framerate / (
            N - 1
        )  # 每個點分割的頻率如果你採樣頻率是4096，你FFT以後頻譜是從-2048到+2048hz（4096除以2），然後你的1024個點均勻分佈，相當於4個HZ你有一個點，那個複數的模就對應了頻譜上的高度
        freq = [df * n for n in range(0, N)]

        wave_data2 = data[0:N]
        self.fft_int = np.fft.fft(wave_data2)
        # print(N, len(data),len(wave_data2))
        c = self.fft_int * 2 / N  # *2能量集中化/N歸一化
        d = int(len(c) / 2)  # 對稱取半
        freq = freq[: d - 1]
        fredata = abs(c[: d - 1])

        return freq, fredata

    def wavehex_to_DEC_n(self, wavedata, wavewidth, wavechannel):  # 錄音存儲數據十六進制數據轉換十進制
        # print("#####################")
        Timedata = []

        # print(type(self.Timedata))
        n = int(len(wavedata) / wavewidth)
        i = 0
        j = 0
        for i in range(0, n):
            b = 0
            for j in range(0, wavewidth):
                temp = wavedata[i * wavewidth : (i + 1) * wavewidth][j] * int(
                    math.pow(2, 8 * j)
                )
                b += temp
            if b > int(math.pow(2, 8 * wavewidth - 1)):
                b = b - int(math.pow(2, 8 * wavewidth))
            Timedata.append(b)
        Timedata = np.array(Timedata)
        # print(len(self.Timedata))
        Timedata.shape = -1, wavechannel
        Timedata = Timedata.T
        x = np.linspace(0, len(Timedata[0]) - 1, len(Timedata[0])) / self.framerate

        return x, Timedata

    def micdata(self):  # 錄音數據，存儲，播放
        data = self.stream.read(self.waveCHUNK)  # 錄音
        self.data = data

    def Dynamic_micwave_init(self):  # 動態顯示圖像-初始化圖像

        self.ax.set_xlim(0, 1)

        normalized_mfcc = self.mfcc()
        (lm,) = self.ax.imshow(
            normalized_mfcc, interpolation="nearest", cmap=cm.coolwarm, origin="lower"
        )
        return (lm,)  # 返回曲線

    def mfcc(self):
        data, sr = librosa.load(self.path)
        mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
        normalized_mfcc = librosa.util.normalize(mfccs)

        return normalized_mfcc

    def Dynamic_micwave_update(self, n):  # 動態顯示圖像-更新圖像

        normalized_mfcc = self.mfcc()
        (lm,) = self.ax.imshow(
            normalized_mfcc, interpolation="nearest", cmap=cm.coolwarm, origin="lower"
        )
        return (lm,)

    def Dynamic_micwave_run(self):  # 動態顯示圖像

        ani = FuncAnimation(
            self.fig,
            self.Dynamic_micwave_update,
            interval=1000 / self.fps,
            init_func=self.Dynamic_micwave_init,
            blit=True,
        )
        plt.show()


a = Audiowave()


def recorder_run():
    while True:
        a.micdata()


# def draw_run():
#     a.Dynamic_micwave_run()


#
#
if __name__ == "__main__":
    t1 = threading.Thread(target=recorder_run, args=())
    # target是要執行的函數名（不是函數），args是函數對應的參數，以元組的形式存在
    # t2 = threading.Thread(target=draw_run,args=())
    # t2.setDaemon(True)
    t1.setDaemon(True)
    t1.start()
    a.Dynamic_micwave_run()
