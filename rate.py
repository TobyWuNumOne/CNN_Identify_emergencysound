import os
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
import warnings

path="a//a_1.wav"
wf = wave.open(path, 'r')
rate=wf.getframerate()
print(rate)