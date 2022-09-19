import utime

import machine
from machine import I2C, Pin
from maeda.LcdApi import LcdApi
from maeda.PicoI2cLcd import I2cLcd
from maeda.Pressao4a20 import Pressao4a20
from maeda.Pt100Maeda import Pt100
from maeda.Csv import Csv
from maeda.ReleCiclicoMaeda import ReleCiclico
from maeda.Config import config
from maeda.SystemFile import File

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

TEMP_CAMARA_AMB = 16
TEMP_CAMARA_QUENTE = 150
TEMP_CAMARA_FRIO = -30

TEMP_TANQUE_AMB = 23
TEMP_TANQUE_1 = 94
TEMP_TANQUE_2 = 118
TEMP_TANQUE_3 = 23
TEMP_TANQUE_4 = -10

ESTAGIO_1 = 0
ESTAGIO_2 = 1
ESTAGIO_3 = 2
ESTAGIO_4 = 3

TEMPO_1 = 7200
TEMPO_2 = 3900
TEMPO_3 = 4200

estagios = ESTAGIO_1

ERRO_PRESS = -2.4
pin_in_enable = Pin(6, Pin.IN, Pin.PULL_UP)
pin_out_valvula = Pin(7, Pin.OUT)
pin_out_temp_tanque = Pin(5, Pin.OUT)

tempo_primeira_temperatura = TEMPO_1 #7200 segundos  =  120minutos
tempo_segunda_temperatura = TEMPO_2 #3900 segundos  =  65minutos
tempo_terceira_temperatura = TEMPO_3

habilita_contagem = False

def control_temperature(estagios,
                        habilita_contagem,
                        tempo_primeira_temperatura,
                        tempo_segunda_temperatura,
                        tempo_terceira_temperatura
                        ):
    if estagios == ESTAGIO_1:
        if t_amb.temperatura_sistema >= TEMP_CAMARA_AMB:
            print("estagio 1")
            if t_tanque.temperatura_sistema < TEMP_TANQUE_1:
                pin_out_temp_tanque.value(1)
            else:
                pin_out_temp_tanque.value(0)
                habilita_contagem = True
                
            if habilita_contagem == True:
                tempo_primeira_temperatura -= 1
            
            if tempo_primeira_temperatura <= 0:
                tempo_primeira_temperatura = TEMPO_1
                estagios = ESTAGIO_2
                habilita_contagem = False
    
    elif estagios == ESTAGIO_2:
        if t_amb.temperatura_sistema >= TEMP_CAMARA_QUENTE:
            print("estagio 2")
            if t_tanque.temperatura_sistema < TEMP_TANQUE_2:
                pin_out_temp_tanque.value(1)
            else:
                pin_out_temp_tanque.value(0)
                habilita_contagem = True
                
            if habilita_contagem == True:
                tempo_segunda_temperatura -= 1
            
            if tempo_primeira_temperatura <= 0:
                tempo_segunda_temperatura = TEMPO_2
                estagios = ESTAGIO_3
                habilita_contagem = False

    elif estagios == ESTAGIO_3:
        print("estagio 3")
        if t_amb.temperatura_sistema <= TEMP_CAMARA_AMB:
            if t_tanque.temperatura_sistema > TEMP_TANQUE_3:
                pin_out_temp_tanque.value(0)
            else:
                habilita_contagem = True
                
            if habilita_contagem == True:
                tempo_terceira_temperatura -= 1
            
            if tempo_primeira_temperatura <= 0:
                tempo_terceira_temperatura = TEMPO_3
                estagios = ESTAGIO_4
                habilita_contagem = False
    else:
        pin_out_temp_tanque.value(0)
        print("Fim de estágio")
        
if __name__ == "__main__":
    
    i2c = I2C(1, sda=machine.Pin(18), scl=machine.Pin(19), freq=400000)
    lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS) 
    test_canal_0 = Pressao4a20(channel = 1, erro=ERRO_PRESS)
    t_amb = Pt100(2)
    t_tanque = Pt100(3)
        
    csv = Csv(labels = ['Data','Hora', 'Pressao', 'Temperatura Ambiente', 'Temperatura Tanque'], directory = "dados_hba.csv")
    valvula_solenoide = ReleCiclico(base=config.BASE_TIME_SECONDS,
                                    value_ton=2,
                                    value_toff=2,
                                    start_direction = config.DIRECTION_TON,
                                    qtd_ciclos=6000,
                                    pin=pin_out_valvula,
                                    logic_state = config.LOGIC_STATE_DOW
                                    )
    
    file_ = File("config.txt")
    
    prin
    
    if file_:
        try:
            config = file_.read_file()
            result = config.split(';')
            estagios = int(result[0])
            habilita_contagem = bool(result[1])
            tempo_primeira_temperatura = int(result[2])
            tempo_segunda_temperatura = int(result[3])
            tempo_terceira_temperatura = int(result[4])
        except:
            print("Não há configurações para essa processo!!.")
    
    
    while True:
        time = utime.localtime()
#         print("{PP:>0.1f}".format(PP=test_canal_0.pressao_sistema))
        
        lcd.putstr_posi(0,1,string="Pressao: {PP:>0.1f} bar  ".format(PP=test_canal_0.pressao_sistema))
        lcd.putstr_posi(0,2,string="Ambiente: {TA:>0.1f} C  ".format(TA=t_amb.temperatura_sistema))
        lcd.putstr_posi(0,3,string="Tanque: {TT:>0.1f} C  ".format(TT=t_tanque.temperatura_sistema))
        
        if pin_in_enable.value() == 0:
            
            control_temperature(estagios,
                                habilita_contagem,
                                tempo_primeira_temperatura,
                                tempo_segunda_temperatura,
                                tempo_terceira_temperatura
                                )
                
            
            lcd.putstr_posi(0,0,"{HH:>02d}:{MM:>02d}:{SS:>02d} Gravando   ".format(HH=time[3], MM=time[4], SS=time[5]))
            csv.load_value(["{day:>02d}/{month:>02d}/{year:>02d}".format(day=time[0], month=time[1], year=time[2]),
                            "{HH:>02d}:{MM:>02d}:{SS:>02d}".format(HH=time[3],MM=time[4],SS=time[5]),
                            "{PP:>0.1f}".format(PP=test_canal_0.pressao_sistema),
                            "{TA:>0.1f}".format(TA=t_amb.temperatura_sistema),
                            "{TT:>0.1f}".format(TT=t_tanque.temperatura_sistema)
                            ])
            file_ = File("config.txt")
            file_.write_file("{};{};{};{};{}".format(estagios,
                                                 habilita_contagem,
                                                 tempo_primeira_temperatura,
                                                 tempo_segunda_temperatura,
                                                 tempo_terceira_temperatura
                                                 ))
            
            
            if (estagios == ESTAGIO_1) and (t_amb.temperatura_sistema >= TEMP_CAMARA_QUENTE):
                valvula_solenoide.start()
            elif (estagios == ESTAGIO_4) and (t_amb.temperatura_sistema >= TEMP_CAMARA_FRIO):
                valvula_solenoide.stop()
            
        else:
            valvula_solenoide.stop()
            lcd.putstr_posi(0,0,"{HH:>02d}:{MM:>02d}:{SS:>02d} Parado     ".format(HH=time[3], MM=time[4], SS=time[5]))
            pin_out_temp_tanque.value(0)
        
        utime.sleep(0.8)
