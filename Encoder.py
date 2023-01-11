#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
import threading


class Encoder(threading.Thread):
    def __init__(self, channel, fn):
        threading.Thread.__init__(self)
        self.channel = channel
        GPIO.setup(self.channel, GPIO.IN)
        GPIO.add_event_detect(self.channel, GPIO.RISING)
        self.fn = fn
    
    def run(self) -> None:
        while True:
            try:
                if GPIO.event_detected(self.channel):
                    self.fn()
            except:
                break

    def fn(self):
        pass