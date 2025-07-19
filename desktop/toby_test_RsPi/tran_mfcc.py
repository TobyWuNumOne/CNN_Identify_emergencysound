import librosa.display
import matplotlib.pyplot as plt
import sys

path_wav = ""
sys.path.append(path_wav)


def displaymfccs(path):
    filepath = path
    data, sr = librosa.load(filepath)
    print(len(data))
    # plt.plot(data)
    mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13, dct_type=2, norm="ortho")
    # mfccs = sklearn.preprocessing.scale(mfccs)
    normalized_mfcc = librosa.util.normalize(mfccs)
    fig, ax = plt.subplots()
    print(normalized_mfcc.shape)
    # img = librosa.display.specshow(normalized_mfcc, x_axis="time", ax=ax)
    # fig.colorbar(img, ax=ax)
    # plt.show()


displaymfccs(path_wav)
