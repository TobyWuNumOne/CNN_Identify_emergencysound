import RPi.GPIO as GPIO
import time
import wave
import numpy as np
import threading

GPIO.setmode(GPIO.BCM)

# set up the input pin
microphone_pin = 17
GPIO.setup(microphone_pin, GPIO.IN)

# set up recording parameters
sample_rate = 44100
sample_width = 2
duration = 5  # record for 5 seconds
chunk_size = 1024
frames = []


def record():
    global frames
    samples = int(sample_rate * duration)
    chunks = samples // chunk_size
    remainder_samples = samples % chunk_size
    for i in range(chunks):
        chunk = []
        for j in range(chunk_size):
            chunk.append(
                np.frombuffer(
                    np.array([GPIO.input(microphone_pin)], dtype=np.int16).tobytes(),
                    dtype=np.int16,
                )
            )
        frames.append(np.concatenate(chunk))
    if remainder_samples != 0:
        remainder = []
        for j in range(remainder_samples):
            remainder.append(
                np.frombuffer(
                    np.array([GPIO.input(microphone_pin)], dtype=np.int16).tobytes(),
                    dtype=np.int16,
                )
            )
        frames.append(np.concatenate(remainder))


# start recording in a separate thread
record_thread = threading.Thread(target=record)
record_thread.start()

# wait for recording to finish
record_thread.join()

# save recorded audio to file
with wave.open("recorded_audio.wav", "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(b"".join(frames))

GPIO.cleanup()
