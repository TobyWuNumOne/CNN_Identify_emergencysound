import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # TODO
GPIO.setup(18, GPIO.OUT)
while True:
    # 在這裡進行輸出操作
    GPIO.output(18, GPIO.HIGH)
    # print("1")
    time.sleep(0.02)
    GPIO.output(18, GPIO.LOW)
    # print("0")
    time.sleep(0.02)
