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
from keras.models import load_model
import keras
import mfccs_value as mf


class Audiowave:
    def __init__(self):

        self.wavewidth = 2
        self.wavechannel = 1
        self.framerate = 22050
        self.fps = 24
        self.data = []
        self.frames = []
        self.path = "./Toby/soundfile/"

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

        self.c = 0
        self.a = time.time()
        self.b = 0
        self.x = []
        self.y = []
        self.fft_int = []

        np.array(self.x)
        np.array(self.y)

        # self.wf = wave.open(r"D:\pythonProject2\wav\test.wav", "wb")
        # self.wf.setnchannels(self.wavechannel)  # 聲道設置
        # self.wf.setsampwidth(self.p.get_sample_size(format))  # 採樣位數設置
        # self.wf.setframerate(self.framerate)

        # self.wf1 = wave.open(r"D:\pythonProject2\wav\test1.wav", "wb")
        # self.wf1.setnchannels(self.wavechannel)  # 聲道設置
        # self.wf1.setsampwidth(self.p.get_sample_size(format))  # 採樣位數設置
        # self.wf1.setframerate(self.framerate)

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

    def micdata(self):  # 錄音數據
        self.data = self.stream.read(self.waveCHUNK)  # 錄音
        self.frames.append(self.data)

    def Dynamic_micwave_init(self):  # 動態顯示圖像-初始化圖像
        self.ax[0].set_xlim(0, 1 / self.fps)
        self.ax[1].set_xlim(0, 2000)
        (ln,) = self.ax[0].plot([], [], animated=False)
        return (ln,)  # 返回曲線

    def Dynamic_micwave_update(self, n):  # 動態顯示圖像-更新圖像
        x, y = self.wavehex_to_DEC_n(self.data, self.wavewidth, self.wavechannel)
        fre_x, fre_y = self.to_fft(self.waveCHUNK, y[0])
        (ln,) = self.ax[0].plot(x, y[0], "g-")
        (ln1,) = self.ax[1].plot(fre_x, fre_y, "g-")
        return (
            ln,
            ln1,
        )

    def Dynamic_micwave_run(self):  # 動態顯示圖像

        ani = FuncAnimation(
            self.fig,
            self.Dynamic_micwave_update,
            interval=1000 / self.fps,
            init_func=self.Dynamic_micwave_init,
            blit=True,
        )
        plt.show()

    def identify(self):
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

                mf.displaymfccprediction(filepath)
                time.sleep(0.5)
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

        return


a = Audiowave()


def recorder_run():
    while 1:
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

    a.identify()
