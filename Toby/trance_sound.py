from scipy import signal
import scipy
import os
from alive_progress import alive_bar

# install
# 修改資料即可對資料夾內所有檔案

# 存放位置
Folder = "./Toby/soundfile/"

# output 存放位置
save_Folder = "./Toby/soundfile_output/"
fs = 22050
lowcut = 500
highcut = 4000


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], btype="band")
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.lfilter(b, a, data)
    return y


with alive_bar(len(os.listdir(Folder))) as bar:  # progress bar
    for file in os.listdir(Folder):
        fs, data = scipy.io.wavfile.read(Folder + file)
        print(fs)
        filtedData = butter_bandpass_filter(data, lowcut, highcut, fs)
        scipy.io.wavfile.write(save_Folder + file, fs, filtedData)
        bar()  # progress bar
