import librosa 
import numpy
from matplotlib import pyplot as plt
import os

filename = "bgms/jodo.mp3"
y, sr = librosa.load(filename, sr=None)
print(sr)
print(type(y), type(sr))
S = librosa.stft(y)
print(type(S))
print(S.shape)
fig = librosa.display.specshow(S, x_axis="time", y_axis="log", sr=sr)

plt.savefig("figs/"+ os.path.basename(filename.split(".")[0]) + ".png")