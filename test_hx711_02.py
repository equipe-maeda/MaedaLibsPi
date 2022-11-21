#!/usr/bin/python3
import RPi.GPIO as GPIO  # import GPIO
GPIO.setwarnings(False)
from hx711 import HX711
import time

# try:
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
hx = HX711(
    dout_pin=26,
    pd_sck_pin=20,
    channel='A',
    gain=64
)

hx.reset()   # Before we start, reset the HX711 (not obligate)
    # while True:
    #     measures = hx.get_raw_data(times=3)
    #     time.sleep(1)
# finally:
#     GPIO.cleanup()  # always do a GPIO cleanup in your scripts!

while True:
    measures = hx.get_raw_data(times=20)
    print(measures)
    # time.sleep(1)