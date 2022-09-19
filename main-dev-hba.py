import time
from maeda.Pressao4a20 import Pressao4a20
from maeda.Pt100Maeda import Pt100
from maeda.Csv import Csv
from maeda.IOSystem import InPut

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

ERRO_PRESS = 0.0#-2.4
# pin_in_enable = Pin(6, Pin.IN, Pin.PULL_UP)


if __name__ == "__main__":

 

    test_canal_0 = Pressao4a20(channel = 1, erro=ERRO_PRESS)
    t_amb = Pt100(2)
    t_tanque = Pt100(3)
    input = InPut(13)
    
    csv = Csv(labels = ['Tempo', 'Pressao', 'Temperatura Ambiente', 'Temperatura Tanque'], directory = "dados_hba.csv")
    
    while True:
        time_local = time.localtime()

        print("Pressao: {PP:>0.1f} bar  ".format(PP=test_canal_0.pressao_sistema))
        print("Ambiente: {TA:>0.1f} C  ".format(TA=t_amb.temperatura_sistema))
        print("Tanque: {TT:>0.1f} C  ".format(TT=t_tanque.temperatura_sistema))
        
        if input.input == 0:
            print("{HH:>02d}:{MM:>02d}:{SS:>02d} Gravando   ".format(HH=time_local[3], MM=time_local[4], SS=time_local[5]))
            csv.load_value(["{HH:>02d}:{MM:>02d}:{SS:>02d}".format(HH=time_local[3],MM=time_local[4],SS=time_local[5]),
                            "{PP:>0.1f}".format(PP=test_canal_0.pressao_sistema),
                            "{TA:>0.1f}".format(TA=t_amb.temperatura_sistema),
                            "{TT:>0.1f}".format(TT=t_tanque.temperatura_sistema)])
        else:
            print("{HH:>02d}:{MM:>02d}:{SS:>02d} Parado     ".format(HH=time_local[3], MM=time_local[4], SS=time_local[5]))
        
        time.sleep(1)
