#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
GPIO.setwarnings(False)
from hx711 import HX711  # import the class HX711
GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering

N3 = 22
N4 = 4

GPIO.setup(N3, GPIO.OUT)
GPIO.setup(N4, GPIO.OUT)

GPIO.output(N3, 0)
GPIO.output(N4, 0)

cmd = 'H'

while cmd.upper() != 'Q':

    cmd = input("Digite comando:\nS = Subir\nD = Descer\nP = Parar\nF Freiar\nQ = Sair do programa\n")

    if(cmd.upper() == 'S'):
        GPIO.output(N3, 1)
        GPIO.output(N4, 0)

    if(cmd.upper() == 'D'):
        GPIO.output(N3, 0)
        GPIO.output(N4, 1)

    if(cmd.upper() == 'P'):
        GPIO.output(N3, 0)
        GPIO.output(N4, 0)
    
    if(cmd.upper() == 'F'):
        GPIO.output(N3, 1)
        GPIO.output(N4, 1)

GPIO.cleanup()