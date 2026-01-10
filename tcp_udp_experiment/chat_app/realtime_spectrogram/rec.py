import sounddevice as sd
import soundfile as sf

duration = 3
sr = 44100

print("recording")
data = sd.rec(int(duration * sr), samplerate=sr, channels=1)
sd.wait()
sf.write("recorded.wav", data,sr)
print("saved")