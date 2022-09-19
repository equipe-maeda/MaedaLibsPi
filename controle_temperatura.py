from machine import Pin
from maeda.Pt100Maeda import Pt100
import utime

pin_out = Pin(6, Pin.OUT)
pin_in = Pin(7, Pin.IN, Pin.PULL_UP)

pin_out.value(0)

pt = Pt100(1)

while True:
    if pin_in.value() == 0:
        print(pt.temperatura_sistema)
        if pt.temperatura_sistema < 30:
            pin_out.value(1)
        else:
            pin_out.value(0)
        
    else:
        pin_out.value(0)
        
    utime.sleep(1)