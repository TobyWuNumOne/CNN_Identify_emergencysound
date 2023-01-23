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
import wave
import numpy as np
import pylab as plt
import librosa.display
import matplotlib.pyplot as plt
import sklearn
import numpy
import wave
from keras.models import load_model
import librosa.display
import numpy as np
import keras
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import cm

filepath = "./a/1.wav"
data, sr = librosa.load(filepath)


mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
normalized_mfcc = librosa.util.normalize(mfccs)

fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(6, 4))

time = np.linspace(0, 10, 100)
axs[0].plot(time, np.sin(time))
axs[0].set_xlim(0 - 2, 10 + 2)


# load image
# img = librosa.display.specshow(normalized_mfcc, x_axis="time", ax=axs)
# print(type(img))


axs[1].imshow(
    normalized_mfcc, interpolation="nearest", cmap=cm.coolwarm, origin="lower"
)
axs[1].set_title("MFCC")


plt.show()
