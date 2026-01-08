import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

y, sr = librosa.load("bgms/jodo.mp3", sr=None)
hop = 512
S = librosa.stft(y, hop_length=hop)
S_db = librosa.amplitude_to_db(np.abs(S), ref=np.max)

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
img = librosa.display.specshow(
    S_db, x_axis="time", y_axis="log", sr=sr, hop_length=hop, ax=ax
)
ax.set_title("Spectrogram")

# スライダーで表示開始秒を動かす
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03])
max_t = librosa.get_duration(y=y, sr=sr)
window = 10.0  # 表示する秒数
slider = Slider(ax_slider, "t", 0.0, max_t - window, valinit=0.0)

def update(val):
    t0 = slider.val
    ax.set_xlim(t0, t0 + window)
    fig.canvas.draw_idle()

slider.on_changed(update)
plt.show()
