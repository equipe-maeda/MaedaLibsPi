#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
import threading


class Encoder(threading.Thread):
    def __init__(self, channel):
        threading.Thread.__init__(self)
        self.channel = channel
        GPIO.setup(self.channel, GPIO.IN)
        GPIO.add_event_detect(self.channel, GPIO.RISING)
    
    def run(self) -> None:
        while True:
            if GPIO.event_detected(self.channel):
                print('Detectou!')