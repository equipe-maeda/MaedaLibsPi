import RPi.GPIO as GPIO
from maeda.Config import config

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class OutPut:
    def __init__(self, output, pull = None):
        self._output = output
        GPIO.setup(self._output, GPIO.OUT)


    def output(self, value):
        GPIO.output(self._output,value)
          
class InPut:
    def __init__(self, input = None, pull = None):
        self._input = input 
        if pull == config.PULL_UP:
            GPIO.setup(self._input, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        elif pull == config.PULL_DOWN:
            GPIO.setup(self._input, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif pull == None:
            GPIO.setup(self._input, GPIO.IN)
        

    @property
    def input(self):
        return GPIO.input(self._input)
    