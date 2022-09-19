#Link = https://www.youtube.com/watch?v=mOEHRRXlv84

import utime
from machine import I2C, Pin

pino_c0 = Pin(13, Pin.OUT)
pino_c1 = Pin(14, Pin.OUT)
pino_c2 = Pin(15, Pin.OUT)

pino_c0.value(0)
pino_c1.value(0)
pino_c2.value(0)

dev = I2C(0, scl=Pin(9), sda=Pin(8))

print(dev.scan())

address = 72

def readConfig():
    dev.writeto(address, bytearray([1]))
    result = dev.readfrom(address, 2)
    return result[0]<<8 | result[0]

print( bin(readConfig()) )
    
def readValueFrom(channel):
    media = 200
    value = 0
    config = readConfig()
    
    config &= ~(7<<12)# limpa MUX bits
    config &= ~(7<<9)# limpa PGA bits
    
    config |= (7 & (4 + channel))<< 12
    config |= (1<<15) # Trigger para proxima conversão
    config |= (1<<9) # ganho 4.048 volts
    
    config = [int(config>>i & 0xff) for i in [8,0]]
    
    dev.writeto(address, bytearray([1] + config))
    
    config = readConfig()
    
    while (config & 0x8000) == 0:
        #print("Entrou while ", config)
        config = readConfig()
    
        
    dev.writeto(address, bytearray([0]))
    
    for i in range(media):
        result = dev.readfrom(address, 2)
        value += result[1] 
        
    value = int(value/media)
    
    
    #return result[0]<<8 | result[0]
    
    #return (result[0]<<9 | result[0]) + (value<<1 & 0xf0 ) # Para 16bits
    return (result[0]<<8 | result[0]) + (value & 0xfc ) #para 15bits

def readVoltsFrom(channel):
    media = 1
    value = 0
    for i in range(media):
        value += readValueFrom(channel)
    
    value = value/media
    
    # Quando for 15bits (32767) multiplicar por 2 e quando for 16bits (65535) multiplicar por 1
    return ( (4.096 * 2) / 0xffff ) * value


value = 0
volts = 0
while True:
    value = readValueFrom(1)
    volts = readVoltsFrom(1)
    print("Value: {} Volts: {}".format(value, round(volts,4)))
    
    utime.sleep(0.5)
        
