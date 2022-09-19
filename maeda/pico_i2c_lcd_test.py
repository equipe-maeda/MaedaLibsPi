import utime

import machine
from machine import I2C
from maeda.LcdApi import LcdApi
from maeda.PicoI2cLcd import I2cLcd
from maeda.Pressao4a20 import Pressao4a20

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

def test_main():
    #Test function for verifying basic functionality
    print("Running test_main")
    i2c = I2C(1, sda=machine.Pin(18), scl=machine.Pin(19), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)    
    lcd.putstr("It Works!")
    utime.sleep(2)
    lcd.clear()
    
    count = 0
    while True:
        lcd.clear()
        
        time = utime.localtime()
        lcd.putstr("{year:>04d}/{month:>02d}/{day:>02d} {HH:>02d}:{MM:>02d}:{SS:>02d}".format(
            year=time[0], month=time[1], day=time[2],
            HH=time[3], MM=time[4], SS=time[5]))
        if count % 10 == 0:
            print("Turning cursor on")
            lcd.show_cursor()
        if count % 10 == 1:
            print("Turning cursor off")
            lcd.hide_cursor()
        if count % 10 == 2:
            print("Turning blink cursor on")
            lcd.blink_cursor_on()
        if count % 10 == 3:
            print("Turning blink cursor off")
            lcd.blink_cursor_off()                    
        if count % 10 == 4:
            print("Turning backlight off")
            lcd.backlight_off()
        if count % 10 == 5:
            print("Turning backlight on")
            lcd.backlight_on()
        if count % 10 == 6:
            print("Turning display off")
            lcd.display_off()
        if count % 10 == 7:
            print("Turning display on")
            lcd.display_on()
        if count % 10 == 8:
            print("Filling display")
            lcd.clear()
            string = ""
            for x in range(32, 32+I2C_NUM_ROWS*I2C_NUM_COLS):
                string += chr(x)
            lcd.putstr(string)
        count += 1
        utime.sleep(2)

if __name__ == "__main__":
    i2c = I2C(1, sda=machine.Pin(18), scl=machine.Pin(19), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS) 
    test_canal_0 = Pressao4a20(channel = 1)
    while True:
#         lcd.clear()
#         lcd.move_to(0,0)
        print(test_canal_0.pressao_sistema)
    #     test_canal_0.calibracao()
        
   
        lcd.putstr_posi(0,0,"Renato Oliveira!")
        lcd.putstr_posi(0,1,string="Pressao: {} bar".format(test_canal_0.pressao_sistema))
        utime.sleep(1)
    #     test_main()

