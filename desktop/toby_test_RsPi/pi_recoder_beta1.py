import RPi.GPIO as GPIO  # 你先 sudo apt-get install python3-rpi.gpio
import wave
import numpy as np


GPIO.setmode(GPIO.BCM)

microphone_pin = 17  # ky-037 DO 插在GPIO 17角位
GPIO.setup(microphone_pin, GPIO.IN)  # 設定腳位


sample_rate = 44100
sample_width = 2
duration = 5  # 五秒
frames = []


samples = int(sample_rate * duration)
for i in range(samples):
    frames.append(
        np.frombuffer(
            np.array([GPIO.input(microphone_pin)], dtype=np.int16).tobytes(),
            dtype=np.int16,
        )
    )

# 存擋
with wave.open("recorded_audio.wav", "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(b"".join(frames))

GPIO.cleanup()
