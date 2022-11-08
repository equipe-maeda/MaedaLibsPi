import time
import board
import busio

#Define o tipo de módulo usado, no caso, o ADS1115
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class ADS1115:
    def __init__(self,channel=0):
        self.dev = busio.I2C(scl=board.SCL, sda=board.SDA)
        #Cria o objeto ADC
        self.ads = ADS.ADS1115(self.dev)
        self.channel = None
        if channel == 0:
            self.channel = AnalogIn(self.ads, ADS.P0)
        elif channel == 1:
            self.channel = AnalogIn(self.ads, ADS.P1)
        elif channel == 2:
            self.channel = AnalogIn(self.ads, ADS.P2)
        elif channel == 3:
            self.channel = AnalogIn(self.ads, ADS.P3)
            
    def readValueFrom(self):
        return self.channel.value & 0xfff8
    
    def readVoltsFrom(self):
        media = 1 # Se quiser aumentar o número de médias...
        value = 0
        for i in range(media):
            value += self.readValueFrom()
        
        value = value/media
        
        # Quando for 15bits (32767) multiplicar por 2 e quando for 16bits (65535) multiplicar por 1
        return ( (4.096 * 2) / 0xffff ) * value   
    
if __name__ == "__main__":
    test = ADS1115(channel=0)
    while True:
        
        print("{} valor ad.".format(test.readValueFrom()))
        print("{} volts.".format(test.readVoltsFrom()))
        time.sleep(1)


